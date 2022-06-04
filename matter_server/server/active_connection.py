from __future__ import annotations

import asyncio
from contextlib import suppress
import json
import typing
from typing import TYPE_CHECKING, Coroutine, Final
from concurrent import futures

from aiohttp import WSCloseCode, WSMsgType, web
from chip.exceptions import ChipStackError

from ..common.json_utils import CHIPJSONDecoder, CHIPJSONEncoder
from ..common.model.message import (
    CommandMessage,
    ErrorResultMessage,
    SubscriptionReportMessage,
    SuccessResultMessage,
)
from ..common.model.version import VersionInfo
from ..backports.enum import StrEnum

if TYPE_CHECKING:
    from .server import MatterServer
    from chip.clusters import Attribute, ClusterObjects

MAX_PENDING_MSG = 512
CANCELLATION_ERRORS: Final = (asyncio.CancelledError, futures.CancelledError)


class InstanceCommands(StrEnum):

    DEVICE_CONTROLLER = "device_controller"


class DeviceControllerCommands(StrEnum):

    COMMISSION_WITH_CODE = "CommissionWithCode"
    READ = "Read"
    RESOLVE_NODE = "ResolveNode"
    SEND_COMMAND = "SendCommand"
    SET_THREAD_OPERATIONAL_DATASET = "SetThreadOperationalDataset"
    SET_WIFI_CREDENTIALS = "SetWiFiCredentials"


PROTOCOL = {
    InstanceCommands.DEVICE_CONTROLLER: {
        DeviceControllerCommands.COMMISSION_WITH_CODE: {},
        DeviceControllerCommands.READ: {},
        DeviceControllerCommands.RESOLVE_NODE: {},
        DeviceControllerCommands.SEND_COMMAND: {},
        DeviceControllerCommands.SET_THREAD_OPERATIONAL_DATASET: {},
        DeviceControllerCommands.SET_WIFI_CREDENTIALS: {},
    }
}


