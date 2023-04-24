"""Server-only constants for the Python Matter Server."""
import pathlib
from typing import Final

# The minimum schema version (of a client) the server can support
MIN_SCHEMA_VERSION = 2

# the paa-root-certs path is hardcoded in the sdk at this time
# and always uses the development subfolder
# regardless of anything you pass into instantiating the controller
# revisit this once matter 1.1 is released
PAA_ROOT_CERTS_DIR: Final[pathlib.Path] = (
    pathlib.Path(__file__)
    .parent.resolve()
    .parent.resolve()
    .parent.resolve()
    .joinpath("credentials/development/paa-root-certs")
)
