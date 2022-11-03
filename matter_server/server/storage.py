"""Logic to handle storage of persistent data."""

import asyncio
import logging
import os
from types import NoneType
from typing import TYPE_CHECKING, Dict, Union

from genericpath import isfile

try:
    import orjson as json
except ImportError:
    import json

DEFAULT_SAVE_DELAY = 30

if TYPE_CHECKING:
    from .server import MatterServer

StorageDataType = Union[str, dict, int, list[str], list[int], list[dict], NoneType]


class StorageController:
    """Controller that handles storage of persistent data."""

    def __init__(self, server: MatterServer) -> None:
        """Initialize storage controller."""
        self.server = server
        self.logger = logging.getLogger(__name__)
        self._data: Dict[str, StorageDataType] = {}
        self._timer_handle: asyncio.TimerHandle = None

    @property
    def filename(self) -> str:
        """Return full path to (fabric-specific) storage file."""
        return f"{self.server.device_controller.compressed_fabric_id}.json"

    async def start(self) -> None:
        """Async initialize of controller."""
        await self._load()
        self.logger.debug("Started.")

    async def stop(self) -> None:
        """ "Handle logic on server stop."""
        if not self._timer_handle:
            # no point in forcing a save when there are no changes pending
            return
        await self._save(immediate=True)
        self.logger.debug("Stopped.")

    def get(
        self, key: str, default: StorageDataType = None, subkey: str | None = None
    ) -> StorageDataType:
        """Get data from specific (sub)key."""
        if subkey:
            # we provide support for (1-level) nested dict
            return self._data.get(key, {}).get(subkey, default)
        return self._data.get(key, default)

    def set(
        self,
        key: str,
        value: StorageDataType,
        subkey: str | None = None,
        immediate: bool = False,
    ) -> None:
        """
        Set a (sub)value in persistent storage.

        NOTE: Json serializable types only!
        """
        if self.get(key, subkey=subkey) == value:
            # no need to save if value did not change
            return
        if subkey:
            # we provide support for (1-level) nested dict
            self._data.setdefault(key, {})
            self._data[key][subkey] = value
        else:
            self._data[key] = value
        self._save(immediate)

    def __getitem__(self, key: str) -> StorageDataType:
        """Get data from specific key."""
        return self._data[key]

    def __setitem__(self, key: str, value: StorageDataType) -> None:
        """Set a value in persistent storage."""
        self.set(key, value)

    async def _load(self) -> None:
        """Load data from persistent storage."""
        assert not self._data, "Already loaded"

        def _load() -> dict:
            for filename in self.filename, f"{self.filename}.backup":
                try:
                    _filename = os.path.join(self.server.storage_path, filename)
                    with open(filename, "r") as _file:
                        data = json.loads(_file.read())
                        self.logger.debug(
                            "Loaded persistent settings from %s", filename
                        )
                        return data
                except FileNotFoundError:
                    pass
                except json.decoder.JSONDecodeError as err:
                    self.logger.error(
                        "Error while reading persistent storage file %s", filename
                    )
            self.logger.debug(
                "Started with empty storage: No persistent storage file found."
            )
            return {}

        loop = asyncio.get_running_loop()
        self._data = await loop.run_in_executor(None, _load)

    def _save(self, immediate: bool = False) -> None:
        """Schedule save of data to disk."""

        if self._timer_handle is not None:
            self._timer_handle.cancel()
            self._timer_handle = None

        loop = asyncio.get_running_loop()

        def _save():
            filename_backup = f"{self.filename}.backup"
            # make backup before we write a new file
            if os.path.isfile(self.filename):
                if os.path.isfile(filename_backup):
                    os.remove(filename_backup)
                os.rename(self.filename, filename_backup)

            with open(self.filename, "w") as _file:
                json_data = json.dumps(self._data)
            self.logger.debug("Saved data to persistent storage")

        fut = loop.run_in_executor(None, _save)
        if immediate:
            loop.create_task(fut)
        else:
            # schedule the save for later
            self._timer_handle = loop.call_later(
                DEFAULT_SAVE_DELAY, loop.create_task, None, fut
            )
