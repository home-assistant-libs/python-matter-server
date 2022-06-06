from __future__ import annotations

import asyncio
from concurrent import futures
from functools import partial
import logging
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Final, cast

from chip.exceptions import ChipStackError

from ..common.model.message import (
    CommandMessage,
    ErrorResultMessage,
    ServerInformation,
    SubscriptionReportMessage,
    SuccessResultMessage,
)
from ..common.model.version import VersionInfo

if TYPE_CHECKING:
    from chip.clusters import Attribute

    from .server import MatterServer

MAX_PENDING_MSG = 512
CANCELLATION_ERRORS: Final = (asyncio.CancelledError, futures.CancelledError)


class Commands(dict):
    """Small helper to register commands."""

    def register(self, command: str):
        """Decorate a command handler."""

        def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
            self[command] = func
            return func

        return decorator


class Disconnect(Exception):
    """When the connection needs to be closed."""


class ActiveConnection:
    """Active connection between a client and Matter."""

    commands = Commands()
    fabric_id: int

    def __init__(
        self,
        logger: logging.Logger,
        server: MatterServer,
        send_message: Callable[[Any], None],
    ):
        self.logger = logger
        self.server = server
        self.loop = asyncio.get_running_loop()
        self._send_message = send_message
        self._subscriptions: dict[int, Attribute.SubscriptionTransaction] = {}

    async def async_initialize(self):
        """Initialize connection."""
        self._send_message(
            VersionInfo(
                driver_version=0,
                server_version=0,
                min_schema_version=1,
                max_schema_version=1,
            )
        )

    def async_handle_close(self):
        """Handle connection shutting down."""
        for subscriptionid, subscription in self._subscriptions.items():
            self.logger.info("Shutdown subscription id %d", subscriptionid)
            subscription.Shutdown()

    def async_handle(self, msg: CommandMessage):
        """Handle a command."""
        handler = self.commands.get(msg.command)

        if handler is None:
            self._send_message(ErrorResultMessage(msg.messageId, "INVALID_COMMAND"))
            self.logger.warning("Unknown command: %s", msg.command)
            return

        self.loop.create_task(self._run_handler(handler, msg))

    async def _run_handler(self, handler, msg: CommandMessage):
        try:
            await handler(self, msg)
        except ChipStackError as ex:
            self._send_message(ErrorResultMessage(msg.messageId, str(ex)))
        except Exception:  # pylint: disable=broad-except
            self.logger.exception("Error handling message: %s", msg)
            self._send_message(ErrorResultMessage(msg.messageId, "unknown_error"))

    # pylint: disable=invalid-name

    @commands.register("server.GetInfo")
    async def _handle_server_GetInfo(self, msg: CommandMessage):
        self._send_message(
            SuccessResultMessage(
                msg.messageId,
                ServerInformation(
                    fabricId=self.server.stack.fabric_id,
                    compressedFabricId=self.server.stack.compressed_fabric_id,
                ),
            )
        )

    @commands.register("device_controller.CommissionWithCode")
    async def _handle_device_controller_CommissionWithCode(self, msg: CommandMessage):
        if not self.server.stack.wifi_cred_set:
            self.logger.warning("Received commissioning without Wi-Fi set")

        result = await self.loop.run_in_executor(
            None,
            partial(self.server.stack.device_controller.CommissionWithCode, **msg.args),
        )
        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    @commands.register("device_controller.Read")
    async def _handle_device_controller_Read(self, msg: CommandMessage):
        if isinstance(msg.args.get("attributes"), list):
            converted_attributes = []
            for attribute in msg.args["attributes"]:
                if isinstance(attribute, list):
                    converted_attributes.append(tuple(attribute))
                else:
                    converted_attributes.append(attribute)

            msg.args["attributes"] = converted_attributes

        result = await self.server.stack.device_controller.Read(**msg.args)

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

    @commands.register("device_controller.ResolveNode")
    async def _handle_device_controller_ResolveNode(self, msg: CommandMessage):
        result = await self.loop.run_in_executor(
            None, partial(self.server.stack.device_controller.ResolveNode, **msg.args)
        )
        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    @commands.register("device_controller.SendCommand")
    async def _handle_device_controller_SendCommand(self, msg: CommandMessage):
        result = await self.server.stack.device_controller.SendCommand(**msg.args)
        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    @commands.register("device_controller.SetThreadOperationalDataset")
    async def _handle_device_controller_SetThreadOperationalDataset(
        self, msg: CommandMessage
    ):
        result = await self.loop.run_in_executor(
            None,
            partial(
                self.server.stack.device_controller.SetThreadOperationalDataset,
                **msg.args,
            ),
        )
        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    @commands.register("device_controller.OpenCommissioningWindow")
    async def _handle_device_controller_OpenCommissioningWindow(
        self, msg: CommandMessage
    ):
        result = await self.loop.run_in_executor(
            None,
            partial(
                self.server.stack.device_controller.OpenCommissioningWindow,
                **msg.args,
            ),
        )
        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    @commands.register("device_controller.SetWiFiCredentials")
    async def _handle_device_controller_SetWiFiCredentials(self, msg: CommandMessage):
        result = await self.loop.run_in_executor(
            None,
            partial(self.server.stack.device_controller.SetWiFiCredentials, **msg.args),
        )

        if result == 0:
            self.server.stack.wifi_cred_set = True

        self._send_message(SuccessResultMessage(msg.messageId, {"raw": result}))

    @commands.register("device_controller.Unsubscribe")
    async def _handle_device_controller_Unsubscribe(self, msg: CommandMessage):
        """Unsubscribe."""
        subscription = self._subscriptions.pop(msg.args["subscription_id"], None)
        if subscription is None:
            self._send_message(ErrorResultMessage(msg.messageId, "not_found"))
            return

        await self.loop.run_in_executor(None, subscription.Shutdown)
        self._send_message(SuccessResultMessage(msg.messageId, None))
