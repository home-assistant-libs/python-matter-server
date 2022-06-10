import asyncio
import logging
import os
from pathlib import Path
import sys

import coloredlogs

from .matter_stack import MatterStack
from .server import MatterServer

logging.basicConfig(level=logging.WARN)
_LOGGER = logging.getLogger(__package__)
_LOGGER.setLevel(logging.DEBUG)


def main() -> int:
    host = os.getenv("CHIP_WS_SERVER_HOST", "::,0.0.0.0").split(",")
    port = int(os.getenv("CHIP_WS_SERVER_PORT", "5580"))
    storage_path = os.getenv(
        "CHIP_WS_STORAGE",
        str(Path.home() / ".chip-storage/python-kv.json"),
    )
    debug = os.getenv("CHIP_WS_DEBUG") is not None

    coloredlogs.install(level=logging.DEBUG if debug else logging.INFO)
    stack = MatterStack(storage_path)

    loop = asyncio.get_event_loop()

    async def create_server():
        return MatterServer(stack)

    server = loop.run_until_complete(create_server())
    server.run(host, port)
    stack.shutdown()


if __name__ == "__main__":
    sys.exit(main())
