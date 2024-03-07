"""Server-only constants for the Python Matter Server."""


# The minimum schema version (of a client) the server can support
MIN_SCHEMA_VERSION = 5

# schema version of our data model
# only bump if the format of the data in MatterNodeData changed
# and a full re-interview is mandatory
DATA_MODEL_SCHEMA_VERSION = 6
