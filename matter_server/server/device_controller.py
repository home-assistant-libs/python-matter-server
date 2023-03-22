"""Controller that Manages Matter devices."""

from __future__ import annotations

import asyncio
from collections import deque
from datetime import datetime
from functools import partial
import logging
import pathlib
from typing import TYPE_CHECKING, Any, Callable, Deque, Final, Type, TypeVar, cast

from chip.ChipDeviceCtrl import CommissionableNode
from chip.clusters import Attribute
from chip.clusters.ClusterObjects import ALL_CLUSTERS, Cluster
from chip.exceptions import ChipStackError

from matter_server.server.helpers.paa_certificates import fetch_certificates

from ..common.const import SCHEMA_VERSION
from ..common.errors import (
    NodeCommissionFailed,
    NodeInterviewFailed,
    NodeNotExists,
    NodeNotResolving,
)
from ..common.helpers.api import api_command
from ..common.helpers.util import create_attribute_path, dataclass_from_dict
from ..common.models import APICommand, EventType, MatterNodeData

if TYPE_CHECKING:
    from .server import MatterServer
    from chip.ChipDeviceCtrl import ChipDeviceController

_T = TypeVar("_T")

DATA_KEY_NODES = "nodes"
DATA_KEY_LAST_NODE_ID = "last_node_id"

LOGGER = logging.getLogger(__name__)

# the paa-root-certs path is hardcoded in the sdk at this time
# and always uses the development subfolder
# regardless of anything you pass into instantiating the controller
# revisit this once matter 1.1 is released
PAA_ROOT_CERTS_DIR: Final[pathlib.Path] = (
    pathlib.Path(__file__)
    .parent.resolve()
    .parent.resolve()
    .parent.resolve()
    .joinpath("credentials/development/paa-root-certs")
)


