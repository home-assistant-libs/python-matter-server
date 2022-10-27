"""Controller that Manages Matter devices."""

from __future__ import annotations

import asyncio
from concurrent import futures
from functools import partial
import logging
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Final, cast

from chip.exceptions import ChipStackError

# NOTE: import the ChipDeviceController here to prevent circular import issues
from chip.ChipDeviceCtrl import ChipDeviceController, DiscoveryFilterType


from ..common.model.message import (
    CommandMessage,
    ErrorResultMessage,
    SubscriptionReportMessage,
    SuccessResultMessage,
)
from ..common.model.server_information import VersionInfo
from .client_connection import WS_COMMANDS

if TYPE_CHECKING:
    from chip.clusters import Attribute

    from .stack import MatterStack


class MatterDeviceController:
    """Class that manages the Matter devices."""

    # To track if wifi credentials set this session.
    wifi_cred_set = False

    def __init__(
        self,
        stack: MatterStack,
    ):
        self.stack = stack
        self.loop = asyncio.get_running_loop()
        self.logger = stack.logger.getChild("devices")
        
        # Instantiate the underlying ChipDeviceController instance on the Fabric
        self.chip_controller: ChipDeviceController = stack.fabric_admin.NewController()
        self._subscriptions: dict[int, Attribute.SubscriptionTransaction] = {}
        self.logger.debug("Device controller initialized.")


    @WS_COMMANDS.register("device_controller.CommissionWithCode")
    async def commission_with_code(self, setupPayload: str, nodeId: int) -> bool:
        """
        Commission a device.

        Return boolean if successful.
        """
        assert self.wifi_cred_set, "Received commissioning without Wi-Fi set"

        return await self.loop.run_in_executor(
            None,
            partial(self.chip_controller.CommissionWithCode, setupPayload=setupPayload, nodeid=nodeId),
        )

    @WS_COMMANDS.register("device_controller.CommissionOnNetwork")
    async def commission_on_network(self, nodeId: int, setupPinCode: int, filterType: DiscoveryFilterType = DiscoveryFilterType.NONE, filter: Any = None) -> bool:
        """
        Commission a device already connected to the network.

        Does the routine for OnNetworkCommissioning, with a filter for mDNS discovery.
        The filter can be an integer, a string or None depending on the actual type of selected filter.
        Return boolean if successful.
        """
        return await self.loop.run_in_executor(
            None,
            partial(self.chip_controller.CommissionOnNetwork, nodeId=nodeId, setupPinCode=setupPinCode, filterType=filterType, filter=filter),
        )

    @WS_COMMANDS.register("device_controller.Read")
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
                "nodeId": msg.args["nodeid"],
                "endpoint": path.Path.EndpointId,
                "cluster": path.ClusterType,
                "attribute": path.AttributeName,
                "value": data,
            }
            self.logger.info("subscription_callback %s", value)

            # This callback is running in the CHIP stack thread
            self.loop.call_soon_threadsafe(
                self._send_message, SubscriptionReportMessage(subscription_id, value)
            )

        subscription.SetAttributeUpdateCallback(subscription_callback)
        self.logger.info(f"SubscriptionId {subscription_id}")
        self._subscriptions[subscription_id] = subscription
        self._send_message(
            SuccessResultMessage(msg.messageId, {"subscription_id": subscription_id})
        )

    @WS_COMMANDS.register("device_controller.ResolveNode")
    async def _handle_device_controller_ResolveNode(self, msg: CommandMessage):
        result = await self.loop.run_in_executor(
            None, partial(self.chip_controller.ResolveNode, **msg.args)
        )
        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    @WS_COMMANDS.register("device_controller.SendCommand")
    async def _handle_device_controller_SendCommand(self, msg: CommandMessage):
        result = await self.chip_controller.SendCommand(**msg.args)
        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    @WS_COMMANDS.register("device_controller.SetThreadOperationalDataset")
    async def _handle_device_controller_SetThreadOperationalDataset(
        self, msg: CommandMessage
    ):
        result = await self.loop.run_in_executor(
            None,
            partial(
                self.chip_controller.SetThreadOperationalDataset,
                **msg.args,
            ),
        )
        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    @WS_COMMANDS.register("device_controller.OpenCommissioningWindow")
    async def _handle_device_controller_OpenCommissioningWindow(
        self, msg: CommandMessage
    ):
        result = await self.loop.run_in_executor(
            None,
            partial(
                self.chip_controller.OpenCommissioningWindow,
                **msg.args,
            ),
        )
        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    @WS_COMMANDS.register("device_controller.SetWiFiCredentials")
    async def _handle_device_controller_SetWiFiCredentials(self, msg: CommandMessage):
        result = await self.loop.run_in_executor(
            None,
            partial(self.chip_controller.SetWiFiCredentials, **msg.args),
        )

        if result == 0:
            self.server.stack.wifi_cred_set = True

        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    @WS_COMMANDS.register("device_controller.Unsubscribe")
    async def _handle_device_controller_Unsubscribe(self, msg: CommandMessage):
        """Unsubscribe."""
        subscription = self._subscriptions.pop(msg.args["subscription_id"], None)
        if subscription is None:
            self._send_message(ErrorResultMessage(msg.messageId, "not_found"))
            return

        await self.loop.run_in_executor(None, subscription.Shutdown)
        self._send_message(SuccessResultMessage(msg.messageId, None))
