"""Controller that Manages Matter devices."""

from __future__ import annotations

import asyncio
from collections import deque
from concurrent import futures
from datetime import datetime
from enum import IntEnum
from functools import partial
import logging
import os
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Deque,
    Final,
    Generator,
    List,
    Optional,
    Tuple,
    Type,
    Union,
    cast,
)

from chip.ChipDeviceCtrl import ChipDeviceController
from chip.discovery import FilterType as DiscoveryFilterType
from chip.exceptions import ChipStackError

from ..common.helpers.api import api_command
from ..common.helpers.util import dataclass_from_dict, dataclass_to_dict
from ..common.models.api_command import APICommand
from ..common.models.error import (
    NodeCommissionFailed,
    NodeInterviewFailed,
    NodeNotExists,
    SDKCommandFailed,
)
from ..common.models.events import EventType
from ..common.models.message import (
    CommandMessage,
    ErrorResultMessage,
    SuccessResultMessage,
)
from ..common.models.node import MatterNode
from .const import SCHEMA_VERSION

if TYPE_CHECKING:
    from chip.clusters import (
        Attribute,
        Cluster,
        ClusterAttributeDescriptor,
        ClusterCommand,
        ClusterEvent,
    )

    from .server import MatterServer
    from .stack import MatterStack


DATA_KEY_NODES = "nodes"
DATA_KEY_LAST_NODE_ID = "last_node_id"


