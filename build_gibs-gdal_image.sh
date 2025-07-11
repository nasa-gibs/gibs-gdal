#!/bin/sh

# Source the version information
. "$(dirname "$0")/version.sh"

# Detect CPU architecture
ARCH=$(uname -m)
DOCKER_PLATFORM_OPTION=""

if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    DOCKER_PLATFORM_OPTION="--platform=linux/amd64"
fi

# Build the _gdal_dev image
docker build \
    --no-cache \
    $DOCKER_PLATFORM_OPTION \
    --build-arg ALMA_VERSION="${ALMA_VERSION}" \
    --build-arg GDAL_VERSION="${GDAL_VERSION}" \
    --build-arg GDAL_RELEASE="${GDAL_RELEASE}" \
    -f ./docker/Dockerfile \
    -t "${IMAGE_NAME}" \
    .
