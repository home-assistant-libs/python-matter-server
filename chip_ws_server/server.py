import json
import logging

import chip.clusters.Objects as Clusters
from chip_ws_common.wsmsg import WSDecoder

_LOGGER = logging.getLogger(__name__)


class CHIPControllerServer:
    def __init__(self):
        pass

    def setup(self):
        _LOGGER.info("Setup CHIP Controller Server")

    def shutdown(self):
        _LOGGER.info("Shutdown CHIP Controller Server")

    def new_message(self, msg: str):
        _LOGGER.info(msg)
        print(json.loads(msg, cls=WSDecoder))

