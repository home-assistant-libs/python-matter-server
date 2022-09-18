import pathlib
import subprocess

REPO_ROOT = pathlib.Path(__file__).parent.parent

CHIP_ROOT = REPO_ROOT / "../connectedhomeip"

CLUSTER_OBJECTS = REPO_ROOT / "matter_server/vendor/chip/clusters/Objects.py"
CLUSTER_OBJECTS_VERSION = (
    REPO_ROOT / "matter_server/vendor/chip/clusters/ObjectsVersion.py"
)

REPLACE_IMPORT = {
    "from chip import ChipUtility\n": "from .. import ChipUtility\n",
    "from chip.tlv import uint, float32\n": "from ..tlv import uint, float32\n",
}


def chip_sha():
    return (
        subprocess.run(
            "git rev-parse HEAD",
            shell=True,
            cwd=CHIP_ROOT,
            check=True,
            capture_output=True,
        )
        .stdout.decode()
        .strip()
    )


def main():
    with open(CLUSTER_OBJECTS, "w") as cluster_outfile:
        with open(
            CHIP_ROOT / "src/controller/python/chip/clusters/Objects.py", "r"
        ) as cluster_file:
            for line in cluster_file:
                if line in REPLACE_IMPORT.keys():
                    line = REPLACE_IMPORT[line]
                cluster_outfile.write(line)
    with open(CLUSTER_OBJECTS_VERSION, "w") as cluster_version_outfile:
        cluster_version_outfile.write(f'CLUSTER_OBJECT_VERSION = "{chip_sha()}"')


if __name__ == "__main__":
    main()
