#!/bin/sh
set -e

set -- matter-server --storage-path /data "$@"

echo "Starting server:" "$@"
exec "$@"
