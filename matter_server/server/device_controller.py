"""Controller that Manages Matter devices."""

from __future__ import annotations

import asyncio
from concurrent import futures
from contextlib import asynccontextmanager
from enum import IntEnum
from functools import partial
import logging
import os
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
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

from matter_server.common.helpers.util import dataclass_from_dict, dataclass_to_dict

from ..common.helpers.api import api_command
from ..common.model.error import InterviewFailed, NodeNotExists
from ..common.model.event import EventType
from ..common.model.message import (
    CommandMessage,
    ErrorResultMessage,
    SubscriptionReportMessage,
    SuccessResultMessage,
)
from ..common.model.server_information import VersionInfo

if TYPE_CHECKING:
    from chip.clusters import (
        Attribute,
        Cluster,
        ClusterAttributeDescriptor,
        ClusterEvent,
    )

    from .stack import MatterStack
    from .server import MatterServer

from dataclasses import dataclass

NODES_DATA_KEY = "nodes"


@dataclass
class MatterNode:
    """Representation of a Matter Node."""

    # root_device_type_instance: MatterDeviceTypeInstance[device_types.RootNode]
    # aggregator_device_type_instance: MatterDeviceTypeInstance[
    #     device_types.Aggregator
    # ] | None = None
    # device_type_instances: list[MatterDeviceTypeInstance]
    # node_devices: list[AbstractMatterNodeDevice]


class CommissionOption(IntEnum):
    """Enum with available comissioning methodes/options."""

    BASIC = 0
    ENHANCED = 1


