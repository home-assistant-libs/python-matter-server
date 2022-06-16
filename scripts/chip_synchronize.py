import os
import pathlib
import shutil
import re

REPO_ROOT = pathlib.Path(__file__).parent.parent

CHIP_ROOT = REPO_ROOT / "../connectedhomeip"

CLUSTER_OBJECTS = REPO_ROOT / "matter_server/vendor/chip/clusters/Objects.py"

REPLACE_IMPORT = {
    "from chip import ChipUtility\n": "from .. import ChipUtility\n",
    "from chip.tlv import uint, float32\n": "from ..tlv import uint, float32\n"
}


def main():
    with open(CLUSTER_OBJECTS, "w") as cluster_outfile:
        with open(CHIP_ROOT / "src/controller/python/chip/clusters/Objects.py", "r") as cluster_file:
            for line in cluster_file:
                if line in REPLACE_IMPORT.keys():
                    line = REPLACE_IMPORT[line]
                cluster_outfile.write(line)


if __name__ == "__main__":
    main()
