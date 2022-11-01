"""Controller that Manages Matter devices."""

from __future__ import annotations

import asyncio
from concurrent import futures
from enum import IntEnum
from functools import partial
import logging
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Final, Optional, cast

from chip.ChipDeviceCtrl import ChipDeviceController
from chip.exceptions import ChipStackError
from chip.discovery import FilterType as DiscoveryFilterType

from ..common.model.message import (
    CommandMessage,
    ErrorResultMessage,
    SubscriptionReportMessage,
    SuccessResultMessage,
)
from ..common.model.server_information import VersionInfo
from .client_handler import COMMANDS

if TYPE_CHECKING:
    from chip.clusters import Attribute

    from .stack import MatterStack
    from .server import MatterServer


class MatterDeviceController:
    """Class that manages the Matter devices."""

    wifi_creds_set = False

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

    @property
    def fabric_id(self) -> int:
        """Return Fabric ID."""
        return self.chip_controller.fabricId

    @property
    def compressed_fabric_id(self) -> int:
        """Return Fabric ID."""
        return self.chip_controller.GetCompressedFabricId()

    async def start(self) -> None:
        """Async initialize of controller."""
        self.logger.debug("Started.")

    async def stop(self) -> None:
        """ "Handle logic on server stop."""
        self.logger.debug("Stopped.")

    @COMMANDS.register("device_controller.CommissionWithCode")
    async def commission_with_code(self, setupPayload: str, nodeid: int) -> bool:
        """
        Commission a device.

        Return boolean if successful.
        """
        assert self.wifi_creds_set, "Received commissioning without Wi-Fi set"

        return await self.server.loop.run_in_executor(
            None,
            partial(
                self.chip_controller.CommissionWithCode,
                setupPayload=setupPayload,
                nodeid=nodeid,
            ),
        )

    @COMMANDS.register("device_controller.CommissionOnNetwork")
    async def commission_on_network(
        self,
        nodeid: int,
        setupPinCode: int,
        filterType: DiscoveryFilterType = DiscoveryFilterType.NONE,
        filter: Any = None,
    ) -> bool:
        """
        Commission a device already connected to the network.

        Does the routine for OnNetworkCommissioning, with a filter for mDNS discovery.
        The filter can be an integer, a string or None depending on the actual type of selected filter.
        Return boolean if successful.
        """
        return await self.server.loop.run_in_executor(
            None,
            partial(
                self.chip_controller.CommissionOnNetwork,
                nodeId=nodeid,
                setupPinCode=setupPinCode,
                filterType=filterType,
                filter=filter,
            ),
        )

    @COMMANDS.register("device_controller.SetWiFiCredentials")
    async def set_wifi_credentials(self, ssid: str, credentials: str) -> bool:
        """Set WiFi credentials for commissioning to a (new) device."""
        error_code = await self.server.loop.run_in_executor(
            None,
            partial(
                self.chip_controller.SetWiFiCredentials,
                ssid=ssid,
                credentials=credentials,
            ),
        )

        if error_code == 0:
            self.wifi_creds_set = True

        return error_code == 0

    @COMMANDS.register("device_controller.SetThreadOperationalDataset")
    async def set_thread_operational_dataset(self, dataset: bytes) -> bool:
        """Set Thread Operational dataset in the stack."""
        error_code = await self.server.loop.run_in_executor(
            None,
            partial(
                self.chip_controller.SetThreadOperationalDataset,
                threadOperationalDataset=dataset,
            ),
        )
        return error_code == 0

    @COMMANDS.register("device_controller.ResolveNode")
    async def resolve_node(self, nodeid: int) -> None:
        """Resolve the DNS-SD name for given Node ID and update address."""
        await self.server.loop.run_in_executor(
            None, partial(self.chip_controller.ResolveNode, nodeid=nodeid)
        )

    class CommissionOption(IntEnum):
        """Enum with available comissioning methodes/options."""

        BASIC = 0
        ENHANCED = 1

    @COMMANDS.register("device_controller.OpenCommissioningWindow")
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

        await self.server.loop.run_in_executor(
            None,
            partial(
                self.chip_controller.OpenCommissioningWindow,
                nodeid=nodeid,
                timeout=timeout,
                iteration=iteration,
                discriminator=discriminator,
                option=option,
            ),
        )
        return discriminator

    @COMMANDS.register("device_controller.SendCommand")
    async def _handle_device_controller_SendCommand(self, msg: CommandMessage):
        result = await self.chip_controller.SendCommand(**msg.args)
        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    async def _handle_device_controller_Unsubscribe(self, msg: CommandMessage):
        """Unsubscribe."""
        subscription = self._subscriptions.pop(msg.args["subscription_id"], None)
        if subscription is None:
            self._send_message(ErrorResultMessage(msg.messageId, "not_found"))
            return

        await self.server.loop.run_in_executor(None, subscription.Shutdown)
        self._send_message(SuccessResultMessage(msg.messageId, None))

    @COMMANDS.register("device_controller.Read")
    async def Read(self, msg: CommandMessage):
        if isinstance(msg.args.get("attributes"), list):
            converted_attributes = []
            for attribute in msg.args["attributes"]:
                if isinstance(attribute, list):
                    converted_attributes.append(tuple(attribute))
                else:
                    converted_attributes.append(attribute)

            msg.args["attributes"] = converted_attributes

        result = await self.chip_controller.Read(**msg.args)

        if msg.args.get("reportInterval") is None:
            self._send_message(SuccessResultMessage(msg.messageId, result))
            return

        self.logger.info("Setting up Subscription for %s", msg.args["attributes"])

        subscription = cast("Attribute.SubscriptionTransaction", result)

        # pylint: disable=protected-access
        subscription_id = subscription._subscriptionId

        # Subscription, we need to keep track on it server side
        def subscription_callback(
            path: Attribute.TypedAttributePath,
            subscription: Attribute.SubscriptionTransaction,
        ):
            data = subscription.GetAttribute(path)
            value = {
                "subscriptionId": subscription_id,
                "fabridId": self.server.stack.fabric_id,
                "nodeid": msg.args["nodeid"],
                "endpoint": path.Path.EndpointId,
                "cluster": path.ClusterType,
                "attribute": path.AttributeName,
                "value": data,
            }
            self.logger.info("subscription_callback %s", value)

            # This callback is running in the CHIP stack thread
            self.server.loop.call_soon_threadsafe(
                self._send_message, SubscriptionReportMessage(subscription_id, value)
            )

        subscription.SetAttributeUpdateCallback(subscription_callback)
        self.logger.info(f"SubscriptionId {subscription_id}")
        self._subscriptions[subscription_id] = subscription
        self._send_message(
            SuccessResultMessage(msg.messageId, {"subscription_id": subscription_id})
        )

    async def _subscribe_node(self, nodeid: int) -> None:
        """Subscribe to all node state changes (wildcard subscription)."""
        assert nodeid not in self._subscriptions, "Already subscribed to this node!"
