"""Controller that Manages Matter devices."""

# pylint: disable=too-many-lines

from __future__ import annotations

import asyncio
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import partial
import logging
from random import randint
import time
from typing import TYPE_CHECKING, Any, Callable, Iterable, TypeVar, cast

from chip.ChipDeviceCtrl import DeviceProxyWrapper
from chip.clusters import Attribute, Objects as Clusters
from chip.clusters.Attribute import ValueDecodeFailure
from chip.clusters.ClusterObjects import ALL_ATTRIBUTES, ALL_CLUSTERS, Cluster
from chip.exceptions import ChipStackError
from zeroconf import IPVersion, ServiceStateChange, Zeroconf
from zeroconf.asyncio import AsyncServiceBrowser, AsyncServiceInfo, AsyncZeroconf

from matter_server.common.models import CommissionableNodeData, CommissioningParameters
from matter_server.server.helpers.attributes import parse_attributes_from_read_result
from matter_server.server.helpers.utils import ping_ip

from ..common.errors import (
    NodeCommissionFailed,
    NodeInterviewFailed,
    NodeNotExists,
    NodeNotReady,
    NodeNotResolving,
)
from ..common.helpers.api import api_command
from ..common.helpers.util import (
    create_attribute_path_from_attribute,
    dataclass_from_dict,
    dataclass_to_dict,
    parse_attribute_path,
    parse_value,
)
from ..common.models import (
    APICommand,
    EventType,
    MatterNodeData,
    MatterNodeEvent,
    NodePingResult,
)
from .const import DATA_MODEL_SCHEMA_VERSION, PAA_ROOT_CERTS_DIR
from .helpers.paa_certificates import fetch_certificates

if TYPE_CHECKING:
    from chip.ChipDeviceCtrl import ChipDeviceController

    from .server import MatterServer

_T = TypeVar("_T")

DATA_KEY_NODES = "nodes"
DATA_KEY_LAST_NODE_ID = "last_node_id"

LOGGER = logging.getLogger(__name__)
NODE_SUBSCRIPTION_CEILING = 60
NODE_SUBSCRIPTION_CEILING_BATTERY_POWERED = 1800
MAX_COMMISSION_RETRIES = 3
NODE_RESUBSCRIBE_ATTEMPTS_UNAVAILABLE = 3
NODE_RESUBSCRIBE_TIMEOUT_OFFLINE = 30 * 60 * 1000

MDNS_TYPE_OPERATIONAL_NODE = "_matter._tcp.local."
MDNS_TYPE_COMMISSIONABLE_NODE = "_matterc._udp.local."


ROUTING_ROLE_ATTRIBUTE_PATH = create_attribute_path_from_attribute(
    0, Clusters.ThreadNetworkDiagnostics.Attributes.RoutingRole
)


# pylint: disable=too-many-lines,too-many-locals,too-many-statements,too-many-branches,too-many-instance-attributes


