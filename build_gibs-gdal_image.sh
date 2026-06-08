#!/bin/sh

# Source the version information
. "$(dirname "$0")/version.sh"

# Allow passing specific architectures as arguments, otherwise default to both
TARGET_ARCHS=${@:-"amd64 arm64"}

for ARCH in $TARGET_ARCHS; do
    echo "========================================="
    echo "Building ${IMAGE_NAME} for linux/${ARCH}..."
    echo "========================================="

    # Build the image for the specific architecture
    # We tag the image with the architecture so they don't overwrite each other
    docker build \
        --no-cache \
        --platform "linux/${ARCH}" \
        --build-arg ALMA_VERSION="${ALMA_VERSION}" \
        --build-arg GDAL_VERSION="${GDAL_VERSION}" \
        --build-arg GDAL_RELEASE="${GDAL_RELEASE}" \
        -f ./docker/Dockerfile \
        -t "${IMAGE_NAME}-${ARCH}" \
        .
done
