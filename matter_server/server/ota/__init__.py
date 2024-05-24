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
        "minApplicableSoftwareVersion": 1,
        "maxApplicableSoftwareVersion": 1,
        "otaUrl": "https://github.com/agners/matter-linux-example-apps/releases/download/v1.3.0.0/chip-ota-requestor-app-x86-64.ota",
    }
}


async def check_for_update(
    vid: int, pid: int, current_software_version: int
) -> None | dict:
    """Check for software updates."""
    if (vid, pid) in HARDCODED_UPDATES:
        return HARDCODED_UPDATES[(vid, pid)]

    return await dcl.check_for_update(vid, pid, current_software_version)
