"""Matter adapter."""
from __future__ import annotations

from abc import abstractmethod
import logging
from typing import Callable

import aiohttp

from .model.node import MatterNode


class AbstractMatterAdapter:

    logger: logging.Logger

    @abstractmethod
    async def load_data(self) -> dict | None:
        """Load data."""

    @abstractmethod
    async def save_data(self, data: dict) -> None:
        """Save data."""

    @abstractmethod
    def delay_save_data(self, get_data: Callable[[], dict]) -> None:
        """Save data, but not right now."""

    @abstractmethod
    def get_server_url(self) -> str:
        """Return server URL."""

    @abstractmethod
    def get_client_session(self) -> aiohttp.ClientSession:
        """Return aiohttp client session."""

    @abstractmethod
    async def setup_node(self, node: MatterNode) -> None:
        """Set up a node."""

    @abstractmethod
    async def handle_server_disconnected(self, should_reload: bool) -> None:
        """Server disconnected."""
