"""Constants that are shared between server and client."""

# schema version is used to determine compatibility between server and client
SCHEMA_VERSION = 1

# we allow the schema version to be one version behind
MIN_SCHEMA_VERSION = SCHEMA_VERSION - 1

# we allow the schema version to be 2 versions ahead
# when making breaking changes (we shouldn't, I know),
# just bump the schema version a few points.
MAX_SCHEMA_VERSION = SCHEMA_VERSION + 2