class ActiveConnection:

    wsock: web.WebSocketResponse | None = None

    def __init__(self, server: MatterServer, request):
        self.server = server
        self.request = request
        self.logger = server.logger
        self._to_write: asyncio.Queue = asyncio.Queue(maxsize=MAX_PENDING_MSG)
        self._subscriptions: dict[int, Attribute.SubscriptionTransaction] = {}
        self._shutdown_event: asyncio.Event | None = None

    def _send_message(self, message) -> None:
        """Send a message to the client."""
        try:
            self._to_write.put_nowait(json.dumps(message, cls=CHIPJSONEncoder))
        except asyncio.QueueFull:
            self.logger.error(
                "Client exceeded max pending messages: %s", MAX_PENDING_MSG
            )
            asyncio.get_running_loop().create_task(self.disconnect())

    async def disconnect(self):
        self._shutdown_event = asyncio.Event()
        await self.wsock.close(code=WSCloseCode.GOING_AWAY, message="Server shutdown")
        await self._shutdown_event.wait()

    async def handle_request(self):
        self.logger.info("New Client connection...")
        self.wsock = web.WebSocketResponse()
        await self.wsock.prepare(self.request)

        self._send_message(
            VersionInfo(
                driver_version=0,
                server_version=0,
                min_schema_version=1,
                max_schema_version=1,
            )
        )

        self.logger.info("Websocket connection ready")

        writer_task = asyncio.create_task(self._writer())

        try:
            while not self.wsock.closed:
                msg = await self.wsock.receive()
                if msg.type in (
                    WSMsgType.CLOSE,
                    WSMsgType.CLOSING,
                    WSMsgType.CLOSED,
                ):
                    break

                if msg.type != WSMsgType.TEXT:
                    self.logger.debug("Ignoring %s", msg)
                    continue

                try:
                    self.logger.info("Received: %s", msg.data)
                    msg = json.loads(msg.data, cls=CHIPJSONDecoder)
                except ValueError:
                    self.logger.error("Invalid JSON: %s", msg.data)
                    await self.wsock.close(
                        code=WSCloseCode.INVALID_TEXT, message="Invalid JSON"
                    )
                    break

                self.logger.info("Deserialized message: %s", msg)
                if not isinstance(msg, CommandMessage):
                    self.logger.error("Invalid Message received: %s", msg.data)
                    continue

                self._handle_message(msg)
        finally:
            self.logger.info("Websocket connection closed")
            writer_task.cancel()

            for subscriptionid, subscription in self._subscriptions.items():
                self.logger.info("Shutdown subscription id %d", subscriptionid)
                subscription.Shutdown()

            await writer_task
            if self._shutdown_event:
                self._shutdown_event.set()

        return self.wsock

    async def _writer(self) -> None:
        """Write outgoing messages."""
        # Exceptions if Socket disconnected or cancelled by connection handler
        with suppress(RuntimeError, ConnectionResetError, *CANCELLATION_ERRORS):
            while not self.wsock.closed:
                message = await self._to_write.get()
                self.logger.debug("Sending %s", message)
                await self.wsock.send_str(message)

    def _handle_message(self, msg: CommandMessage):
        instance, _, command = msg.command.partition(".")

        if instance not in PROTOCOL:
            self._send_message(ErrorResultMessage(msg.messageId, "INVALID_COMMAND"))
            self.logger.warning("Unknown command: %s", msg.command)
            return

        if command not in PROTOCOL[instance]:
            self.logger.warning("Unknown command: %s", msg.command)
            # TODO turn on to ensure we only allow approved methods
            # self._send_message(ErrorResultMessage(msg.messageId, "INVALID_COMMAND"))
            # return

        # TODO Validate message against schema.

        try:
            getattr(self, f"_handle_{instance}_message")(msg, command)
        except ChipStackError as ex:
            self._send_message(ErrorResultMessage(msg.messageId, str(ex)))
        except Exception:  # pylint: disable=broad-except
            self.logger.exception("Error handling message: %s", msg.data)
            self._send_message(ErrorResultMessage(msg.messageId, "Unknown error"))

    def _handle_device_controller_message(self, msg: CommandMessage, command: str):
        if command == "Read" and msg.args.get("reportInterval") is not None:
            method = self._handle_device_controller_subscribe_message
        else:
            method = getattr(self.server.stack.device_controller, command)

        if command == "CommissionWithCode" and not self.server.stack.wifi_cred_set:
            self.logger.warning("Received commissioning without Wi-Fi set")

        elif command == "Read" and isinstance(msg.args.get("attributes"), list):
            converted_attributes = []
            for attribute in msg.args["attributes"]:
                if isinstance(attribute, list):
                    converted_attributes.append(tuple(attribute))
                else:
                    converted_attributes.append(attribute)

            msg.args["attributes"] = converted_attributes

        # TODO check commmands if blocking and if so push it to executor.
        result = method(**msg.args)

        if asyncio.iscoroutine(result):
            asyncio.get_running_loop().create_task(
                self._handle_coroutine_command(msg, result)
            )
            return

        if command == "SetWiFiCredentials" and result == 0:
            self.server.stack.wifi_cred_set = True

        self._send_message(SuccessResultMessage(msg.messageId, result))

    async def _handle_device_controller_subscribe_message(
        self,
        nodeid: int,
        # Moved up f
        reportInterval: typing.Tuple[int, int],
        attributes: typing.List[
            typing.Union[
                None,  # Empty tuple, all wildcard
                typing.Tuple[int],  # Endpoint
                # Wildcard endpoint, Cluster id present
                typing.Tuple[typing.Type[ClusterObjects.Cluster]],
                # Wildcard endpoint, Cluster + Attribute present
                typing.Tuple[typing.Type[ClusterObjects.ClusterAttributeDescriptor]],
                # Wildcard attribute id
                typing.Tuple[int, typing.Type[ClusterObjects.Cluster]],
                # Concrete path
                typing.Tuple[
                    int, typing.Type[ClusterObjects.ClusterAttributeDescriptor]
                ],
            ]
        ] = None,
        dataVersionFilters: typing.List[
            typing.Tuple[int, typing.Type[ClusterObjects.Cluster], int]
        ] = None,
        events: typing.List[
            typing.Union[
                None,  # Empty tuple, all wildcard
                typing.Tuple[str, int],  # all wildcard with urgency set
                typing.Tuple[int, int],  # Endpoint,
                # Wildcard endpoint, Cluster id present
                typing.Tuple[typing.Type[ClusterObjects.Cluster], int],
                # Wildcard endpoint, Cluster + Event present
                typing.Tuple[typing.Type[ClusterObjects.ClusterEvent], int],
                # Wildcard event id
                typing.Tuple[int, typing.Type[ClusterObjects.Cluster], int],
                # Concrete path
                typing.Tuple[int, typing.Type[ClusterObjects.ClusterEvent], int],
            ]
        ] = None,
        returnClusterObject: bool = False,
        fabricFiltered: bool = True,
        keepSubscriptions: bool = False,
    ):
        """
        Handle a Read that results in a subscription.

        Type signature is copied from Read except reportInterval is made mandatory.
        """
        self.logger.info("Setting up Subscription for %s", attributes)

        fabricid = self.server.stack.device_controller.GetFabricId()
        loop = asyncio.get_event_loop()

        subscription: Attribute.SubscriptionTransaction = (
            await self.server.stack.device_controller.Read(
                nodeid,
                attributes,
                dataVersionFilters,
                events,
                returnClusterObject,
                reportInterval,
                fabricFiltered,
                keepSubscriptions,
            )
        )

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
                "fabridId": fabricid,
                "nodeId": nodeid,
                "endpoint": path.Path.EndpointId,
                "cluster": path.ClusterType,
                "attribute": path.AttributeName,
                "value": data,
            }
            self.logger.info("subscription_callback %s", value)

            # This callback is running in the CHIP stack thread
            loop.call_soon_threadsafe(
                self._send_message, SubscriptionReportMessage(subscription_id, value)
            )

        self.logger.info("Setting callback for subscription of %s", attributes)
        subscription.SetAttributeUpdateCallback(subscription_callback)
        self.logger.info(f"SubscriptionId {subscription_id}")
        self._subscriptions[subscription_id] = subscription
        return subscription_id

    async def _handle_coroutine_command(self, msg: CommandMessage, action: Coroutine):
        try:
            result = await action
        except ChipStackError as ex:
            self._send_message(ErrorResultMessage(msg.messageId, str(ex)))
        except Exception:
            self.logger.exception("Error handling message: %s", msg.data)
            self._send_message(ErrorResultMessage(msg.messageId, "Unknown error"))

        self._send_message(SuccessResultMessage(msg.messageId, result))
