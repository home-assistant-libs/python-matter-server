"""Controller that Manages Matter devices."""

from __future__ import annotations

import asyncio
from collections import deque
from datetime import datetime
from functools import partial
import logging
from typing import TYPE_CHECKING, Any, Callable, Deque, Optional, Type

from chip.ChipDeviceCtrl import ChipDeviceController
from chip.clusters import Attribute, ClusterCommand
from chip.exceptions import ChipStackError

from ..common.helpers.api import api_command
from ..common.helpers.util import dataclass_from_dict
from ..common.models.api_command import APICommand
from ..common.models.error import (
    NodeCommissionFailed,
    NodeInterviewFailed,
    NodeNotExists,
    NodeNotResolving,
    SDKCommandFailed,
)
from ..common.models.events import EventType
from ..common.models.node import MatterAttribute, MatterNode
from .const import SCHEMA_VERSION

if TYPE_CHECKING:

    from .server import MatterServer

DATA_KEY_NODES = "nodes"
DATA_KEY_LAST_NODE_ID = "last_node_id"

LOGGER = logging.getLogger(__name__)


class MatterDeviceController:
    """Class that manages the Matter devices."""

    def __init__(
        self,
        server: MatterServer,
    ):
        self.server = server
        # Instantiate the underlying ChipDeviceController instance on the Fabric
        self.chip_controller: ChipDeviceController = (
            server.stack.fabric_admin.NewController()
        )
        # we keep the last events in memory so we can include them in the diagnostics dump
        self.event_history: Deque[Attribute.EventReadResult] = deque(maxlen=25)
        self._subscriptions: dict[int, Attribute.SubscriptionTransaction] = {}
        self._nodes: dict[int, MatterNode] = {}
        self.wifi_credentials_set: bool = False
        self.thread_credentials_set: bool = False

    @property
    def fabric_id(self) -> int:
        """Return Fabric ID."""
        return self.chip_controller.fabricId

    @property
    def compressed_fabric_id(self) -> int:
        """Return unique identifier for this initialized fabric."""
        return self.chip_controller.GetCompressedFabricId()

    async def start(self) -> None:
        """Async initialize of controller."""
        # load nodes from persistent storage
        nodes_data = self.server.storage.get(DATA_KEY_NODES, {})
        for node_id_str, node_dict in nodes_data.items():
            node_id = int(node_id_str)
            node = dataclass_from_dict(MatterNode, node_dict)
            self._nodes[node_id] = node
            # make sure to start node subscriptions
            try:
                await self.subscribe_node(node_id)
            except NodeNotResolving:
                LOGGER.warning("Node %s is not resolving, skipping...", node_id)
        # create task to check for nodes that need any re(interviews)
        self.server.loop.create_task(self._check_interviews())
        LOGGER.debug("CHIP Device Controller Initialized")

    async def stop(self) -> None:
        """ "Handle logic on server stop."""
        # unsubscribe all node subscriptions
        for sub in self._subscriptions.values():
            await self._call_sdk(sub.Shutdown)
        self._subscriptions = {}
        await self._call_sdk(self.chip_controller.Shutdown)
        LOGGER.debug("Stopped.")

    @api_command(APICommand.GET_NODES)
    def get_nodes(self) -> list[MatterNode]:
        """Return all Nodes known to the server."""
        return [x for x in self._nodes.values() if x is not None]

    @api_command(APICommand.GET_NODE)
    def get_node(self, node_id: int) -> MatterNode:
        """Return info of a single Node."""
        node = self._nodes.get(node_id)
        assert node is not None, "Node does not exist or is not yet interviewed"
        return node

    @api_command(APICommand.COMMISSION_WITH_CODE)
    async def commission_with_code(self, code: str) -> MatterNode:
        """
        Commission a device using QRCode or ManualPairingCode.

        Returns full NodeInfo once complete.
        """
        node_id = self._get_next_node_id()

        # TODO TEMP !!!
        # The call to CommissionWithCode returns early without waiting ?!
        # This is most likely a bug in the SDK or its python wrapper
        # success = await self._call_sdk(
        #     self.chip_controller.CommissionWithCode,
        #     setupPayload=code,
        #     nodeid=node_id,
        # )
        # if not success:
        #     raise NodeCommissionFailed(f"CommissionWithCode failed for node {node_id}")
        await self._call_sdk(
            self.chip_controller.CommissionWithCode,
            setupPayload=code,
            nodeid=node_id,
        )
        await asyncio.sleep(60)

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
    ) -> MatterNode:
        """
        Commission a device already connected to the network.

        Does the routine for OnNetworkCommissioning, with a filter for mDNS discovery.
        The filter can be an integer,
        a string or None depending on the actual type of selected filter.
        Returns full NodeInfo once complete.
        """
        node_id = self._get_next_node_id()
        success = await self._call_sdk(
            self.chip_controller.CommissionOnNetwork,
            nodeId=node_id,
            setupPinCode=setup_pin_code,
            filterType=filter_type,
            filter=filter,
        )
        if not success:
            raise NodeCommissionFailed(f"CommissionWithCode failed for node {node_id}")
        # full interview of the device
        await self.interview_node(node_id)
        # make sure we start a subscription for this newly added node
        await self.subscribe_node(node_id)
        # return full node object once we're complete
        return self.get_node(node_id)

    @api_command(APICommand.SET_WIFI_CREDENTIALS)
    async def set_wifi_credentials(self, ssid: str, credentials: str) -> None:
        """Set WiFi credentials for commissioning to a (new) device."""
        error_code = await self._call_sdk(
            self.chip_controller.SetWiFiCredentials,
            ssid=ssid,
            credentials=credentials,
        )

        if error_code != 0:
            raise SDKCommandFailed("Set WiFi credentials failed.")
        self.wifi_credentials_set = True

    @api_command(APICommand.SET_THREAD_DATASET)
    async def set_thread_operational_dataset(self, dataset: str) -> None:
        """Set Thread Operational dataset in the stack."""
        error_code = await self._call_sdk(
            self.chip_controller.SetThreadOperationalDataset,
            threadOperationalDataset=bytes.fromhex(dataset),
        )

        if error_code != 0:
            raise SDKCommandFailed("Set Thread credentials failed.")
        self.thread_credentials_set = True

    @api_command(APICommand.OPEN_COMMISSIONING_WINDOW)
    async def open_commissioning_window(
        self,
        node_id: int,
        timeout: int = 300,
        iteration: int = 1000,
        option: int = 0,
        discriminator: Optional[int] = None,
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
    async def discover_commissionable_nodes(self):
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
                    nodeid=node_id, attributes="*", events="*"
                )
            )
        except ChipStackError as err:
            raise NodeInterviewFailed(f"Failed to interview node {node_id}") from err

        existing_info = self._nodes.get(node_id)
        node = MatterNode(
            node_id=node_id,
            date_commissioned=existing_info.date_commissioned
            if existing_info
            else datetime.utcnow(),
            last_interview=datetime.utcnow(),
            interview_version=SCHEMA_VERSION,
            attributes=self._parse_attributes_from_read_result(
                node_id, read_response.attributes
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
        if existing_info is None:
            # new node - first interview
            self.server.signal_event(EventType.NODE_ADDED, node)

        LOGGER.debug("Interview of node %s completed", node_id)

    @api_command(APICommand.DEVICE_COMMAND)
    async def send_device_command(
        self, node_id: int, endpoint: int, payload: ClusterCommand
    ) -> Any:
        """Send a command to a Matter node/device."""
        return await self.chip_controller.SendCommand(
            nodeid=node_id, endpoint=endpoint, payload=payload
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
        LOGGER.debug("Setup subscription for node %s", node_id)

        try:
            await self._call_sdk(self.chip_controller.ResolveNode, nodeid=node_id)
        except ChipStackError as err:
            raise NodeNotResolving(f"Failed to resolve node {node_id}") from err
        # we follow the pattern of apple and google here and
        # just do a wildcard subscription for all clusters and properties
        # the client will handle filtering of the events.
        # if it turns out in the future that this is too much traffic (I don't think so now)
        # we can revisit this choice and do some selected subscriptions.
        sub: Attribute.SubscriptionTransaction = await self.chip_controller.Read(
            nodeid=node_id, attributes="*", events="*", reportInterval=(0, 10)
        )

        def attribute_updated_callback(
            path: Attribute.TypedAttributePath,
            transaction: Attribute.SubscriptionTransaction,
        ):
            new_value = transaction.GetAttribute(path)
            LOGGER.debug("attribute updated -- %s - new value: %s", path, new_value)
            node = self._nodes[node_id]
            attr = node.attributes[str(path.Path)]
            attr.value = new_value

            # schedule save to persistent storage
            self.server.storage.set(
                DATA_KEY_NODES,
                subkey=str(node_id),
                value=node,
            )

            # This callback is running in the CHIP stack thread
            self.server.loop.call_soon_threadsafe(
                self.server.signal_event, EventType.ATTRIBUTE_UPDATED, attr
            )

        def event_callback(
            data: Attribute.EventReadResult,
            transaction: Attribute.SubscriptionTransaction,
        ):
            # pylint: disable=unused-argument
            LOGGER.debug("received node event: %s", data)
            self.event_history.append(data)
            # TODO: This callback does not seem to fire ever or my test devices do not have events
            self.server.loop.call_soon_threadsafe(
                self.server.signal_event, EventType.NODE_EVENT, data
            )

        def error_callback(
            chipError: int, transaction: Attribute.SubscriptionTransaction
        ):
            # pylint: disable=unused-argument, invalid-name
            LOGGER.error("Got error fron node: %s", chipError)

        def resubscription_attempted(
            transaction: Attribute.SubscriptionTransaction,
            terminationError: int,
            nextResubscribeIntervalMsec: int,
        ):
            # pylint: disable=unused-argument, invalid-name
            LOGGER.debug(
                "Previous subscription failed with Error: %s - re-subscribing in %s ms...",
                terminationError,
                nextResubscribeIntervalMsec,
            )
            # TODO: update node status to unavailable

        def resubscription_succeeded(transaction: Attribute.SubscriptionTransaction):
            # pylint: disable=unused-argument, invalid-name
            LOGGER.debug("Subscription succeeded")
            # TODO: update node status to available

        sub.SetAttributeUpdateCallback(attribute_updated_callback)
        sub.SetEventUpdateCallback(event_callback)
        sub.SetErrorCallback(error_callback)
        sub.SetResubscriptionAttemptedCallback(resubscription_attempted)
        sub.SetResubscriptionSucceededCallback(resubscription_succeeded)
        self._subscriptions[node_id] = sub

    def _get_next_node_id(self) -> int:
        """Return next node_id."""
        next_node_id = self.server.storage.get(DATA_KEY_LAST_NODE_ID, 0) + 1
        self.server.storage.set(DATA_KEY_LAST_NODE_ID, next_node_id, force=True)
        return next_node_id

    async def _call_sdk(self, func: Callable, *args, **kwargs) -> Any:
        """Call function on the SDK in executor and return result."""
        return await self.server.loop.run_in_executor(
            None,
            partial(func, *args, **kwargs),
        )

    async def _check_interviews(self) -> None:
        """Check if any nodes need to be (re)interviewed."""
        # Reinterview all nodes that have an outdated schema
        # and/or have been interviewed more than 30 days ago.
        for node in self._nodes.values():
            if (
                SCHEMA_VERSION > node.interview_version
                or (datetime.utcnow() - node.last_interview).days > 30
            ):
                await self.interview_node(node.node_id)
        # reschedule self to run every hour
        self.server.loop.call_later(
            3600, self.server.loop.create_task, self._check_interviews()
        )

    @staticmethod
    def _parse_attributes_from_read_result(
        node_id: int, attributes: dict[int, dict[Type, dict[Type, Any]]]
    ) -> dict[int, MatterAttribute]:
        """Parse attributes from ReadResult."""
        result = {}
        for endpoint, cluster_dict in attributes.items():
            # read result output is in format {endpoint: {ClusterClass: {AttributeClass: value}}}
            # we parse this to our own much more useable format
            for cluster_cls, attr_dict in cluster_dict.items():
                for attr_cls, attr_value in attr_dict.items():
                    if attr_cls == Attribute.DataVersion:
                        continue
                    attr = MatterAttribute(
                        node_id=node_id,
                        endpoint=endpoint,
                        cluster_id=cluster_cls.id,
                        cluster_type=cluster_cls,
                        cluster_name=cluster_cls.__name__,
                        attribute_id=attr_cls.attribute_id,
                        attribute_type=attr_cls,
                        attribute_name=attr_cls.__name__,
                        value=attr_value,
                    )
                    result[attr.path] = attr
        return result
