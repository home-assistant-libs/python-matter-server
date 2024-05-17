FROM python:3.11-slim-bullseye

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /app

RUN \
    set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        libuv1 \
        zlib1g \
        libjson-c5 \
        libnl-3-200 \
        libnl-route-3-200 \
        unzip \
        gdb \
        iputils-ping \
        iproute2 \
    && apt-get purge -y --auto-remove \
    && rm -rf \
        /var/lib/apt/lists/* \
        /usr/src/*

ARG PYTHON_MATTER_SERVER

# hadolint ignore=DL3013
RUN \
    pip3 install --no-cache-dir "python-matter-server[server]==${PYTHON_MATTER_SERVER}"

VOLUME ["/data"]
EXPOSE 5580

ENTRYPOINT [ "matter-server" ]
CMD [ "--storage-path", "/data", "--paa-root-cert-dir", "/data/credentials" ]
