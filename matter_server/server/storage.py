"""Logic to handle storage of persistent data."""

import asyncio
from genericpath import isfile
import logging
from types import NoneType
from typing import Dict, Union
import os

try:
    import orjson as json
except ImportError:
    import json

DATA_FILE = "storage.json"
DATA_FILE_BACKUP = f"{DATA_FILE}.backup"
DEFAULT_SAVE_DELAY = 30

StorageDataType = Union[str, dict, int, list, NoneType]

class StorageController:
    """Controller that handles storage of persistent data."""

    def __init__(self, storage_path: str) -> None:
        """Initialize storage controller."""
        self.storage_path = storage_path
        self.logger = logging.getLogger(__name__)
        self._data: Dict[str, StorageDataType] = {}
        self._timer_handle: asyncio.TimerHandle = None

    async def start(self) -> None:
        """Async initialize of controller."""
        await self._load()
        self.logger.debug("Started.")

    async def stop(self) -> None:
        """"Handle logic on server stop."""
        if not self._timer_handle:
            # no point in forcing a save when there are no changes pending
            return
        await self.save(immediate=True)
        self.logger.debug("Stopped.")

    async def get(self, key: str, default: StorageDataType = None) -> StorageDataType:
        """Get data from specific key."""
        return self._data.get(key, default)

    async def set(self, key: str, value: StorageDataType) -> None:
        """Set a value in persistent storage."""

    async def save(self, immediate: bool = False) -> None:
        """Schedule save of data to disk."""

        if self._timer_handle is not None:
            self._timer_handle.cancel()
            self._timer_handle = None

        loop = asyncio.get_running_loop()

        def _save():
            # make backup before we write a new file
            if os.path.isfile(DATA_FILE):
                if os.path.isfile(DATA_FILE_BACKUP):
                    os.remove(DATA_FILE_BACKUP)
                os.rename(DATA_FILE, DATA_FILE_BACKUP)

            with open(DATA_FILE, "w") as _file:
                json_data = json.dumps(self._data)
            self.logger.debug("Saved data to perstent storage")

        fut = loop.run_in_executor(None, _save)
        if immediate:
            loop.create_task(fut)
        else:
            # schedule the save for later
            self._timer_handle = loop.call_later(
                DEFAULT_SAVE_DELAY, loop.create_task, None, fut
            )

    async def _load(self) -> None:
        """Load data from persistent storage."""
        assert not self._data, "Already loaded"

        def _load() -> dict:
            for filename in DATA_FILE, DATA_FILE_BACKUP:
                try:
                    with open(DATA_FILE, "r") as _file:
                        data = json.loads(_file.read())
                        self.logger.debug("Loaded persistent settings from %s", filename)
                        return data
                except FileNotFoundError:
                    pass
                except json.decoder.JSONDecodeError as err:
                    self.logger.error("Error while reading persistent storage file %s", filename)
            self.logger.debug("Started with empty storage: No persistent storage file found.")
            return {}

        loop = asyncio.get_running_loop()
        self._data = await loop.run_in_executor(None, _load)