class MatterDeviceController:
    """Class that manages the Matter devices."""

    def __init__(
        self,
        server: MatterServer,
    ):
        self.server = server
        self.logger = server.logger.getChild("device_controller")
        # Instantiate the underlying ChipDeviceController instance on the Fabric
        self.chip_controller: ChipDeviceController = (
            server.stack.fabric_admin.NewController()
        )
        # we keep the last events in memory so we can include them in the diagnostics dump
        self.event_history: Deque[Attribute.EventReadResult] = deque(maxlen=25)
        self._subscriptions: dict[int, Attribute.SubscriptionTransaction] = {}
        self._nodes: dict[int, MatterNode] = {}
        self._wifi_creds_set = False
        self.logger.debug("CHIP Device Controller Initialized")

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
            # TEMP !!!! TODO
            # node_dict["attributes"] = {}
            node = dataclass_from_dict(MatterNode, node_dict)
            self._nodes[node_id] = node
            # make sure to start node subscriptions
            await self.subscribe_node(node_id)
        # create task to check for nodes that need any re(interviews)
        self.server.loop.create_task(self._check_interviews())
        self.logger.debug("Started.")

    async def stop(self) -> None:
        """ "Handle logic on server stop."""
        # unsubscribe all node subscriptions
        for sub in self._subscriptions.values():
            await self._call_sdk(sub.Shutdown)
        self._subscriptions = {}
        await self._call_sdk(self.chip_controller.Shutdown)
        self.logger.debug("Stopped.")

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
        assert self._wifi_creds_set, "Received commissioning without Wi-Fi set"
        node_id = self._get_next_node_id()
        success = await self._call_sdk(
            self.chip_controller.CommissionWithCode,
            setupPayload=code,
            nodeid=node_id,
        )

        # TODO TEMP !!!
        # The call to CommissionWithCode returns early without waiting ?!
        # if not success:
        #     raise NodeCommissionFailed(f"CommissionWithCode failed for node {node_id}")
        await asyncio.sleep(120)

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
        filter_type: DiscoveryFilterType = DiscoveryFilterType.NONE,
        filter: Any = None,
    ) -> MatterNode:
        """
        Commission a device already connected to the network.

        Does the routine for OnNetworkCommissioning, with a filter for mDNS discovery.
        The filter can be an integer, a string or None depending on the actual type of selected filter.
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

        self._wifi_creds_set = True
        if error_code != 0:
            raise SDKCommandFailed("Set WiFi credentials failed.")

    @api_command(APICommand.SET_THREAD_DATASET)
    async def set_thread_operational_dataset(self, dataset: str) -> None:
        """Set Thread Operational dataset in the stack."""
        error_code = await self._call_sdk(
            self.chip_controller.SetThreadOperationalDataset,
            threadOperationalDataset=bytes.fromhex(dataset),
        )
        if error_code != 0:
            raise SDKCommandFailed("Set Thread credentials failed.")

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
        self.logger.debug("Interviewing node: %s", node_id)
        try:
            await self._call_sdk(self.chip_controller.ResolveNode, nodeid=node_id)
            read_response: Attribute.AsyncReadTransaction.ReadResponse = (
                await self.chip_controller.Read(
                    nodeid=node_id, attributes="*", events="*", returnClusterObject=True
                )
            )
        except ChipStackError as err:
            raise NodeInterviewFailed(f"Failed to interview node {node_id}") from err

        existing_info = self._nodes.get(node_id)
        node = MatterNode(
            nodeid=node_id,
            date_commissioned=existing_info.date_commissioned
            if existing_info
            else datetime.utcnow(),
            last_interview=datetime.utcnow(),
            interview_version=SCHEMA_VERSION,
        )
        node.parse_attributes(read_response.attributes)

        # save updated node data
        self._nodes[node_id] = node
        node_dict = dataclass_to_dict(node)
        self.server.storage.set(
            DATA_KEY_NODES,
            subkey=str(node_id),
            value=node_dict,
            force=not existing_info,
        )
        if existing_info is None:
            # new node - first interview
            self.server.signal_event(EventType.NODE_ADDED, node)
        else:
            # re interview of existing node
            self.server.signal_event(EventType.NODE_UPDATED, node)

        self.logger.debug("Interview of node %s completed", node_id)

    @api_command(APICommand.DEVICE_COMMAND)
    async def send_device_command(
        self, node_id: int, endpoint: int, payload: ClusterCommand
    ) -> Any:
        """Send a command to a Matter node/device."""
        return await self.chip_controller.SendCommand(
            nodeid=node_id, endpoint=endpoint, payload=payload
        )

    async def subscribe_node(self, node_id: int) -> None:
        """
        Subscribe to all node state changes/events for an individual node.

        Note that by using the listen command at server level, you will receive all node events.
        """
        if node_id not in self._nodes:
            raise NodeNotExists(f"Node {node_id} does not exist.")
        assert node_id not in self._subscriptions, "Already subscribed to node"
        self.logger.debug("Setup subscription for node %s", node_id)

        await self._call_sdk(self.chip_controller.ResolveNode, nodeid=node_id)
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
            data = transaction.GetAttribute(path)
            # value = {
            #     "fabridId": self.server.stack.fabric_id,
            #     "nodeId": msg.args["node_id"],
            #     "endpoint": path.Path.EndpointId,
            #     "cluster": path.ClusterType,
            #     "attribute": path.AttributeName,
            #     "value": data,
            # }
            self.logger.debug(
                "attribute updated - path: %s - transaction: %s - data: %s",
                path,
                transaction,
                data,
            )

            # This callback is running in the CHIP stack thread
            self.server.loop.call_soon_threadsafe(
                self.server.signal_event, EventType.NODE_UPDATED
            )

        def event_callback(
            data: Attribute.EventReadResult,
            transaction: Attribute.SubscriptionTransaction,
        ):
            self.logger.debug("event_callback: %s", data)
            self.event_history.append(data)
            # TODO: forward event

        def error_callback(
            chipError: int, transaction: Attribute.SubscriptionTransaction
        ):
            self.logger.debug("error_callback: %s", chipError)

        def resubscription_attempted(
            transaction: Attribute.SubscriptionTransaction,
            terminationError: int,
            nextResubscribeIntervalMsec: int,
        ):
            self.logger.debug(
                "Previous subscription failed with Error: %s - re-subscribing in %s ms...",
                terminationError,
                nextResubscribeIntervalMsec,
            )

        def resubscription_succeeded(transaction: Attribute.SubscriptionTransaction):
            self.logger.debug(f"Subscription succeeded")

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
        self._last_nodeid = next_node_id
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
