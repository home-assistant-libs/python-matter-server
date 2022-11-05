"""Controller that Manages Matter devices."""

from __future__ import annotations

import asyncio
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

from matter_server.server.const import SCHEMA_VERSION

from ..common.helpers.api import api_command
from ..common.helpers.util import dataclass_from_dict, dataclass_to_dict
from ..common.model.error import (
    NodeCommissionFailed,
    NodeInterviewFailed,
    NodeNotExists,
)
from ..common.model.event import EventType
from ..common.model.message import (
    CommandMessage,
    ErrorResultMessage,
    SubscriptionReportMessage,
    SuccessResultMessage,
)

if TYPE_CHECKING:
    from chip.clusters import (
        Attribute,
        Cluster,
        ClusterAttributeDescriptor,
        ClusterEvent,
    )

    from .stack import MatterStack
    from .server import MatterServer

from dataclasses import dataclass, field

DATA_KEY_NODES = "nodes"
DATA_KEY_LAST_NODEID = "last_nodeid"


@dataclass
class MatterNodeData:
    """Representation of a Matter Node."""

    nodeid: int
    date_commissioned: datetime
    last_interview: datetime
    interview_version: int
    attributes: dict[int, dict] = field(default_factory=dict)


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
        self.chip_controller: ChipDeviceController = (
            server.stack.fabric_admin.NewController()
        )
        self.logger.debug("CHIP Device Controller Initialized")
        self._subscriptions: dict[int, Attribute.SubscriptionTransaction] = {}
        self._nodes: dict[int, MatterNodeData] = {}
        self._wifi_creds_set = False

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
        for nodeid_str, node_dict in nodes_data.items():
            nodeid = int(nodeid_str)
            node = dataclass_from_dict(MatterNodeData, node_dict)
            self._nodes[nodeid] = node
            # make sure to start node subscriptions
            await self._subscribe_node(nodeid)
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

    @api_command("device_controller.GetNodes")
    async def get_nodes(self) -> list[MatterNodeData]:
        """Return all Nodes known to the server."""
        return [x for x in self._nodes.values() if x is not None]

    @api_command("device_controller.GetNode")
    async def get_node(self, nodeid: int) -> MatterNodeData:
        """Return info of a single Node."""
        node = self._nodes.get(nodeid)
        assert node is not None, "Node does not exist or is not yet interviewed"
        return node

    @api_command("device_controller.CommissionWithCode")
    async def commission_with_code(self, code: str) -> MatterNodeData:
        """
        Commission a device using QRCode or ManualPairingCode.

        Returns full NodeInfo once complete.
        """
        assert self._wifi_creds_set, "Received commissioning without Wi-Fi set"
        nodeid = self._get_next_nodeid()
        success = await self._call_sdk(
            self.chip_controller.CommissionWithCode,
            setupPayload=code,
            nodeid=nodeid,
        )
        if not success:
            raise NodeCommissionFailed(f"CommissionWithCode failed for node {nodeid}")
        # full interview of the device
        await self.interview_node(nodeid)
        # make sure we start a subscription for this newly added node
        await self._subscribe_node(nodeid)
        # return full node object once we're complete
        return self.get_node(nodeid)

    @api_command("device_controller.CommissionOnNetwork")
    async def commission_on_network(
        self,
        setupPinCode: int,
        filterType: DiscoveryFilterType = DiscoveryFilterType.NONE,
        filter: Any = None,
    ) -> MatterNodeData:
        """
        Commission a device already connected to the network.

        Does the routine for OnNetworkCommissioning, with a filter for mDNS discovery.
        The filter can be an integer, a string or None depending on the actual type of selected filter.
        Returns full NodeInfo once complete.
        """
        nodeid = self._get_next_nodeid()
        success = await self._call_sdk(
            self.chip_controller.CommissionOnNetwork,
            nodeId=nodeid,
            setupPinCode=setupPinCode,
            filterType=filterType,
            filter=filter,
        )
        if not success:
            raise NodeCommissionFailed(f"CommissionWithCode failed for node {nodeid}")
        # full interview of the device
        await self.interview_node(nodeid)
        # make sure we start a subscription for this newly added node
        await self._subscribe_node(nodeid)
        # return full node object once we're complete
        return self.get_node(nodeid)

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
    async def discover_commissionable_nodes(self):
        """DiscoverCommissionableNodes"""

        result = await self._call_sdk(
            self.chip_controller.DiscoverCommissionableNodes,
        )
        return result

    @api_command("device_controller.InterviewNode")
    async def interview_node(self, nodeid: int) -> None:
        """Interview a node."""
        self.logger.debug("Interviewing node: %s", nodeid)
        try:
            await self._call_sdk(self.chip_controller.ResolveNode, nodeid=nodeid)
            read_response: Attribute.AsyncReadTransaction.ReadResponse = (
                await self.chip_controller.Read(
                    nodeid=nodeid, attributes="*", events="*", returnClusterObject=True
                )
            )
        except ChipStackError as err:  # pylint: disable=broad-except
            raise NodeInterviewFailed(f"Failed to interview node {nodeid}") from err

        if nodeid not in self._nodes:
            # new node - first interview
            is_new_node = True
            node_data = MatterNodeData(
                nodeid=nodeid,
                date_commissioned=datetime.utcnow(),
                last_interview=datetime.utcnow(),
                interview_version=SCHEMA_VERSION,
            )
        else:
            node_data = self._nodes.get(nodeid)
            node_data.last_interview = datetime.now()
            node_data.interview_version = SCHEMA_VERSION

        node_data.attributes = read_response.attributes

        # save updated node data
        self._nodes[nodeid] = node_data
        self.server.storage.set(
            DATA_KEY_NODES, subkey=str(nodeid), value=dataclass_to_dict(node_data)
        )

        if is_new_node:
            # new node - first interview
            self.server.signal_event(EventType.NODE_ADDED, node_data)
        else:
            # re interview of existing node
            # TODO: should we compare values to see if something actually changed?
            self.server.signal_event(EventType.NODE_UPDATED, node_data)

        self.logger.debug("Interview of node %s completed", nodeid)

    @api_command("device_controller.SendCommand")
    async def _handle_device_controller_SendCommand(self, msg: CommandMessage):
        result = await self.chip_controller.SendCommand(**msg.args)
        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    async def _subscribe_node(self, nodeid: int) -> None:
        """Subscribe to all node state changes/events."""
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

        def attribute_updated_callback(
            path: Attribute.TypedAttributePath,
            transaction: Attribute.SubscriptionTransaction,
        ):
            data = transaction.GetAttribute(path)
            # value = {
            #     "fabridId": self.server.stack.fabric_id,
            #     "nodeId": msg.args["nodeid"],
            #     "endpoint": path.Path.EndpointId,
            #     "cluster": path.ClusterType,
            #     "attribute": path.AttributeName,
            #     "value": data,
            # }
            self.logger.debug("attribute updated: %s", data)

            # This callback is running in the CHIP stack thread
            self.server.loop.call_soon_threadsafe(
                self.server.signal_event, EventType.NODE_UPDATED
            )

        def event_callback(
            data: Attribute.EventReadResult,
            transaction: Attribute.SubscriptionTransaction,
        ):
            self.logger.debug("event_callback: %s", data)

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
                f"Previous subscription failed with Error: {terminationError} - re-subscribing in {nextResubscribeIntervalMsec}ms..."
            )

        def resubscription_succeeded(transaction: Attribute.SubscriptionTransaction):
            self.logger.debug(f"Subscription succeeded")

        sub.SetAttributeUpdateCallback(attribute_updated_callback)
        sub.SetEventUpdateCallback(event_callback)
        sub.SetErrorCallback(error_callback)
        sub.SetResubscriptionAttemptedCallback(resubscription_attempted)
        sub.SetResubscriptionSucceededCallback()
        self._subscriptions[nodeid] = sub

    def _get_next_nodeid(self) -> int:
        """Return next nodeid."""
        next_nodeid = self.server.storage.get(DATA_KEY_LAST_NODEID, 0) + 1
        self.server.storage.set(DATA_KEY_LAST_NODEID, next_nodeid, force=True)
        self._last_nodeid = next_nodeid
        return next_nodeid

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
            if SCHEMA_VERSION > node.interview_version or (datetime.utcnow() - node.last_interview).days > 30:
                await self.interview_node(node.nodeid)
        # reschedule self to run every hour
        self.server.loop.call_later(
                3600, self.server.loop.create_task, self._check_interviews()
            )
