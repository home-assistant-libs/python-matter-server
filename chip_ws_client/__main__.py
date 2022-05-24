import asyncio
import logging
import os
import sys
from dataclasses import dataclass
from functools import partial
from tkinter.tix import TEXT

import aiohttp
from aiohttp.http import WSMsgType

from chip_ws_client.client import CHIPControllerClient

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

HOST = os.getenv('CHIP_WS_SERVER_HOST', '127.0.0.1')
PORT = int(os.getenv('CHIP_WS_SERVER_PORT', 8080))

URL = f'http://{HOST}:{PORT}/chip_ws'
                    

if __name__ == '__main__':
    client = CHIPControllerClient(URL)
    scope_vars = { 'client': client }

    from traitlets.config import Config
    c = Config()
    c.InteractiveShellApp.exec_lines = [
        "await client.setup()"
    ]

    import IPython
    IPython.start_ipython(config=c, argv=[], user_ns=scope_vars)
