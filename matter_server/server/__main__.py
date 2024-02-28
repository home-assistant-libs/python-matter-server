"""Script entry point to run the Matter Server."""

import argparse
import asyncio
import logging
import os
from pathlib import Path
import sys
import threading

from aiorun import run
import coloredlogs

from matter_server.server import stack

from .server import MatterServer

DEFAULT_VENDOR_ID = 0xFFF1
DEFAULT_FABRIC_ID = 1
DEFAULT_PORT = 5580
# Default to None to bind to all addresses on both IPv4 and IPv6
DEFAULT_LISTEN_ADDRESS = None
DEFAULT_STORAGE_PATH = os.path.join(Path.home(), ".matter_server")

# Get parsed passed in arguments.
parser = argparse.ArgumentParser(
    description="Matter Controller Server using WebSockets."
)


parser.add_argument(
    "--vendorid",
    type=int,
    default=DEFAULT_VENDOR_ID,
    help=f"Vendor ID for the Fabric, defaults to {DEFAULT_VENDOR_ID}",
)
parser.add_argument(
    "--fabricid",
    type=int,
    default=DEFAULT_FABRIC_ID,
    help=f"Fabric ID for the Fabric, defaults to {DEFAULT_FABRIC_ID}",
)
parser.add_argument(
    "--storage-path",
    type=str,
    default=DEFAULT_STORAGE_PATH,
    help=f"Storage path to keep persistent data, defaults to {DEFAULT_STORAGE_PATH}",
)
parser.add_argument(
    "--port",
    type=int,
    default=DEFAULT_PORT,
    help=f"TCP Port to run the websocket server, defaults to {DEFAULT_PORT}",
)
parser.add_argument(
    "--listen-address",
    type=str,
    action="append",
    default=DEFAULT_LISTEN_ADDRESS,
    help="IP address to bind the websocket server to, defaults to any IPv4 and IPv6 address.",
)
parser.add_argument(
    "--log-level",
    type=str,
    default="info",
    help="Global logging level. Example --log-level debug, default=info, possible=(critical, error, warning, info, debug)",
)
parser.add_argument(
    "--log-level-sdk",
    type=str,
    default="error",
    help="Matter SDK logging level. Example --log-level-sdk detail, default=error, possible=(none, error, progress, detail, automation)",
)
parser.add_argument(
    "--log-file",
    type=str,
    default=None,
    help="Log file to write to (optional).",
)
parser.add_argument(
    "--primary-interface",
    type=str,
    default=None,
    help="Primary network interface for link-local addresses (optional).",
)

args = parser.parse_args()


def _setup_logging() -> None:
    custom_level_style = {
        **coloredlogs.DEFAULT_LEVEL_STYLES,
        "chip_automation": {"color": "green", "faint": True},
        "chip_detail": {"color": "green", "faint": True},
        "chip_progress": {},
        "chip_error": {"color": "red"},
    }
    # Let coloredlogs handle all levels, we filter levels in the logging module
    coloredlogs.install(level=logging.NOTSET, level_styles=custom_level_style)

    handlers = None
    if args.log_file:
        handlers = [logging.FileHandler(args.log_file)]
    logging.basicConfig(handlers=handlers, level=args.log_level.upper())

    stack.init_logging(args.log_level_sdk.upper())
    logging.getLogger().setLevel(args.log_level.upper())

    if not logging.getLogger().isEnabledFor(logging.DEBUG):
        logging.getLogger("PersistentStorage").setLevel(logging.WARNING)
        # Temporary disable the logger of chip.clusters.Attribute because it now logs
        # an error on every custom attribute that couldn't be parsed which confuses people.
        # We can restore the default log level again when we've patched the device controller
        # to handle the raw attribute data to deal with custom clusters.
        logging.getLogger("chip.clusters.Attribute").setLevel(logging.CRITICAL)
    if not logging.getLogger().isEnabledFor(logging.DEBUG):
        # (temporary) raise the log level of zeroconf as its a logs an annoying
        # warning at startup while trying to bind to a loopback IPv6 interface
        logging.getLogger("zeroconf").setLevel(logging.ERROR)

    # register global uncaught exception loggers
    sys.excepthook = lambda *args: logging.getLogger(None).exception(
        "Uncaught exception",
        exc_info=args,
    )
    threading.excepthook = lambda args: logging.getLogger(None).exception(
        "Uncaught thread exception",
        exc_info=(  # type: ignore[arg-type]
            args.exc_type,
            args.exc_value,
            args.exc_traceback,
        ),
    )


def main() -> None:
    """Run main execution."""

    _setup_logging()

    # make sure storage path exists
    if not os.path.isdir(args.storage_path):
        os.mkdir(args.storage_path)

    # Init server
    server = MatterServer(
        args.storage_path,
        int(args.vendorid),
        int(args.fabricid),
        int(args.port),
        args.listen_address,
        args.primary_interface,
    )

    async def handle_stop(loop: asyncio.AbstractEventLoop) -> None:
        # pylint: disable=unused-argument
        await server.stop()

    # run the server
    run(server.start(), shutdown_callback=handle_stop, executor_workers=32)


if __name__ == "__main__":
    main()
