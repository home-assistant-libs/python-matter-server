FROM debian:bullseye as base

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG MATTER_SERVER_VERSION=1.0.7
ARG HOME_ASSISTANT_CHIP_VERSION=2022.11.1

WORKDIR /app

RUN \
    set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    libuv1 \
    openssl \
    zlib1g \
    libjson-c5 \
    python3-venv \
    python3-pip \
    python3-gi \
    python3-gi-cairo \
    python3-dbus \
    python3-psutil \
    unzip \
    libcairo2 \
    gdb \
    git \
    && git clone --depth 1 -b v1.0-branch \
    https://github.com/project-chip/connectedhomeip \
    && cp -r connectedhomeip/credentials /root/credentials \
    && rm -rf connectedhomeip \
    && apt-get purge -y --auto-remove \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/src/*

# hadolint ignore=DL3013
RUN \
    pip3 install \
    home-assistant-chip-clusters==${HOME_ASSISTANT_CHIP_VERSION} \
    home-assistant-chip-core==${HOME_ASSISTANT_CHIP_VERSION} \
    && pip3 install --no-cache-dir python-matter-server=="${MATTER_SERVER_VERSION}"

COPY docker-entrypoint.sh ./

VOLUME ["/data"]
EXPOSE 5580

ENTRYPOINT ["./docker-entrypoint.sh"]
