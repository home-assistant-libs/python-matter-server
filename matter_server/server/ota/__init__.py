"""OTA implementation for the Matter Server."""

from matter_server.server.ota import dcl

HARDCODED_UPDATES: dict[tuple[int, int], dict] = {
    # OTA requestor example app, useful for testing
    (0xFFF1, 0x8001): {
        "vid": 0xFFF1,
        "pid": 0x8001,
        "softwareVersion": 2,
        "softwareVersionString": "2.0",
        "cdVersionNumber": 1,
        "softwareVersionValid": True,
        "otaChecksum": "7qcyvg2kPmKZaDLIk8C7Vyteqf4DI73x0tFZkmPALCo=",
        "otaChecksumType": 1,
        "minApplicableSoftwareVersion": 1,
        "maxApplicableSoftwareVersion": 1,
        "otaUrl": "https://github.com/agners/matter-linux-example-apps/releases/download/v1.3.0.0/chip-ota-requestor-app-x86-64.ota",
        "releaseNotesUrl": "https://github.com/agners/matter-linux-example-apps/releases/tag/v1.3.0.0",
    },
    (0x143D, 0x1001): {
        "vid": 0x143D,
        "pid": 0x1001,
        "softwareVersion": 10010011,
        "softwareVersionString": "1.1.11-c85ba1e-dirty",
        "cdVersionNumber": 1,
        "softwareVersionValid": True,
        "otaChecksum": "x2sK9xjVuGff0eefYa4cporDO+Z+WVxxw+JP5Ol+5og=",
        "otaChecksumType": 1,
        "minApplicableSoftwareVersion": 10010000,
        "maxApplicableSoftwareVersion": 10010011,
        "otaUrl": "https://raw.githubusercontent.com/ChampOnBon/Onvis/master/S4/debug.ota",
    },
}


async def check_for_update(
    vid: int,
    pid: int,
    current_software_version: int,
    requested_software_version: int | None = None,
) -> None | dict:
    """Check for software updates."""
    if (vid, pid) in HARDCODED_UPDATES:
        update = HARDCODED_UPDATES[(vid, pid)]
        if (
            requested_software_version is None
            or update["softwareVersion"] == requested_software_version
        ):
            return update

    return await dcl.check_for_update(vid, pid, current_software_version)