class MatterDeviceController:
    """Class that manages the Matter devices."""

    chip_controller: ChipDeviceController | None
    fabric_id_hex: str

    def __init__(
        self,
        server: MatterServer,
    ):
        """Initialize the device controller."""
        self.server = server
        # we keep the last events in memory so we can include them in the diagnostics dump
        self.event_history: deque[Attribute.EventReadResult] = deque(maxlen=25)
        self._subscriptions: dict[int, Attribute.SubscriptionTransaction] = {}
        self._nodes_in_setup: set[int] = set()
        self._mdns_last_seen: dict[int, float] = {}
        self._nodes: dict[int, MatterNodeData] = {}
        self._last_known_ip_addresses: dict[int, list[str]] = {}
        self._last_subscription_attempt: dict[int, int] = {}
        self._known_commissioning_params: dict[int, CommissioningParameters] = {}
        self.wifi_credentials_set: bool = False
        self.thread_credentials_set: bool = False
        self.compressed_fabric_id: int | None = None
        self._node_lock: dict[int, asyncio.Lock] = {}
        self._aiobrowser: AsyncServiceBrowser | None = None
        self._aiozc: AsyncZeroconf | None = None
        self._sdk_executor = ThreadPoolExecutor(max_workers=1)

    async def initialize(self) -> None:
        """Async initialize of controller."""
        # (re)fetch all PAA certificates once at startup
        # NOTE: this must be done before initializing the controller
        await fetch_certificates()
        # Instantiate the underlying ChipDeviceController instance on the Fabric
        self.chip_controller = self.server.stack.fabric_admin.NewController(
            paaTrustStorePath=str(PAA_ROOT_CERTS_DIR)
        )
        self.compressed_fabric_id = cast(
            int, await self._call_sdk(self.chip_controller.GetCompressedFabricId)
        )
        self.fabric_id_hex = hex(self.compressed_fabric_id)[2:]
        LOGGER.debug("CHIP Device Controller Initialized")

    async def start(self) -> None:
        """Handle logic on controller start."""
        # load nodes from persistent storage
        nodes: dict[str, dict | None] = self.server.storage.get(DATA_KEY_NODES, {})
        orphaned_nodes: set[str] = set()
        for node_id_str, node_dict in nodes.items():
            node_id = int(node_id_str)
            if node_dict is None:
                # Non-initialized (left-over) node from a failed commissioning attempt.
                # NOTE: This code can be removed in a future version
                # as this can no longer happen.
                orphaned_nodes.add(node_id_str)
                continue
            try:
                node = dataclass_from_dict(MatterNodeData, node_dict, strict=True)
            except (KeyError, ValueError):
                # constructing MatterNodeData from the cached dict is not possible,
                # revert to a fallback object and the node will be re-interviewed
                node = MatterNodeData(
                    node_id=node_id,
                    date_commissioned=node_dict.get(
                        "date_commissioned",
                        datetime(1970, 1, 1),
                    ),
                    last_interview=node_dict.get(
                        "last_interview",
                        datetime(1970, 1, 1),
                    ),
                    interview_version=0,
                )
            # always mark node as unavailable at startup until subscriptions are ready
            node.available = False
            self._nodes[node_id] = node
        # cleanup orhpaned nodes from storage
        for node_id_str in orphaned_nodes:
            self.server.storage.remove(DATA_KEY_NODES, node_id_str)
        LOGGER.info("Loaded %s nodes from stored configuration", len(self._nodes))
        # set-up mdns browser
        self._aiozc = AsyncZeroconf(ip_version=IPVersion.All)
        services = [MDNS_TYPE_OPERATIONAL_NODE, MDNS_TYPE_COMMISSIONABLE_NODE]
        self._aiobrowser = AsyncServiceBrowser(
            self._aiozc.zeroconf,
            services,
            handlers=[self._on_mdns_service_state_change],
        )

    async def stop(self) -> None:
        """Handle logic on server stop."""
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")
        # unsubscribe all node subscriptions
        for sub in self._subscriptions.values():
            await self._call_sdk(sub.Shutdown)
        self._subscriptions = {}
        # shutdown (and cleanup) mdns browser
        if self._aiobrowser:
            await self._aiobrowser.async_cancel()
        if self._aiozc:
            await self._aiozc.async_close()
        # shutdown the sdk device controller
        await self._call_sdk(self.chip_controller.Shutdown)
        LOGGER.debug("Stopped.")

    @api_command(APICommand.GET_NODES)
    def get_nodes(self, only_available: bool = False) -> list[MatterNodeData]:
        """Return all Nodes known to the server."""
        return [
            x
            for x in self._nodes.values()
            if x is not None and (x.available or not only_available)
        ]

    @api_command(APICommand.GET_NODE)
    def get_node(self, node_id: int) -> MatterNodeData:
        """Return info of a single Node."""
        if node := self._nodes.get(node_id):
            return node
        raise NodeNotExists(f"Node {node_id} does not exist or is not yet interviewed")

    @api_command(APICommand.COMMISSION_WITH_CODE)
    async def commission_with_code(
        self, code: str, network_only: bool = False
    ) -> MatterNodeData:
        """
        Commission a device using a QR Code or Manual Pairing Code.

        :param code: The QR Code or Manual Pairing Code for device commissioning.
        :param network_only: If True, restricts device discovery to network only.

        :return: The NodeInfo of the commissioned device.
        """
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        node_id = self._get_next_node_id()

        attempts = 0
        # we retry commissioning a few times as we've seen devices in the wild
        # that are a bit unstable.
        # by retrying, we increase the chances of a successful commission
        while attempts <= MAX_COMMISSION_RETRIES:
            attempts += 1
            LOGGER.info(
                "Starting Matter commissioning with code using Node ID %s (attempt %s/%s).",
                node_id,
                attempts,
                MAX_COMMISSION_RETRIES,
            )
            success = await self._call_sdk(
                self.chip_controller.CommissionWithCode,
                setupPayload=code,
                nodeid=node_id,
                networkOnly=network_only,
            )
            if success:
                break
            if not success and attempts >= MAX_COMMISSION_RETRIES:
                raise NodeCommissionFailed(
                    f"Commission with code failed for node {node_id}."
                )
            await asyncio.sleep(5)

        LOGGER.info("Matter commissioning of Node ID %s successful.", node_id)

        # perform full (first) interview of the device
        # we retry the interview max 3 times as it may fail in noisy
        # RF environments (in case of thread), mdns trouble or just flaky devices.
        # retrying both the mdns resolve and (first) interview, increases the chances
        # of a successful device commission.
        retries = 3
        while retries:
            try:
                await self.interview_node(node_id)
            except (NodeNotResolving, NodeInterviewFailed) as err:
                if retries <= 0:
                    raise err
                retries -= 1
                LOGGER.warning("Unable to interview Node %s: %s", node_id, err)
                await asyncio.sleep(5)
            else:
                break

        # make sure we start a subscription for this newly added node
        await self._setup_node(node_id)
        LOGGER.info("Commissioning of Node ID %s completed.", node_id)
        # return full node object once we're complete
        return self.get_node(node_id)

    @api_command(APICommand.COMMISSION_ON_NETWORK)
    async def commission_on_network(
        self,
        setup_pin_code: int,
        filter_type: int = 0,
        filter: Any = None,  # pylint: disable=redefined-builtin
        ip_addr: str | None = None,
    ) -> MatterNodeData:
        """
        Do the routine for OnNetworkCommissioning, with a filter for mDNS discovery.

        The filter can be an integer,
        a string or None depending on the actual type of selected filter.

        NOTE: For advanced usecases only, use `commission_with_code`
        for regular commissioning.

        Returns full NodeInfo once complete.
        """
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        node_id = self._get_next_node_id()
        if ip_addr is not None:
            ip_addr = self.server.scope_ipv6_lla(ip_addr)

        attempts = 0
        # we retry commissioning a few times as we've seen devices in the wild
        # that are a bit unstable.
        # by retrying, we increase the chances of a successful commission
        while attempts <= MAX_COMMISSION_RETRIES:
            attempts += 1
            if ip_addr is None:
                # regular CommissionOnNetwork if no IP address provided
                LOGGER.info(
                    "Starting Matter commissioning on network using Node ID %s (attempt %s/%s).",
                    node_id,
                    attempts,
                    MAX_COMMISSION_RETRIES,
                )
                success = await self._call_sdk(
                    self.chip_controller.CommissionOnNetwork,
                    nodeId=node_id,
                    setupPinCode=setup_pin_code,
                    filterType=filter_type,
                    filter=filter,
                )
            else:
                LOGGER.info(
                    "Starting Matter commissioning using Node ID %s and IP %s (attempt %s/%s).",
                    node_id,
                    ip_addr,
                    attempts,
                    MAX_COMMISSION_RETRIES,
                )
                success = await self._call_sdk(
                    self.chip_controller.CommissionIP,
                    nodeid=node_id,
                    setupPinCode=setup_pin_code,
                    ipaddr=ip_addr,
                )
            if success:
                break
            if not success and attempts >= MAX_COMMISSION_RETRIES:
                raise NodeCommissionFailed(f"Commissioning failed for node {node_id}.")
            await asyncio.sleep(5)

        LOGGER.info("Matter commissioning of Node ID %s successful.", node_id)

        # perform full (first) interview of the device
        # we retry the interview max 3 times as it may fail in noisy
        # RF environments (in case of thread), mdns trouble or just flaky devices.
        # retrying both the mdns resolve and (first) interview, increases the chances
        # of a successful device commission.
        retries = 3
        while retries:
            try:
                await self.interview_node(node_id)
            except NodeInterviewFailed as err:
                if retries <= 0:
                    raise err
                retries -= 1
                LOGGER.warning("Unable to interview Node %s: %s", node_id, err)
                await asyncio.sleep(5)
            else:
                break
        # make sure we start a subscription for this newly added node
        await self._setup_node(node_id)
        LOGGER.info("Commissioning of Node ID %s completed.", node_id)
        # return full node object once we're complete
        return self.get_node(node_id)

    @api_command(APICommand.SET_WIFI_CREDENTIALS)
    async def set_wifi_credentials(self, ssid: str, credentials: str) -> None:
        """Set WiFi credentials for commissioning to a (new) device."""
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        await self._call_sdk(
            self.chip_controller.SetWiFiCredentials,
            ssid=ssid,
            credentials=credentials,
        )

        self.wifi_credentials_set = True

    @api_command(APICommand.SET_THREAD_DATASET)
    async def set_thread_operational_dataset(self, dataset: str) -> None:
        """Set Thread Operational dataset in the stack."""
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        await self._call_sdk(
            self.chip_controller.SetThreadOperationalDataset,
            threadOperationalDataset=bytes.fromhex(dataset),
        )

        self.thread_credentials_set = True

    @api_command(APICommand.OPEN_COMMISSIONING_WINDOW)
    async def open_commissioning_window(
        self,
        node_id: int,
        timeout: int = 300,
        iteration: int = 1000,
        option: int = 1,
        discriminator: int | None = None,
    ) -> CommissioningParameters:
        """Open a commissioning window to commission a device present on this controller to another.

        Returns code to use as discriminator.
        """
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        if (node := self._nodes.get(node_id)) is None or not node.available:
            raise NodeNotReady(f"Node {node_id} is not (yet) available.")

        if node_id in self._known_commissioning_params:
            # node has already been put into commissioning mode,
            # return previous parameters
            return self._known_commissioning_params[node_id]

        if discriminator is None:
            discriminator = randint(0, 4095)  # noqa: S311

        sdk_result = await self._call_sdk(
            self.chip_controller.OpenCommissioningWindow,
            nodeid=node_id,
            timeout=timeout,
            iteration=iteration,
            discriminator=discriminator,
            option=option,
        )
        self._known_commissioning_params[node_id] = params = CommissioningParameters(
            setup_pin_code=sdk_result.setupPinCode,
            setup_manual_code=sdk_result.setupManualCode,
            setup_qr_code=sdk_result.setupQRCode,
        )
        # we store the commission parameters and clear them after the timeout
        if TYPE_CHECKING:
            assert self.server.loop
        self.server.loop.call_later(
            timeout, self._known_commissioning_params.pop, node_id, None
        )
        return params

    @api_command(APICommand.DISCOVER)
    async def discover_commissionable_nodes(
        self,
    ) -> list[CommissionableNodeData]:
        """Discover Commissionable Nodes (discovered on BLE or mDNS)."""
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        sdk_result = await self._call_sdk(
            self.chip_controller.DiscoverCommissionableNodes,
        )
        if sdk_result is None:
            return []
        # ensure list
        if not isinstance(sdk_result, list):
            sdk_result = [sdk_result]
        return [
            CommissionableNodeData(
                instance_name=x.instanceName,
                host_name=x.hostName,
                port=x.port,
                long_discriminator=x.longDiscriminator,
                vendor_id=x.vendorId,
                product_id=x.productId,
                commissioning_mode=x.commissioningMode,
                device_type=x.deviceType,
                device_name=x.deviceName,
                pairing_instruction=x.pairingInstruction,
                pairing_hint=x.pairingHint,
                mrp_retry_interval_idle=x.mrpRetryIntervalIdle,
                mrp_retry_interval_active=x.mrpRetryIntervalActive,
                supports_tcp=x.supportsTcp,
                addresses=x.addresses,
                rotating_id=x.rotatingId,
            )
            for x in sdk_result
        ]

    @api_command(APICommand.INTERVIEW_NODE)
    async def interview_node(self, node_id: int) -> None:
        """Interview a node."""
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        try:
            if not (node := self._nodes.get(node_id)) or not node.available:
                await self._resolve_node(node_id=node_id)
            async with self._get_node_lock(node_id):
                LOGGER.info("Interviewing node: %s", node_id)
                read_response: Attribute.AsyncReadTransaction.ReadResponse = (
                    await self.chip_controller.Read(
                        nodeid=node_id,
                        attributes="*",
                        fabricFiltered=False,
                    )
                )
        except ChipStackError as err:
            raise NodeInterviewFailed(f"Failed to interview node {node_id}") from err

        is_new_node = node_id not in self._nodes
        existing_info = self._nodes.get(node_id)
        node = MatterNodeData(
            node_id=node_id,
            date_commissioned=(
                existing_info.date_commissioned if existing_info else datetime.utcnow()
            ),
            last_interview=datetime.utcnow(),
            interview_version=DATA_MODEL_SCHEMA_VERSION,
            available=existing_info.available if existing_info else False,
            attributes=parse_attributes_from_read_result(read_response.tlvAttributes),
        )

        if existing_info:
            node.attribute_subscriptions = existing_info.attribute_subscriptions
        # work out if the node is a bridge device by looking at the devicetype of endpoint 1
        if attr_data := node.attributes.get("1/29/0"):
            node.is_bridge = any(x[0] == 14 for x in attr_data)

        # save updated node data
        self._nodes[node_id] = node
        self._write_node_state(node_id, True)
        if is_new_node:
            # new node - first interview
            self.server.signal_event(EventType.NODE_ADDED, node)
        else:
            # existing node, signal node updated event
            # TODO: maybe only signal this event if attributes actually changed ?
            self.server.signal_event(EventType.NODE_UPDATED, node)

        LOGGER.debug("Interview of node %s completed", node_id)

    @api_command(APICommand.DEVICE_COMMAND)
    async def send_device_command(
        self,
        node_id: int,
        endpoint_id: int,
        cluster_id: int,
        command_name: str,
        payload: dict,
        response_type: Any | None = None,
        timed_request_timeout_ms: int | None = None,
        interaction_timeout_ms: int | None = None,
    ) -> Any:
        """Send a command to a Matter node/device."""
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")
        if (node := self._nodes.get(node_id)) is None or not node.available:
            raise NodeNotReady(f"Node {node_id} is not (yet) available.")
        cluster_cls: Cluster = ALL_CLUSTERS[cluster_id]
        command_cls = getattr(cluster_cls.Commands, command_name)
        command = dataclass_from_dict(command_cls, payload, allow_sdk_types=True)
        async with self._get_node_lock(node_id):
            return await self.chip_controller.SendCommand(
                nodeid=node_id,
                endpoint=endpoint_id,
                payload=command,
                responseType=response_type,
                timedRequestTimeoutMs=timed_request_timeout_ms,
                interactionTimeoutMs=interaction_timeout_ms,
            )

    @api_command(APICommand.READ_ATTRIBUTE)
    async def read_attribute(
        self, node_id: int, attribute_path: str, fabric_filtered: bool = False
    ) -> dict[str, Any]:
        """Read one or more attribute(s) on a node by specifying an attributepath."""
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")
        if (node := self._nodes.get(node_id)) is None or not node.available:
            raise NodeNotReady(f"Node {node_id} is not (yet) available.")
        endpoint_id, cluster_id, attribute_id = parse_attribute_path(attribute_path)
        assert self.server.loop is not None
        async with self._get_node_lock(node_id):
            future = self.server.loop.create_future()
            device = await self._resolve_node(node_id)
            Attribute.Read(
                future=future,
                eventLoop=self.server.loop,
                device=device.deviceProxy,
                devCtrl=self.chip_controller,
                attributes=[
                    Attribute.AttributePath(
                        EndpointId=endpoint_id,
                        ClusterId=cluster_id,
                        AttributeId=attribute_id,
                    )
                ],
                fabricFiltered=fabric_filtered,
            ).raise_on_error()
            result: Attribute.AsyncReadTransaction.ReadResponse = await future
            read_atributes = parse_attributes_from_read_result(result.tlvAttributes)
            # update cached info in node attributes
            self._nodes[node_id].attributes.update(read_atributes)
            self._write_node_state(node_id)
            return read_atributes

    @api_command(APICommand.WRITE_ATTRIBUTE)
    async def write_attribute(
        self,
        node_id: int,
        attribute_path: str,
        value: Any,
    ) -> Any:
        """Write an attribute(value) on a target node."""
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")
        if (node := self._nodes.get(node_id)) is None or not node.available:
            raise NodeNotReady(f"Node {node_id} is not (yet) available.")
        endpoint_id, cluster_id, attribute_id = parse_attribute_path(attribute_path)
        attribute = cast(
            Clusters.ClusterAttributeDescriptor,
            ALL_ATTRIBUTES[cluster_id][attribute_id](),
        )
        attribute.value = parse_value(
            name=attribute_path,
            value=value,
            value_type=attribute.attribute_type.Type,
            allow_sdk_types=True,
        )
        async with self._get_node_lock(node_id):
            return await self.chip_controller.WriteAttribute(
                nodeid=node_id,
                attributes=[(endpoint_id, attribute)],
            )

    @api_command(APICommand.REMOVE_NODE)
    async def remove_node(self, node_id: int) -> None:
        """Remove a Matter node/device from the fabric."""
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        if node_id not in self._nodes:
            raise NodeNotExists(
                f"Node {node_id} does not exist or has not been interviewed."
            )

        LOGGER.info("Removing Node ID %s.", node_id)

        # shutdown any existing subscriptions
        if sub := self._subscriptions.pop(node_id, None):
            await self._call_sdk(sub.Shutdown)

        node = self._nodes.pop(node_id)
        self.server.storage.remove(
            DATA_KEY_NODES,
            subkey=str(node_id),
        )
        LOGGER.info("Node ID %s successfully removed from Matter server.", node_id)

        self.server.signal_event(EventType.NODE_REMOVED, node_id)

        assert node is not None

        attribute_path = create_attribute_path_from_attribute(
            0,
            Clusters.OperationalCredentials.Attributes.CurrentFabricIndex,
        )
        fabric_index = node.attributes.get(attribute_path)
        if fabric_index is None:
            return
        result: Clusters.OperationalCredentials.Commands.NOCResponse | None = None
        try:
            result = await self.chip_controller.SendCommand(
                nodeid=node_id,
                endpoint=0,
                payload=Clusters.OperationalCredentials.Commands.RemoveFabric(
                    fabricIndex=fabric_index,
                ),
            )
        except ChipStackError as err:
            LOGGER.warning("Removing current fabric from device failed.", exc_info=err)
            return
        if (
            result is None
            or result.statusCode
            == Clusters.OperationalCredentials.Enums.NodeOperationalCertStatusEnum.kOk
        ):
            LOGGER.info("Successfully removed Home Assistant fabric from device.")
        else:
            LOGGER.warning(
                "Removing current fabric from device failed with status code %d.",
                result.statusCode,
            )

    @api_command(APICommand.SUBSCRIBE_ATTRIBUTE)
    async def subscribe_attribute(
        self, node_id: int, attribute_path: str | list[str]
    ) -> None:
        """
        Subscribe to given AttributePath(s).

        Either supply a single attribute path or a list of paths.
        The given attribute path(s) will be added to the list of attributes that
        are watched for the given node. This is persistent over restarts.
        """
        LOGGER.debug(
            "The subscribe_attribute command has been deprecated and will be removed from"
            " a future version. You no longer need to call this to subscribe to attribute changes."
        )

    @api_command(APICommand.PING_NODE)
    async def ping_node(self, node_id: int) -> NodePingResult:
        """Ping node on the currently known IP-adress(es)."""
        result: NodePingResult = {}
        node = self._nodes.get(node_id)
        if node is None:
            raise NodeNotExists(
                f"Node {node_id} does not exist or is not yet interviewed"
            )
        node_logger = LOGGER.getChild(f"[node {node_id}]")

        battery_powered = (
            node.attributes.get(ROUTING_ROLE_ATTRIBUTE_PATH, 0)
            == Clusters.ThreadNetworkDiagnostics.Enums.RoutingRoleEnum.kSleepyEndDevice
        )

        async def _do_ping(ip_address: str) -> None:
            """Ping IP and add to result."""
            timeout = 10 if battery_powered else 2
            if "%" in ip_address:
                # ip address contains an interface index
                clean_ip, interface_idx = ip_address.split("%", 1)
                node_logger.debug(
                    "Pinging address %s (using interface %s)", clean_ip, interface_idx
                )
            else:
                clean_ip = ip_address
                node_logger.debug("Pinging address %s", clean_ip)
            result[clean_ip] = await ping_ip(ip_address, timeout)

        ip_addresses = await self.get_node_ip_addresses(
            node_id, prefer_cache=False, scoped=True
        )
        tasks = [_do_ping(x) for x in ip_addresses]
        # TODO: replace this gather with a taskgroup once we bump our py version
        await asyncio.gather(*tasks)

        # retrieve the currently connected/used address which is used
        # by the sdk for communicating with the device
        if TYPE_CHECKING:
            assert self.chip_controller is not None
        if sdk_result := await self._call_sdk(
            self.chip_controller.GetAddressAndPort, nodeid=node_id
        ):
            active_address = sdk_result[0]
            node_logger.info(
                "The SDK is communicating with the device using %s", active_address
            )
            if active_address not in result and node.available:
                # if the sdk is connected to a node, treat the address as pingable
                result[active_address] = True

        return result

    @api_command(APICommand.GET_NODE_IP_ADRESSES)
    async def get_node_ip_addresses(
        self, node_id: int, prefer_cache: bool = False, scoped: bool = False
    ) -> list[str]:
        """Return the currently known (scoped) IP-adress(es)."""
        cached_info = self._last_known_ip_addresses.get(node_id, [])
        if prefer_cache and cached_info:
            return cached_info if scoped else [x.split("%")[0] for x in cached_info]
        node = self._nodes.get(node_id)
        if node is None:
            raise NodeNotExists(
                f"Node {node_id} does not exist or is not yet interviewed"
            )
        node_logger = LOGGER.getChild(f"[node {node_id}]")
        # query mdns for all IP's
        # ensure both fabric id and node id have 16 characters (prefix with zero's)
        mdns_name = f"{self.compressed_fabric_id:0{16}X}-{node_id:0{16}X}.{MDNS_TYPE_OPERATIONAL_NODE}"
        info = AsyncServiceInfo(MDNS_TYPE_OPERATIONAL_NODE, mdns_name)
        if TYPE_CHECKING:
            assert self._aiozc is not None
        if not await info.async_request(self._aiozc.zeroconf, 3000):
            node_logger.info(
                "Node could not be discovered on the network, returning cached IP's"
            )
            return cached_info
        ip_adresses = info.parsed_scoped_addresses(IPVersion.All)
        # cache this info for later use
        self._last_known_ip_addresses[node_id] = ip_adresses
        return ip_adresses if scoped else [x.split("%")[0] for x in ip_adresses]

    async def _subscribe_node(self, node_id: int) -> None:
        """
        Subscribe to all node state changes/events for an individual node.

        Note that by using the listen command at server level,
        you will receive all (subscribed) node events and attribute updates.
        """
        # pylint: disable=too-many-locals,too-many-statements
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        if self._nodes.get(node_id) is None:
            raise NodeNotExists(
                f"Node {node_id} does not exist or has not been interviewed."
            )

        node_logger = LOGGER.getChild(f"[node {node_id}]")
        node = self._nodes[node_id]

        # check if we already have setup subscriptions for this node,
        # if so, we need to unsubscribe
        if prev_sub := self._subscriptions.get(node_id, None):
            node_logger.info("Unsubscribing from existing subscription.")
            await self._call_sdk(prev_sub.Shutdown)
            del self._subscriptions[node_id]

        # determine if node is battery powered sleeping device
        # Endpoint 0, ThreadNetworkDiagnostics Cluster, routingRole attribute
        battery_powered = (
            node.attributes.get(ROUTING_ROLE_ATTRIBUTE_PATH, 0)
            == Clusters.ThreadNetworkDiagnostics.Enums.RoutingRoleEnum.kSleepyEndDevice
        )

        loop = cast(asyncio.AbstractEventLoop, self.server.loop)

        # set-up the actual subscription

        def attribute_updated_callback(
            path: Attribute.TypedAttributePath,
            transaction: Attribute.SubscriptionTransaction,
        ) -> None:
            self._mdns_last_seen[node_id] = time.time()
            new_value = transaction.GetAttribute(path)
            # failsafe: ignore ValueDecodeErrors
            # these are set by the SDK if parsing the value failed miserably
            if isinstance(new_value, ValueDecodeFailure):
                return

            attr_path = str(path.Path)
            old_value = node.attributes.get(attr_path)

            # return early if the value did not actually change at all
            if old_value == new_value:
                return

            node_logger.debug(
                "Attribute updated: %s - old value: %s - new value: %s",
                path,
                old_value,
                new_value,
            )

            # work out added/removed endpoints on bridges
            if (
                node.is_bridge
                and path.Path.EndpointId == 0
                and path.AttributeType == Clusters.Descriptor.Attributes.PartsList
            ):
                endpoints_removed = set(old_value or []) - set(new_value)
                endpoints_added = set(new_value) - set(old_value or [])
                if endpoints_removed:
                    loop.call_soon_threadsafe(
                        self._handle_endpoints_removed, node_id, endpoints_removed
                    )
                if endpoints_added:
                    loop.create_task(
                        self._handle_endpoints_added(node_id, endpoints_added)
                    )
                return

            # work out if software version changed
            if (
                path.AttributeType == Clusters.BasicInformation.softwareVersion
                and new_value != old_value
            ):
                # schedule a full interview of the node if the software version changed
                loop.create_task(self.interview_node(node_id))

            # store updated value in node attributes
            node.attributes[attr_path] = new_value

            # schedule save to persistent storage
            self._write_node_state(node_id)

            # This callback is running in the CHIP stack thread
            loop.call_soon_threadsafe(
                self.server.signal_event,
                EventType.ATTRIBUTE_UPDATED,
                # send data as tuple[node_id, attribute_path, new_value]
                (node_id, attr_path, new_value),
            )

        def event_callback(
            data: Attribute.EventReadResult,
            transaction: Attribute.SubscriptionTransaction,
        ) -> None:
            # pylint: disable=unused-argument
            assert loop is not None
            node_logger.debug(
                "Received node event: %s - transaction: %s", data, transaction
            )
            node_event = MatterNodeEvent(
                node_id=node_id,
                endpoint_id=data.Header.EndpointId,
                cluster_id=data.Header.ClusterId,
                event_id=data.Header.EventId,
                event_number=data.Header.EventNumber,
                priority=data.Header.Priority,
                timestamp=data.Header.Timestamp,
                timestamp_type=data.Header.TimestampType,
                data=data.Data,
            )
            self.event_history.append(node_event)
            loop.call_soon_threadsafe(
                self.server.signal_event, EventType.NODE_EVENT, node_event
            )

        def error_callback(
            chipError: int, transaction: Attribute.SubscriptionTransaction
        ) -> None:
            # pylint: disable=unused-argument, invalid-name
            node_logger.error("Got error from node: %s", chipError)

        def resubscription_attempted(
            transaction: Attribute.SubscriptionTransaction,
            terminationError: int,
            nextResubscribeIntervalMsec: int,
        ) -> None:
            # pylint: disable=unused-argument, invalid-name
            node_logger.info(
                "Previous subscription failed with Error: %s, re-subscribing in %s ms...",
                terminationError,
                nextResubscribeIntervalMsec,
            )
            resubscription_attempt = self._last_subscription_attempt[node_id] + 1
            self._last_subscription_attempt[node_id] = resubscription_attempt
            # Mark node as unavailable and signal consumers.
            # We debounce it a bit so we only mark the node unavailable
            # after some resubscription attempts and we shutdown the subscription
            # if the resubscription interval exceeds 30 minutes (TTL of mdns).
            # The node will be auto picked up by mdns if it's alive again.
            if (
                node.available
                and resubscription_attempt >= NODE_RESUBSCRIBE_ATTEMPTS_UNAVAILABLE
            ):
                node.available = False
                self.server.signal_event(EventType.NODE_UPDATED, node)
                LOGGER.info("Marked node %s as unavailable", node_id)
            if (
                not node.available
                and nextResubscribeIntervalMsec > NODE_RESUBSCRIBE_TIMEOUT_OFFLINE
            ):
                asyncio.create_task(self._node_offline(node_id))

        def resubscription_succeeded(
            transaction: Attribute.SubscriptionTransaction,
        ) -> None:
            # pylint: disable=unused-argument, invalid-name
            self._mdns_last_seen[node_id] = time.time()
            node_logger.info("Re-Subscription succeeded")
            self._last_subscription_attempt[node_id] = 0
            # mark node as available and signal consumers
            if not node.available:
                node.available = True
                self.server.signal_event(EventType.NODE_UPDATED, node)

        node_logger.info("Setting up attributes and events subscription.")
        interval_floor = 0
        interval_ceiling = (
            NODE_SUBSCRIPTION_CEILING_BATTERY_POWERED
            if battery_powered
            else NODE_SUBSCRIPTION_CEILING
        )
        self._last_subscription_attempt[node_id] = 0
        future = loop.create_future()
        device = await self._resolve_node(node_id)
        Attribute.Read(
            future=future,
            eventLoop=loop,
            device=device.deviceProxy,
            devCtrl=self.chip_controller,
            attributes=[Attribute.AttributePath()],  # wildcard
            events=[
                Attribute.EventPath(EndpointId=None, Cluster=None, Event=None, Urgent=1)
            ],
            returnClusterObject=False,
            subscriptionParameters=Attribute.SubscriptionParameters(
                interval_floor, interval_ceiling
            ),
            # Use fabricfiltered as False to detect changes made by other controllers
            # and to be able to provide a list of all fabrics attached to the device
            fabricFiltered=False,
            autoResubscribe=True,
        ).raise_on_error()
        sub: Attribute.SubscriptionTransaction = await future

        sub.SetAttributeUpdateCallback(attribute_updated_callback)
        sub.SetEventUpdateCallback(event_callback)
        sub.SetErrorCallback(error_callback)
        sub.SetResubscriptionAttemptedCallback(resubscription_attempted)
        sub.SetResubscriptionSucceededCallback(resubscription_succeeded)

        # if we reach this point, it means the node could be resolved
        # and the initial subscription succeeded, mark the node available.
        self._subscriptions[node_id] = sub
        node.available = True
        # update attributes with current state from read request
        # NOTE: Make public method upstream for retrieving the attributeTLVCache
        # pylint: disable=protected-access
        tlv_attributes = sub._readTransaction._cache.attributeTLVCache
        node.attributes.update(parse_attributes_from_read_result(tlv_attributes))
        node_logger.info("Subscription succeeded")
        self._mdns_last_seen[node_id] = time.time()
        self.server.signal_event(EventType.NODE_UPDATED, node)

    def _get_next_node_id(self) -> int:
        """Return next node_id."""
        next_node_id = cast(int, self.server.storage.get(DATA_KEY_LAST_NODE_ID, 0)) + 1
        self.server.storage.set(DATA_KEY_LAST_NODE_ID, next_node_id, force=True)
        return next_node_id

    async def _call_sdk(self, func: Callable[..., _T], *args: Any, **kwargs: Any) -> _T:
        """Call function on the SDK in executor and return result."""
        if self.server.loop is None:
            raise RuntimeError("Server not started.")

        return cast(
            _T,
            await self.server.loop.run_in_executor(
                self._sdk_executor,
                partial(func, *args, **kwargs),
            ),
        )

    async def _setup_node(self, node_id: int) -> None:
        """Handle set-up of subscriptions and interview (if needed) for known/discovered node."""
        if node_id not in self._nodes:
            raise NodeNotExists(f"Node {node_id} does not exist.")
        if node_id in self._nodes_in_setup:
            # prevent duplicate setup actions
            return
        self._nodes_in_setup.add(node_id)
        try:
            # ping the node to out stale mdns reports and to prevent that we
            # send an unreachable node to the sdk which is very slow with resolving it
            # this will also precache the ip addresses of the node for later use.
            ping_result = await self.ping_node(node_id)
            if not any(ping_result.values()):
                LOGGER.warning(
                    "Skip set-up for node %s because it does not appear to be reachable...",
                    node_id,
                )
                return
            LOGGER.info("Setting-up node %s...", node_id)
            # (re)interview node (only) if needed
            node_data = self._nodes[node_id]
            if (
                # re-interview if we dont have any node attributes (empty node)
                not node_data.attributes
                # re-interview if the data model schema has changed
                or node_data.interview_version != DATA_MODEL_SCHEMA_VERSION
            ):
                try:
                    await self.interview_node(node_id)
                except (NodeNotResolving, NodeInterviewFailed) as err:
                    LOGGER.warning("Unable to interview Node %s", exc_info=err)
                    # NOTE: the node will be picked up by mdns discovery automatically
                    # when it comes available again.
                    return
            # setup subscriptions for the node
            try:
                await self._subscribe_node(node_id)
            except NodeNotResolving:
                LOGGER.warning(
                    "Unable to subscribe to Node %s as it is unavailable",
                    node_id,
                )
                # NOTE: the node will be picked up by mdns discovery automatically
                # when it becomes available again.
        finally:
            self._nodes_in_setup.discard(node_id)

    async def _resolve_node(
        self, node_id: int, retries: int = 2, attempt: int = 1
    ) -> DeviceProxyWrapper:
        """Resolve a Node on the network."""
        log_level = logging.DEBUG if attempt == 1 else logging.INFO
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")
        try:
            LOGGER.log(
                log_level,
                "Attempting to resolve node %s... (attempt %s of %s)",
                node_id,
                attempt,
                retries,
            )
            return await self._call_sdk(
                self.chip_controller.GetConnectedDeviceSync,
                nodeid=node_id,
                allowPASE=False,
                timeoutMs=None,
            )
        except (ChipStackError, TimeoutError) as err:
            if attempt >= retries:
                # when we're out of retries, raise NodeNotResolving
                raise NodeNotResolving(f"Unable to resolve Node {node_id}") from err
            await asyncio.sleep(2 + attempt)
            # retry the resolve
            return await self._resolve_node(
                node_id=node_id, retries=retries, attempt=attempt + 1
            )

    def _handle_endpoints_removed(self, node_id: int, endpoints: Iterable[int]) -> None:
        """Handle callback for when bridge endpoint(s) get deleted."""
        node = self._nodes[node_id]
        for endpoint_id in endpoints:
            node.attributes = {
                key: value
                for key, value in node.attributes.items()
                if not key.startswith(f"{endpoint_id}/")
            }
            self.server.signal_event(
                EventType.ENDPOINT_REMOVED,
                {"node_id": node_id, "endpoint_id": endpoint_id},
            )
        # schedule save to persistent storage
        self._write_node_state(node_id)

    async def _handle_endpoints_added(
        self, node_id: int, endpoints: Iterable[int]
    ) -> None:
        """Handle callback for when bridge endpoint(s) get added."""
        # we simply do a full interview of the node
        await self.interview_node(node_id)
        # signal event to consumers
        for endpoint_id in endpoints:
            self.server.signal_event(
                EventType.ENDPOINT_ADDED,
                {"node_id": node_id, "endpoint_id": endpoint_id},
            )

    def _on_mdns_service_state_change(
        self,
        zeroconf: Zeroconf,  # pylint: disable=unused-argument
        service_type: str,
        name: str,
        state_change: ServiceStateChange,
    ) -> None:
        LOGGER.debug("Received %s MDNS event for %s", state_change, name)
        if service_type == MDNS_TYPE_COMMISSIONABLE_NODE:
            asyncio.create_task(
                self._on_mdns_commissionable_node_state(name, state_change)
            )
            return
        if service_type == MDNS_TYPE_OPERATIONAL_NODE:
            self._on_mdns_operational_node_state(name, state_change)

    def _on_mdns_operational_node_state(
        self, name: str, state_change: ServiceStateChange
    ) -> None:
        """Handle a (operational) Matter node MDNS state change."""
        name = name.lower()
        if self.fabric_id_hex not in name:
            # filter out messages that are not for our fabric
            return

        if state_change == ServiceStateChange.Removed:
            # we're not interested in removals as this is already
            # handled in the subscription logic
            return

        # the mdns name is constructed as [fabricid]-[nodeid]._matter._tcp.local.
        # extract the node id from the name
        node_id = int(name.split("-")[1].split(".")[0], 16)

        if not (node := self._nodes.get(node_id)):
            return  # this should not happen, but guard just in case

        # mdns events for matter devices arrive in bursts of (duplicate) messages
        # so we debounce this as we only use the mdns messages for operational node discovery
        # and we have other logic in place to determine node aliveness

        now = time.time()
        last_seen = self._mdns_last_seen.get(node_id, 0)
        self._mdns_last_seen[node_id] = now
        if now - last_seen < NODE_SUBSCRIPTION_CEILING:
            return

        # we treat UPDATE state changes as ADD if the node is marked as
        # unavailable to ensure we catch a node being operational
        if node.available and state_change == ServiceStateChange.Updated:
            return

        if node_id in self._nodes_in_setup:
            # prevent duplicate setup actions
            return
        LOGGER.info("Node %s (re)discovered on MDNS", node_id)
        # setup the node - this will (re) setup the subscriptions etc.
        asyncio.create_task(self._setup_node(node_id))

    async def _on_mdns_commissionable_node_state(
        self, name: str, state_change: ServiceStateChange
    ) -> None:
        """Handle a (commissionable) Matter node MDNS state change."""
        if state_change == ServiceStateChange.Added:
            info = AsyncServiceInfo(MDNS_TYPE_COMMISSIONABLE_NODE, name)
            assert self._aiozc is not None
            await info.async_request(self._aiozc.zeroconf, 3000)
            LOGGER.debug("Discovered commissionable Matter node using MDNS: %s", info)

    def _get_node_lock(self, node_id: int) -> asyncio.Lock:
        """Return lock for given node."""
        if node_id not in self._node_lock:
            self._node_lock[node_id] = asyncio.Lock()
        return self._node_lock[node_id]

    def _write_node_state(self, node_id: int, force: bool = False) -> None:
        """Schedule the write of the current node state to persistent storage."""
        node = self._nodes[node_id]
        self.server.storage.set(
            DATA_KEY_NODES,
            value=dataclass_to_dict(node),
            subkey=str(node_id),
            force=force,
        )

    async def _node_offline(self, node_id: int) -> None:
        """Mark node as offline."""
        # shutdown existing subscriptions
        if sub := self._subscriptions.pop(node_id, None):
            await self._call_sdk(sub.Shutdown)
        # mark node as unavailable (if it wasn't already)
        node = self._nodes[node_id]
        if not node.available:
            return  # nothing to do to
        node.available = False
        self.server.signal_event(EventType.NODE_UPDATED, node)
        LOGGER.info("Marked node %s as offline", node_id)
