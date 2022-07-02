from __future__ import annotations

from typing import TYPE_CHECKING

from .device_controller import DeviceController
from .read_subscriptions import ReadSubscriptions

if TYPE_CHECKING:
    from .. import client


class Driver:
    def __init__(self, client: client.Client):
        self.server_info = client.server_info
        self._client = client
        self.device_controller = DeviceController(client)
        self.read_subscriptions = ReadSubscriptions(client)
