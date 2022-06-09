from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Callable

from matter_server.client.exceptions import NotConnected

if TYPE_CHECKING:
    from ..client import Client
    from .device_controller import (
        ReadAttributesType,
        ReadDataVersionFiltersType,
        ReadEventsType,
    )


class ReadSubscriptions:
    def __init__(self, client: Client):
        self.client = client
        self.subscriptions: dict[int, Callable[[dict], None]] = {}

    async def subscribe_node(
        self,
        nodeid: int,
        subscription_callback: Callable[[dict], None],
        reportInterval: tuple[int, int],
        attributes: ReadAttributesType = None,
        dataVersionFilters: ReadDataVersionFiltersType = None,
        events: ReadEventsType = None,
        returnClusterObject: bool = False,
        fabricFiltered: bool = True,
        keepSubscriptions: bool = False,
    ):
        """Subscribe to a node."""
        read_result = await self.client.driver.device_controller.read(
            nodeid=nodeid,
            reportInterval=reportInterval,
            attributes=attributes,
            dataVersionFilters=dataVersionFilters,
            events=events,
            returnClusterObject=returnClusterObject,
            fabricFiltered=fabricFiltered,
            keepSubscriptions=keepSubscriptions,
        )

        self.subscriptions[read_result["subscription_id"]] = subscription_callback

        async def unsubscribe():
            with suppress(NotConnected):
                await self.client.async_send_command(
                    "device_controller.Unsubscribe",
                    {"subscription_id": read_result["subscription_id"]},
                )

        return unsubscribe

    def receive_event(self, event):
        """Receive a subscription event."""
        subscription_id = event["subscriptionId"]
        if not (callback := self.subscriptions.get(subscription_id)):
            self.client.logger.warning(
                f"No Subscription object for Subscription Id 0x{subscription_id:X} present."
            )
            return
        try:
            callback(event)
        except Exception:  # pylint: disable=broad-except
            self.client.logger.exception(
                "Unexpected exception handling event %s", event
            )
