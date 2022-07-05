import argparse
import asyncio
import logging
import os
from pathlib import Path
import sys

import coloredlogs

from .matter_stack import MatterStack
from .server import MatterServer

_LOGGER = logging.getLogger(__package__)


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""

    parser = argparse.ArgumentParser(
        description="Matter Controller Server using WebSockets."
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Log file to write to.  If not set, matter_server.log is used",
    )
    parser.add_argument(
        "-log",
        "--log-level",
        default="info",
        help="Provide logging level. Example --log-level debug, default=info, possible=(critical, error, warning, info, debug)",
    )

    arguments = parser.parse_args()

    return arguments


def main() -> int:
    args = get_arguments()
    handlers = None

    if args.log_file:
        handlers = [logging.FileHandler(args.log_file)]

    logging.basicConfig(handlers=handlers, level=args.log_level.upper())

    host = os.getenv("CHIP_WS_SERVER_HOST", "::,0.0.0.0").split(",")
    port = int(os.getenv("CHIP_WS_SERVER_PORT", "5580"))
    storage_path = os.getenv(
        "CHIP_WS_STORAGE",
        str(Path.home() / ".chip-storage/python-kv.json"),
    )
    debug = os.getenv("CHIP_WS_DEBUG") is not None

    coloredlogs.install(level=logging.DEBUG if debug else args.log_level.upper())
    stack = MatterStack(storage_path)

    loop = asyncio.get_event_loop()

    async def create_server():
        return MatterServer(stack)

    server = loop.run_until_complete(create_server())
    server.run(host, port)
    stack.shutdown()


if __name__ == "__main__":
    sys.exit(main())