class MatterDeviceController:
    """Class that manages the Matter devices."""
    chip_controller: ChipDeviceController | None

    def __init__(
        self,
        server: MatterServer,
    ):
        """Initialize the device controller."""
        self.server = server
        # Instantiate the underlying ChipDeviceController instance on the Fabric
        assert PAA_ROOT_CERTS_DIR.is_dir()

        # we keep the last events in memory so we can include them in the diagnostics dump
        self.event_history: Deque[Attribute.EventReadResult] = deque(maxlen=25)
        self._subscriptions: dict[int, Attribute.SubscriptionTransaction] = {}
        self._nodes: dict[int, MatterNodeData | None] = {}
        self.wifi_credentials_set: bool = False
        self.thread_credentials_set: bool = False
        self.compressed_fabric_id: int | None = None
        self._interview_task: asyncio.Task | None = None

    async def initialize(self) -> None:
        """Async initialize of controller."""
        # (re)fetch all PAA certificates once at startup
        # NOTE: this must be done before initializing the controller
        asyncio.create_task(fetch_certificates(PAA_ROOT_CERTS_DIR))
        self.chip_controller = self.server.stack.fabric_admin.NewController(
            paaTrustStorePath=str(PAA_ROOT_CERTS_DIR)
        )
        self.compressed_fabric_id = await self._call_sdk(
            self.chip_controller.GetCompressedFabricId
        )
        LOGGER.debug("CHIP Device Controller Initialized")

    async def start(self) -> None:
        """Handle logic on controller start."""
        # load nodes from persistent storage
        nodes: dict[str, dict] = self.server.storage.get(DATA_KEY_NODES, {})
        for node_id_str, node_dict in nodes.items():
            node_id = int(node_id_str)
            # invalidate node data if schema mismatch,
            # the node will automatically be scheduled for re-interview
            if node_dict and node_dict.get("interview_version") != SCHEMA_VERSION:
                node = None
            else:
                node = dataclass_from_dict(MatterNodeData, node_dict)
                # always mark node as unavailable at startup until subscriptions are ready
                node.available = False
            self._nodes[node_id] = node
        # setup subscriptions and (re)interviews as task in the background
        # as we do not want it to block our startup
        self._interview_task = asyncio.create_task(
            self._check_subscriptions_and_interviews()
        )
        LOGGER.debug("Loaded %s nodes", len(self._nodes))

    async def stop(self) -> None:
        """Handle logic on server stop."""
        # unsubscribe all node subscriptions
        for sub in self._subscriptions.values():
            await self._call_sdk(sub.Shutdown)
        self._subscriptions = {}
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
        node = self._nodes.get(node_id)
        assert node is not None, "Node does not exist or is not yet interviewed"
        return node

    @api_command(APICommand.COMMISSION_WITH_CODE)
    async def commission_with_code(self, code: str) -> MatterNodeData:
        """
        Commission a device using QRCode or ManualPairingCode.

        Returns full NodeInfo once complete.
        """
        # perform a quick delta sync of certificates to make sure
        # we have the latest paa root certs
        await fetch_certificates(PAA_ROOT_CERTS_DIR)
        node_id = self._get_next_node_id()

        success = await self._call_sdk(
            self.chip_controller.CommissionWithCode,
            setupPayload=code,
            nodeid=node_id,
        )
        if not success:
            raise NodeCommissionFailed(
                f"Commission with code failed for node {node_id}"
            )

        # full interview of the device
        await self.interview_node(node_id)
        # make sure we start a subscription for this newly added node
        await self.subscribe_node(node_id)
        # return full node object once we're complete
        return self.get_node(node_id)

    @api_command(APICommand.COMMISSION_ON_NETWORK)
    async def commission_on_network(
        self,
        setup_pin_code: int,
        filter_type: int = 0,
        filter: Any = None,  # pylint: disable=redefined-builtin
    ) -> MatterNodeData:
        """
        Commission a device already connected to the network.

        Does the routine for OnNetworkCommissioning, with a filter for mDNS discovery.
        The filter can be an integer,
        a string or None depending on the actual type of selected filter.
        Returns full NodeInfo once complete.
        """
        # perform a quick delta sync of certificates to make sure
        # we have the latest paa root certs
        # NOTE: Its not very clear if the newly fetched certificates can be used without
        # restarting the device controller
        await fetch_certificates(PAA_ROOT_CERTS_DIR)

        node_id = self._get_next_node_id()

        success = await self._call_sdk(
            self.chip_controller.CommissionOnNetwork,
            nodeId=node_id,
            setupPinCode=setup_pin_code,
            filterType=filter_type,
            filter=filter,
        )
        if not success:
            raise NodeCommissionFailed(
                f"Commission on network failed for node {node_id}"
            )

        # full interview of the device
        await self.interview_node(node_id)
        # make sure we start a subscription for this newly added node
        await self.subscribe_node(node_id)
        # return full node object once we're complete
        return self.get_node(node_id)

    @api_command(APICommand.SET_WIFI_CREDENTIALS)
    async def set_wifi_credentials(self, ssid: str, credentials: str) -> None:
        """Set WiFi credentials for commissioning to a (new) device."""
        await self._call_sdk(
            self.chip_controller.SetWiFiCredentials,
            ssid=ssid,
            credentials=credentials,
        )

        self.wifi_credentials_set = True

    @api_command(APICommand.SET_THREAD_DATASET)
    async def set_thread_operational_dataset(self, dataset: str) -> None:
        """Set Thread Operational dataset in the stack."""
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
        option: int = 0,
        discriminator: int | None = None,
    ) -> int:
        """
        Open a commissioning window to commission a device present on this controller to another.

        Returns code to use as discriminator.
        """
        if discriminator is None:
            discriminator = 3840  # TODO generate random one

        await self._call_sdk(
            self.chip_controller.OpenCommissioningWindow,
            nodeid=node_id,
            timeout=timeout,
            iteration=iteration,
            discriminator=discriminator,
            option=option,
        )
        return discriminator

    @api_command(APICommand.DISCOVER)
    async def discover_commissionable_nodes(
        self,
    ) -> CommissionableNode | list[CommissionableNode] | None:
        """Discover Commissionable Nodes (discovered on BLE or mDNS)."""

        result = await self._call_sdk(
            self.chip_controller.DiscoverCommissionableNodes,
        )
        return result

    @api_command(APICommand.INTERVIEW_NODE)
    async def interview_node(self, node_id: int) -> None:
        """Interview a node."""
        LOGGER.debug("Interviewing node: %s", node_id)
        try:
            await self._call_sdk(self.chip_controller.ResolveNode, nodeid=node_id)
            read_response: Attribute.AsyncReadTransaction.ReadResponse = (
                await self.chip_controller.Read(
                    nodeid=node_id, attributes="*", events="*", fabricFiltered=False
                )
            )
        except ChipStackError as err:
            raise NodeInterviewFailed(f"Failed to interview node {node_id}") from err

        is_new_node = node_id not in self._nodes
        existing_info = self._nodes.get(node_id)
        node = MatterNodeData(
            node_id=node_id,
            date_commissioned=existing_info.date_commissioned
            if existing_info
            else datetime.utcnow(),
            last_interview=datetime.utcnow(),
            interview_version=SCHEMA_VERSION,
            attributes=self._parse_attributes_from_read_result(
                read_response.attributes
            ),
        )

        # save updated node data
        self._nodes[node_id] = node
        self.server.storage.set(
            DATA_KEY_NODES,
            subkey=str(node_id),
            value=node,
            force=not existing_info,
        )
        if is_new_node:
            # new node - first interview
            self.server.signal_event(EventType.NODE_ADDED, node)
        else:
            # existing node, signal node updated event
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
        cluster_cls: Cluster = ALL_CLUSTERS[cluster_id]
        command_cls = getattr(cluster_cls.Commands, command_name)
        command = dataclass_from_dict(command_cls, payload)
        return await self.chip_controller.SendCommand(
            nodeid=node_id,
            endpoint=endpoint_id,
            payload=command,
            responseType=response_type,
            timedRequestTimeoutMs=timed_request_timeout_ms,
            interactionTimeoutMs=interaction_timeout_ms,
        )

    @api_command(APICommand.REMOVE_NODE)
    async def remove_node(self, node_id: int) -> None:
        """Remove a Matter node/device from the fabric."""
        if node_id not in self._nodes:
            raise NodeNotExists(
                f"Node {node_id} does not exist or has not been interviewed."
            )
        self._nodes.pop(node_id)
        self.server.storage.remove(
            DATA_KEY_NODES,
            subkey=str(node_id),
        )
        # TODO: Is there functionality to actually reset the device ?
        self.server.signal_event(EventType.NODE_DELETED, node_id)

    async def subscribe_node(self, node_id: int) -> None:
        """
        Subscribe to all node state changes/events for an individual node.

        Note that by using the listen command at server level, you will receive all node events.
        """
        if node_id not in self._nodes:
            raise NodeNotExists(
                f"Node {node_id} does not exist or has not been interviewed."
            )
        assert node_id not in self._subscriptions, "Already subscribed to node"
        node_logger = LOGGER.getChild(str(node_id))
        node_logger.debug("Setting up subscriptions...")

        node = cast(MatterNodeData, self._nodes[node_id])

        try:
            await self._call_sdk(self.chip_controller.ResolveNode, nodeid=node_id)
        except ChipStackError as err:
            node.available = False
            raise NodeNotResolving(f"Failed to resolve node {node_id}") from err

        # we follow the pattern of apple and google here and
        # just do a wildcard subscription for all clusters and properties
        # the client will handle filtering of the events.
        # if it turns out in the future that this is too much traffic (I don't think so now)
        # we can revisit this choice and do some selected subscriptions.
        sub: Attribute.SubscriptionTransaction = await self.chip_controller.Read(
            nodeid=node_id,
            attributes="*",
            events=[("*", 0)],
            reportInterval=(0, 120),
            fabricFiltered=False,
        )

        def attribute_updated_callback(
            path: Attribute.TypedAttributePath,
            transaction: Attribute.SubscriptionTransaction,
        ) -> None:
            assert self.server.loop is not None
            new_value = transaction.GetAttribute(path)
            node_logger.debug("Attribute updated: %s - new value: %s", path, new_value)
            attr_path = str(path.Path)
            node.attributes[attr_path] = new_value

            # schedule save to persistent storage
            self.server.storage.set(
                DATA_KEY_NODES,
                subkey=str(node_id),
                value=node,
            )

            # This callback is running in the CHIP stack thread
            self.server.loop.call_soon_threadsafe(
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
            assert self.server.loop is not None
            node_logger.debug("Received node event: %s", data)
            self.event_history.append(data)
            # TODO: This callback does not seem to fire ever or my test devices do not have events
            self.server.loop.call_soon_threadsafe(
                self.server.signal_event, EventType.NODE_EVENT, data
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
            node_logger.debug(
                "Previous subscription failed with Error: %s, re-subscribing in %s ms...",
                terminationError,
                nextResubscribeIntervalMsec,
            )
            # mark node as unavailable and signal consumers
            if node.available:
                node.available = False
                self.server.signal_event(EventType.NODE_UPDATED, node)

        def resubscription_succeeded(
            transaction: Attribute.SubscriptionTransaction,
        ) -> None:
            # pylint: disable=unused-argument, invalid-name
            node_logger.debug("Re-Subscription succeeded")
            # mark node as available and signal consumers
            if not node.available:
                node.available = True
                self.server.signal_event(EventType.NODE_UPDATED, node)

        sub.SetAttributeUpdateCallback(attribute_updated_callback)
        sub.SetEventUpdateCallback(event_callback)
        sub.SetErrorCallback(error_callback)
        sub.SetResubscriptionAttemptedCallback(resubscription_attempted)
        sub.SetResubscriptionSucceededCallback(resubscription_succeeded)
        self._subscriptions[node_id] = sub
        # if we reach this point, it means the node could be resolved
        # and the initial subscription succeeded, mark the node available.
        node.available = True
        node_logger.debug("Subscription succeeded")
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
                None,
                partial(func, *args, **kwargs),
            ),
        )

    async def _check_subscriptions_and_interviews(self) -> None:
        """Run subscriptions (and interviews) for known nodes."""
        for node_id, node in self._nodes.items():
            # (re)interview node (only) if needed
            if (
                node is None
                or node.interview_version < SCHEMA_VERSION
                or (datetime.utcnow() - node.last_interview).days > 30
            ):
                try:
                    await self.interview_node(node_id)
                except NodeInterviewFailed as err:
                    LOGGER.warning(
                        "Unable to interview Node %s, we will retry later in the background.",
                        node_id,
                        exc_info=err,
                    )
                    continue

            # setup subscriptions for the node
            if node_id in self._subscriptions:
                continue
            try:
                await self.subscribe_node(node_id)
            except NodeNotResolving as err:
                # If the node is unreachable on the network now,
                # it will throw a NodeNotResolving exception, catch this,
                # log this and just try to resolve this node in the next run.
                LOGGER.warning(
                    "Unable to contact Node %s,"
                    " we will retry later in the background.",
                    node_id,
                    exc_info=err,
                )

        # reschedule self to run every hour
        def _schedule() -> None:
            """Schedule task."""
            self._interview_task = asyncio.create_task(
                self._check_subscriptions_and_interviews()
            )

        loop = cast(asyncio.AbstractEventLoop, self.server.loop)
        loop.call_later(3600, _schedule)

    @staticmethod
    def _parse_attributes_from_read_result(
        read_result: dict[int, dict[Type, dict[Type, Any]]]
    ) -> dict[str, Any]:
        """Parse attributes from ReadResult."""
        result = {}
        for endpoint, cluster_dict in read_result.items():
            # read result output is in format
            # {endpoint: {ClusterClass: {AttributeClass: value}}}
            for cluster_cls, attr_dict in cluster_dict.items():
                for attr_cls, attr_value in attr_dict.items():
                    if attr_cls == Attribute.DataVersion:
                        continue
                    # we are only interested in the raw values and let the client
                    # match back from the id's to the correct cluster/attribute classes
                    # attributes are stored in form of AttributePath:
                    # ENDPOINT/CLUSTER_ID/ATTRIBUTE_ID
                    attribute_path = create_attribute_path(
                        endpoint, cluster_cls.id, attr_cls.attribute_id
                    )
                    result[attribute_path] = attr_value
        return result
