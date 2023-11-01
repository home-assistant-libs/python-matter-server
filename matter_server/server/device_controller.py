"""Controller that Manages Matter devices."""

from __future__ import annotations

import asyncio
from collections import deque
from datetime import datetime
from functools import partial
import logging
import random
from typing import TYPE_CHECKING, Any, Callable, Iterable, Type, TypeVar, cast

from chip.ChipDeviceCtrl import CommissionableNode
from chip.clusters import Attribute, Objects as Clusters
from chip.clusters.Attribute import ValueDecodeFailure
from chip.clusters.ClusterObjects import (
    ALL_ATTRIBUTES,
    ALL_CLUSTERS,
    Cluster,
    ClusterAttributeDescriptor,
)
from chip.exceptions import ChipStackError

from ..common.const import SCHEMA_VERSION
from ..common.errors import (
    NodeCommissionFailed,
    NodeInterviewFailed,
    NodeNotExists,
    NodeNotResolving,
)
from ..common.helpers.api import api_command
from ..common.helpers.json import json_dumps
from ..common.helpers.util import (
    create_attribute_path,
    create_attribute_path_from_attribute,
    dataclass_from_dict,
    parse_attribute_path,
)
from ..common.models import APICommand, EventType, MatterNodeData, MatterNodeEvent
from .const import PAA_ROOT_CERTS_DIR
from .helpers.paa_certificates import fetch_certificates

if TYPE_CHECKING:
    from chip.ChipDeviceCtrl import ChipDeviceController

    from .server import MatterServer

_T = TypeVar("_T")

DATA_KEY_NODES = "nodes"
DATA_KEY_LAST_NODE_ID = "last_node_id"

LOGGER = logging.getLogger(__name__)
MAX_POLL_INTERVAL = 600

# a list of attributes we should always watch on all nodes
DEFAULT_SUBSCRIBE_ATTRIBUTES: set[tuple[int | str, int | str, int | str]] = {
    ("*", 0x001D, 0x00000000),  # all endpoints, descriptor cluster, deviceTypeList
    ("*", 0x001D, 0x00000003),  # all endpoints, descriptor cluster, partsList
    (0, 0x0028, "*"),  # endpoint 0, BasicInformation cluster, all attributes
    ("*", 0x0039, "*"),  # BridgedDeviceBasicInformation
}