class MatterDeviceController:
    """Class that manages the Matter devices."""

    def __init__(
        self,
        server: MatterServer,
    ):
        self.server = server
        self.logger = server.logger.getChild("device_controller")
        # Instantiate the underlying ChipDeviceController instance on the Fabric
        root_certs_path = os.path.join(server.storage_path, "paa-root-certs")
        self.chip_controller: ChipDeviceController = (
            server.stack.fabric_admin.NewController()
        )
        self.logger.debug("CHIP Device Controller Initialized")
        self._subscriptions: dict[int, Attribute.SubscriptionTransaction] = {}
        self._nodes: dict[int, MatterNode] = {}
        self._wifi_creds_set = False
        self._commission_lock: asyncio.Lock | None = None
        self._interview_queue = asyncio.Queue()

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
        nodes_data = self.server.storage.get(NODES_DATA_KEY, {})
        for nodeid_str, node_dict in nodes_data.items():
            nodeid = int(nodeid_str)
            self._nodes[nodeid] = dataclass_from_dict(MatterNode, node_dict)
        self.logger.debug("Started.")

    async def stop(self) -> None:
        """ "Handle logic on server stop."""
        await self._call_sdk(self.chip_controller.Shutdown)
        self.logger.debug("Stopped.")

    @api_command("device_controller.GetNodes")
    async def get_nodes(self) -> list[MatterNode]:
        """Return all Nodes known to the server."""
        return [x for x in self._nodes.values() if x is not None]

    @api_command("device_controller.GetNode")
    async def get_node(self, nodeid: int) -> MatterNode:
        """Return info of a single Node."""
        node = self._nodes.get(nodeid)
        assert node is not None, "Node does not exist or is not yet interviewed"
        return node

    @api_command("device_controller.CommissionWithCode")
    async def commission_with_code(
        self, code: str, wait_for_interview: bool = False
    ) -> bool:
        """
        Commission a device.

        Return boolean if successful.
        If `wait_for_interview` is True, it awaits the full interview, otherwise returns early.
        """
        assert self._wifi_creds_set, "Received commissioning without Wi-Fi set"
        async with self._add_node() as next_nodeid:
            success = await self._call_sdk(
                self.chip_controller.CommissionWithCode,
                setupPayload=code,
                nodeid=next_nodeid,
            )
            if success:
                # interview the new node right away and wait for the result
                coro = self._interview_node(next_nodeid)
                if wait_for_interview:
                    await coro
                else:
                    self.server.loop.create_task(coro)
            return success

    @api_command("device_controller.CommissionOnNetwork")
    async def commission_on_network(
        self,
        setupPinCode: int,
        filterType: DiscoveryFilterType = DiscoveryFilterType.NONE,
        filter: Any = None,
        wait_for_interview: bool = False,
    ) -> bool:
        """
        Commission a device already connected to the network.

        Does the routine for OnNetworkCommissioning, with a filter for mDNS discovery.
        The filter can be an integer, a string or None depending on the actual type of selected filter.
        Return boolean if successful.
        If `wait_for_interview` is True, it awaits the full interview, otherwise returns early.
        """
        async with self._add_node() as next_nodeid:
            success = await self._call_sdk(
                self.chip_controller.CommissionOnNetwork,
                nodeId=next_nodeid,
                setupPinCode=setupPinCode,
                filterType=filterType,
                filter=filter,
            )
            if success:
                # interview the new node right away and wait for the result
                coro = self._interview_node(next_nodeid)
                if wait_for_interview:
                    await coro
                else:
                    self.server.loop.create_task(coro)
            return success

    @api_command("device_controller.SetWiFiCredentials")
    async def set_wifi_credentials(self, ssid: str, credentials: str) -> bool:
        """Set WiFi credentials for commissioning to a (new) device."""
        error_code = await self._call_sdk(
            self.chip_controller.SetWiFiCredentials,
            ssid=ssid,
            credentials=credentials,
        )

        self._wifi_creds_set = True
        return error_code == 0

    @api_command("device_controller.SetThreadOperationalDataset")
    async def set_thread_operational_dataset(self, dataset: bytes) -> bool:
        """Set Thread Operational dataset in the stack."""
        error_code = await self._call_sdk(
            self.chip_controller.SetThreadOperationalDataset,
            threadOperationalDataset=dataset,
        )
        return error_code == 0

    @api_command("device_controller.OpenCommissioningWindow")
    async def open_commissioning_window(
        self,
        nodeid: int,
        timeout: int = 300,
        iteration: int = 1000,
        option: CommissionOption = CommissionOption.BASIC,
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
            nodeid=nodeid,
            timeout=timeout,
            iteration=iteration,
            discriminator=discriminator,
            option=option,
        )
        return discriminator

    @api_command("device_controller.DiscoverCommissionableNodes")
    async def discover_commissionable_nodes(
        self):
        """DiscoverCommissionableNodes"""

        result = await self._call_sdk(
            self.chip_controller.DiscoverCommissionableNodes,
        )
        return result

    @api_command("device_controller.SendCommand")
    async def _handle_device_controller_SendCommand(self, msg: CommandMessage):
        result = await self.chip_controller.SendCommand(**msg.args)
        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    async def _interview_node(self, nodeid: int) -> None:
        """Interview a node."""
        if nodeid not in self._nodes:
            raise NodeNotExists(f"Node {nodeid} does not exist.")

        self.logger.debug("Interviewing node: %s", nodeid)
        try:
            await self._call_sdk(self.chip_controller.ResolveNode, nodeid=nodeid)
            node_info = await self.chip_controller.Read(
                nodeid=nodeid, attributes="*", events="*", returnClusterObject=True
            )
        except Exception as err:  # pylint: disable=broad-except
            # TODO: find out what types of exceptions are thrown here
            raise InterviewFailed(f"Failed to interview node {nodeid}") from err

        is_new_node = self._nodes[nodeid] is None
        self._nodes[nodeid] = node_info
        self.server.storage.set(
            NODES_DATA_KEY, str(nodeid), dataclass_to_dict(node_info), immediate=True
        )

        if is_new_node:
            # new node - first interview
            self.server.signal_event(EventType.NODE_ADD_COMPLETE, node_info)
            # make sure we start a subscription for this newly added node
            await self._subscribe_node(nodeid)
        else:
            # re interview of existing node
            # TODO: should we compare values to see if something actually changed?
            self.server.signal_event(EventType.NODE_UPDATED, node_info)

        self.logger.debug("Interview of node %s completed", nodeid)

    async def _subscribe_node(self, nodeid: int) -> None:
        """Subscribe to all node state changes."""
        if nodeid not in self._nodes:
            raise NodeNotExists(f"Node {nodeid} does not exist.")
        assert nodeid not in self._subscriptions, "Already subscribed to node"
        self.logger.debug("Setup subscription for node %s", nodeid)

        await self._call_sdk(self.chip_controller.ResolveNode, nodeid=nodeid)
        # we follow the pattern of apple and google here and
        # just do a wildcard subscription for all clusters and properties
        # the client will handle filtering of the events.
        # if it turns out in the future that this is too much traffic (I don't think so now)
        # we can revisit this choice and so some selected subscriptions.
        sub: Attribute.SubscriptionTransaction = await self.chip_controller.Read(
            nodeid=nodeid, attributes="*", events="*", reportInterval=(0, 120)
        )
        self._subscriptions[nodeid] = sub

        def subscription_callback(
            path: Attribute.TypedAttributePath,
            subscription: Attribute.SubscriptionTransaction,
        ):
            data = subscription.GetAttribute(path)
            # value = {
            #     "subscriptionId": subscription_id,
            #     "fabridId": self.server.stack.fabric_id,
            #     "nodeId": msg.args["nodeid"],
            #     "endpoint": path.Path.EndpointId,
            #     "cluster": path.ClusterType,
            #     "attribute": path.AttributeName,
            #     "value": data,
            # }
            self.logger.info("subscription_callback %s", data)

            # This callback is running in the CHIP stack thread
            self.server.loop.call_soon_threadsafe(
                self.server.signal_event, EventType.NODE_UPDATED
            )

        sub.SetAttributeUpdateCallback(subscription_callback)

    @asynccontextmanager
    async def _add_node(self) -> Generator[int, None, None]:
        """Handle a new node being added."""
        if self._commission_lock is None:
            self._commission_lock = asyncio.Lock()

        async with self._commission_lock:
            # return the next available node id
            if self._nodes:
                next_nodeid = max(x for x in self._nodes) + 1
            else:
                next_nodeid = 4335
            self.server.storage.set(NODES_DATA_KEY, None, str(next_nodeid), force=True)
            self.server.signal_event(EventType.NODE_ADD_PROGRESS, next_nodeid)
            yield next_nodeid

    async def _call_sdk(self, func: Callable, *args, **kwargs) -> Any:
        """Call function on the SDK in executor and return result."""
        return await self.server.loop.run_in_executor(
            None,
            partial(func, *args, **kwargs),
        )