class MatterDeviceController:
    """Class that manages the Matter devices."""

    chip_controller: ChipDeviceController | None

    def __init__(
        self,
        server: MatterServer,
    ):
        """Initialize the device controller."""
        self.server = server
        # we keep the last events in memory so we can include them in the diagnostics dump
        self.event_history: deque[Attribute.EventReadResult] = deque(maxlen=25)
        self._subscriptions: dict[int, Attribute.SubscriptionTransaction] = {}
        self._attr_subscriptions: dict[int, list[tuple[Any, ...]] | str] = {}
        self._resub_debounce_timer: dict[int, asyncio.TimerHandle] = {}
        self._sub_retry_timer: dict[int, asyncio.TimerHandle] = {}
        self._nodes: dict[int, MatterNodeData | None] = {}
        self.wifi_credentials_set: bool = False
        self.thread_credentials_set: bool = False
        self.compressed_fabric_id: int | None = None
        self._resolve_lock: asyncio.Lock = asyncio.Lock()
        self._node_lock: dict[int, asyncio.Lock] = {}

    async def initialize(self) -> None:
        """Async initialize of controller."""
        # (re)fetch all PAA certificates once at startup
        # NOTE: this must be done before initializing the controller
        await fetch_certificates()
        # Instantiate the underlying ChipDeviceController instance on the Fabric
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
            # setup subscription and (re)interview as task in the background
            # as we do not want it to block our startup
            asyncio.create_task(self._check_interview_and_subscription(node_id))
        LOGGER.debug("Loaded %s nodes", len(self._nodes))

    async def stop(self) -> None:
        """Handle logic on server stop."""
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

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
        if node := self._nodes.get(node_id):
            return node
        raise NodeNotExists(f"Node {node_id} does not exist or is not yet interviewed")

    @api_command(APICommand.COMMISSION_WITH_CODE)
    async def commission_with_code(self, code: str) -> MatterNodeData:
        """
        Commission a device using QRCode or ManualPairingCode.

        Returns full NodeInfo once complete.
        """
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        # perform a quick delta sync of certificates to make sure
        # we have the latest paa root certs
        await fetch_certificates()
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
        await self._subscribe_node(node_id)
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
        Do the routine for OnNetworkCommissioning, with a filter for mDNS discovery.

        The filter can be an integer,
        a string or None depending on the actual type of selected filter.

        NOTE: For advanced usecases only, use `commission_with_code`
        for regular commissioning.

        Returns full NodeInfo once complete.
        """
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        # perform a quick delta sync of certificates to make sure
        # we have the latest paa root certs
        # NOTE: Its not very clear if the newly fetched certificates can be used without
        # restarting the device controller
        await fetch_certificates()

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
        await self._subscribe_node(node_id)
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
    ) -> tuple[int, str]:
        """Open a commissioning window to commission a device present on this controller to another.

        Returns code to use as discriminator.
        """
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        if discriminator is None:
            discriminator = 3840  # TODO generate random one

        pin, code = await self._call_sdk(
            self.chip_controller.OpenCommissioningWindow,
            nodeid=node_id,
            timeout=timeout,
            iteration=iteration,
            discriminator=discriminator,
            option=option,
        )
        return pin, code

    @api_command(APICommand.DISCOVER)
    async def discover_commissionable_nodes(
        self,
    ) -> CommissionableNode | list[CommissionableNode] | None:
        """Discover Commissionable Nodes (discovered on BLE or mDNS)."""
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        result = await self._call_sdk(
            self.chip_controller.DiscoverCommissionableNodes,
        )
        return result

    @api_command(APICommand.INTERVIEW_NODE)
    async def interview_node(self, node_id: int) -> None:
        """Interview a node."""
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        LOGGER.debug("Interviewing node: %s", node_id)
        try:
            await self._resolve_node(node_id=node_id)
            async with self._get_node_lock(node_id):
                read_response: Attribute.AsyncReadTransaction.ReadResponse = (
                    await self.chip_controller.Read(
                        nodeid=node_id,
                        attributes="*",
                        fabricFiltered=False,
                    )
                )
        except (ChipStackError, NodeNotResolving) as err:
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

        if existing_info:
            node.attribute_subscriptions = existing_info.attribute_subscriptions
        # work out if the node is a bridge device by looking at the devicetype of endpoint 1
        if attr_data := node.attributes.get("1/29/0"):
            node.is_bridge = any(x.deviceType == 14 for x in attr_data)

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

        cluster_cls: Cluster = ALL_CLUSTERS[cluster_id]
        command_cls = getattr(cluster_cls.Commands, command_name)
        command = dataclass_from_dict(command_cls, payload)
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
        self,
        node_id: int,
        attribute_path: str,
    ) -> Any:
        """Read a single attribute on a node."""
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")
        node_lock = self._get_node_lock(node_id)
        await self._resolve_node(node_id=node_id)
        endpoint_id, cluster_id, attribute_id = parse_attribute_path(attribute_path)
        attribute: Type[ClusterAttributeDescriptor] = ALL_ATTRIBUTES[cluster_id][
            attribute_id
        ]
        async with node_lock:
            result: Attribute.AsyncReadTransaction.ReadResponse = (
                await self.chip_controller.Read(
                    nodeid=node_id,
                    attributes=[(endpoint_id, attribute)],
                    fabricFiltered=False,
                )
            )
            read_atributes = self._parse_attributes_from_read_result(result.attributes)
            return read_atributes.get(attribute_path, None)

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
        endpoint_id, cluster_id, attribute_id = parse_attribute_path(attribute_path)
        attribute = ALL_ATTRIBUTES[cluster_id][attribute_id]()
        attribute.value = value
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

        # pop any existing interview/subscription reschedule timer
        self._sub_retry_timer.pop(node_id, None)

        node = self._nodes.pop(node_id)
        self.server.storage.remove(
            DATA_KEY_NODES,
            subkey=str(node_id),
        )

        assert node is not None

        attribute_path = create_attribute_path_from_attribute(
            0,
            Clusters.OperationalCredentials.Attributes.CurrentFabricIndex,
        )
        fabric_index = node.attributes[attribute_path]

        self.server.signal_event(EventType.NODE_REMOVED, node_id)

        await self.chip_controller.SendCommand(
            nodeid=node_id,
            endpoint=0,
            payload=Clusters.OperationalCredentials.Commands.RemoveFabric(
                fabricIndex=fabric_index,
            ),
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
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")

        if node_id not in self._nodes:
            raise NodeNotExists(
                f"Node {node_id} does not exist or has not been interviewed."
            )

        node = self._nodes[node_id]
        assert node is not None

        # work out added subscriptions
        if not isinstance(attribute_path, list):
            attribute_path = [attribute_path]
        attribute_paths = {parse_attribute_path(x) for x in attribute_path}
        prev_subs = set(node.attribute_subscriptions)
        node.attribute_subscriptions.update(attribute_paths)
        if prev_subs == node.attribute_subscriptions:
            return  # nothing to do
        # save updated node data
        self.server.storage.set(
            DATA_KEY_NODES,
            subkey=str(node_id),
            value=node,
        )

        # (re)setup node subscription
        # this could potentially be called multiple times within a short timeframe
        # so debounce it a bit
        def resubscribe() -> None:
            self._resub_debounce_timer.pop(node_id, None)
            asyncio.create_task(self._subscribe_node(node_id))

        if existing_timer := self._resub_debounce_timer.pop(node_id, None):
            existing_timer.cancel()
        assert self.server.loop is not None
        self._resub_debounce_timer[node_id] = self.server.loop.call_later(
            5, resubscribe
        )

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
        node_lock = self._get_node_lock(node_id)
        node = cast(MatterNodeData, self._nodes[node_id])
        await self._resolve_node(node_id=node_id)

        # work out all (current) attribute subscriptions
        attr_subscriptions: list[Any] = []
        for (
            endpoint_id,
            cluster_id,
            attribute_id,
        ) in set.union(DEFAULT_SUBSCRIBE_ATTRIBUTES, node.attribute_subscriptions):
            endpoint: int | None = None if endpoint_id == "*" else int(endpoint_id)
            cluster: Type[Cluster] = ALL_CLUSTERS[cluster_id]
            attribute: Type[ClusterAttributeDescriptor] | None = (
                None
                if attribute_id == "*"
                else ALL_ATTRIBUTES[cluster_id][attribute_id]
            )
            if endpoint and attribute:
                # Concrete path: specific endpoint, specific clusterattribute
                attr_subscriptions.append((endpoint, attribute))
            elif endpoint and cluster:
                # Specific endpoint, Wildcard attribute id (specific cluster)
                attr_subscriptions.append((endpoint, cluster))
            elif attribute:
                # Wildcard endpoint, specific attribute
                attr_subscriptions.append(attribute)
            elif cluster:
                # Wildcard endpoint, specific cluster
                attr_subscriptions.append(cluster)

        if len(attr_subscriptions) > 9:
            # strictly taken a matter device can only handle 9 individual subscriptions
            # (3 subscriptions of 3 paths per fabric)
            # although the device can probably handle more, we play it safe and opt for
            # wildcard as soon as we have more than 9 paths to watch for.
            attr_subscriptions = "*"  # type: ignore[assignment]

        # check if we already have an subscription for this node,
        # if so, we need to unsubscribe first because a device can only maintain
        # a very limited amount of concurrent subscriptions.
        if prev_sub := self._subscriptions.pop(node_id, None):
            if self._attr_subscriptions.get(node_id) == attr_subscriptions:
                # the current subscription already matches, no need to re-setup
                node_logger.debug("Re-using existing subscription.")
                return
            async with node_lock:
                node_logger.debug("Unsubscribing from existing subscription.")
                await self._call_sdk(prev_sub.Shutdown)

        # determine if node is battery powered sleeping device
        # Endpoint 0, ThreadNetworkDiagnostics Cluster, routingRole attribute
        battery_powered = (
            node.attributes.get("0/53/1", 0)
            == Clusters.ThreadNetworkDiagnostics.Enums.RoutingRoleEnum.kSleepyEndDevice
        )

        self._attr_subscriptions[node_id] = attr_subscriptions
        async with node_lock:
            node_logger.debug("Setting up attributes and events subscription.")
            # Use a report interval of 0, X which means we want to receive state changes
            # as soon as possible (the 0 as floor) but we want to receive a report
            # at least once every X seconds, this is also used to detect the node is still alive.
            # A resubscription will be initiated automatically by the sdk
            # if there was no report within the interval.
            # NOTE 1: The report interval ceiling is subject to a lot of discussion
            # as setting it too low causes a lot of (unneeded) traffic and causes network
            # congestion as well as drains batteries on sleeping devices.
            # Preferred would be to set the interval as high as possible
            # but that would also mean that detecting that a device is offline would be delayed
            # by that amount of time as the interval ceiling also meant as liveness detection.
            # For now we settle on (more or less) 1 minute for mains powered devices,
            # and 1 hour for sleepy devices (to prevent draining the battery), awaiting
            # further discussion about this.
            # see also: https://github.com/project-chip/connectedhomeip/issues/29804
            # NOTE 2: We randomize the interval a bit to prevent all nodes reporting
            # at the exact same time, also causing congestion.
            interval_floor = 0
            interval_ceiling = (
                random.randint(3500, 3600)
                if battery_powered
                else random.randint(40, 70)
            )
            sub: Attribute.SubscriptionTransaction = await self.chip_controller.Read(
                nodeid=node_id,
                attributes=attr_subscriptions,
                # simply subscribe to urgent device events only (e.g. button press etc.)
                # non urgent events are diagnostic reports etc. for which we have no usecase (yet).
                events=[("*", 1)],
                reportInterval=(interval_floor, interval_ceiling),
                # Use fabricfiltered as False to detect changes made by other controllers
                # and to be able to provide a list of all fabrics attached to the device
                fabricFiltered=False,
            )

        def attribute_updated_callback(
            path: Attribute.TypedAttributePath,
            transaction: Attribute.SubscriptionTransaction,
        ) -> None:
            assert self.server.loop is not None
            new_value = transaction.GetAttribute(path)
            # failsafe: ignore ValueDecodeErrors
            # these are set by the SDK if parsing the value failed miserably
            if isinstance(new_value, ValueDecodeFailure):
                return

            attr_path = str(path.Path)
            old_value = node.attributes.get(attr_path)

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
                    self.server.loop.call_soon_threadsafe(
                        self._handle_endpoints_removed, node_id, endpoints_removed
                    )
                if endpoints_added:
                    self.server.loop.create_task(
                        self._handle_endpoints_added(node_id, endpoints_added)
                    )
                return

            # work out if software version changed
            if (
                path.AttributeType == Clusters.BasicInformation.softwareVersion
                and new_value != old_value
            ):
                # schedule a full interview of the node if the software version changed
                self.server.loop.create_task(self.interview_node(node_id))

            # store updated value in node attributes
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
            self.server.loop.call_soon_threadsafe(
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
            # mark node as unavailable and signal consumers
            if node.available:
                node.available = False
                self.server.signal_event(EventType.NODE_UPDATED, node)
            if nextResubscribeIntervalMsec / 1000 > MAX_POLL_INTERVAL:
                # workaround to handle devices that are unplugged
                # from power for a longer period of time
                # where the sdk is extending the poll timeout at every attempt
                # until even 1,5 hours which is way too long.
                # instead a device back alive should be detected using mDNS,
                # which is not yet implemented in the core sdk.
                # For now, we just override the timeout.
                # NOTE 1: fix this once OperationalNodeDiscovery is available:
                # https://github.com/project-chip/connectedhomeip/pull/26718
                # https://github.com/project-chip/connectedhomeip/issues/29663
                # NOTE 2: We could also just implement zeroconf/mdns ourselves
                # to listen for the announcements.
                sub.OverrideLivenessTimeoutMs(MAX_POLL_INTERVAL * 1000)

        def resubscription_succeeded(
            transaction: Attribute.SubscriptionTransaction,
        ) -> None:
            # pylint: disable=unused-argument, invalid-name
            node_logger.info("Re-Subscription succeeded")
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
        node_logger.info("Subscription succeeded")
        # update attributes with current state from read request
        current_atributes = self._parse_attributes_from_read_result(sub.GetAttributes())
        node.attributes.update(current_atributes)
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

    async def _check_interview_and_subscription(
        self, node_id: int, reschedule_interval: int = 30
    ) -> None:
        """Handle interview (if needed) and subscription for known node."""

        if node_id not in self._nodes:
            raise NodeNotExists(f"Node {node_id} does not exist.")

        # pop any existing reschedule timer
        self._sub_retry_timer.pop(node_id, None)

        def reschedule() -> None:
            """(Re)Schedule interview and/or initial subscription for a node."""
            assert self.server.loop is not None
            self._sub_retry_timer[node_id] = self.server.loop.call_later(
                reschedule_interval,
                asyncio.create_task,
                self._check_interview_and_subscription(
                    node_id,
                    # increase interval at each attempt with maximum of
                    # MAX_POLL_INTERVAL seconds (= 10 minutes)
                    min(reschedule_interval + 10, MAX_POLL_INTERVAL),
                ),
            )

        # (re)interview node (only) if needed
        node_data = self._nodes.get(node_id)
        if (
            node_data is None
            # re-interview if the schema has changed
            or node_data.interview_version < SCHEMA_VERSION
        ):
            try:
                await self.interview_node(node_id)
            except NodeInterviewFailed:
                LOGGER.warning(
                    "Unable to interview Node %s, will retry later in the background.",
                    node_id,
                )
                # reschedule self on error
                reschedule()
                return

        # setup subscriptions for the node
        if node_id in self._subscriptions:
            return

        try:
            await self._subscribe_node(node_id)
        except NodeNotResolving:
            LOGGER.warning(
                "Unable to subscribe to Node %s as it is unavailable, "
                "will retry later in the background.",
                node_id,
            )
            # TODO: fix this once OperationalNodeDiscovery is available:
            # https://github.com/project-chip/connectedhomeip/pull/26718
            reschedule()

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
                    # failsafe: ignore ValueDecodeErrors
                    # these are set by the SDK if parsing the value failed miserably
                    if isinstance(attr_value, ValueDecodeFailure):
                        continue
                    # failsafe: make sure the attribute is serializable
                    # there is a chance we receive malformed data from the sdk
                    # due to all magic parsing to/from TLV.
                    # skip an attribute in that case to prevent serialization issues
                    # of the whole node.
                    try:
                        json_dumps(attr_value)
                    except TypeError as err:
                        LOGGER.warning(
                            "Unserializable data found - "
                            "skip attribute %s - error details: %s",
                            attribute_path,
                            err,
                        )
                        continue
                    result[attribute_path] = attr_value
        return result

    async def _resolve_node(self, node_id: int, retries: int = 3) -> None:
        """Resolve a Node on the network."""
        if (node := self._nodes.get(node_id)) and node.available:
            # no need to resolve, the node is already available/connected
            return

        node_lock = self._get_node_lock(node_id)
        if self.chip_controller is None:
            raise RuntimeError("Device Controller not initialized.")
        try:
            # the sdk crashes when multiple resolves happen at the same time
            # guard simultane resolves with a lock.
            async with node_lock, self._resolve_lock:
                LOGGER.debug("Attempting to resolve node %s...", node_id)
                await self._call_sdk(
                    self.chip_controller.ResolveNode,
                    nodeid=node_id,
                )
        except (ChipStackError, TimeoutError) as err:
            if retries <= 1:
                # when we're out of retries, raise NodeNotResolving
                raise NodeNotResolving(f"Unable to resolve Node {node_id}") from err
            await self._resolve_node(node_id=node_id, retries=retries - 1)
            await asyncio.sleep(2)

    def _handle_endpoints_removed(self, node_id: int, endpoints: Iterable[int]) -> None:
        """Handle callback for when bridge endpoint(s) get deleted."""
        node = cast(MatterNodeData, self._nodes[node_id])
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
        self.server.storage.set(
            DATA_KEY_NODES,
            subkey=str(node_id),
            value=node,
        )

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

    def _get_node_lock(self, node_id: int) -> asyncio.Lock:
        """Return lock for given node."""
        if node_id not in self._node_lock:
            self._node_lock[node_id] = asyncio.Lock()
        return self._node_lock[node_id]
