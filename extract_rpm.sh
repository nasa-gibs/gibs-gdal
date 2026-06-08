#!/bin/sh

# This script extracts the built RPM files from the Docker images.

set -e

# Source the version information
. "$(dirname "$0")/version.sh"

# Allow passing specific architectures as arguments, otherwise default to both
TARGET_ARCHS=${@:-"amd64 arm64"}
#TARGET_ARCHS=${@:-"arm64"}

for ARCH in $TARGET_ARCHS; do
    echo "========================================="
    echo "Extracting RPMs for linux/${ARCH}..."
    echo "========================================="

    # Make output directory architecture-specific to prevent overwriting
    OUTPUT_DIR="./dist/${RPM_VERSION}/${ARCH}"
    
    # Ensure the output directory exists
    mkdir -p "${OUTPUT_DIR}"

    # Create a temporary container from the architecture-specific image
    echo "Creating temporary container from ${IMAGE_NAME}:${ARCH}..."
    CONTAINER_ID=$(docker create "${IMAGE_NAME}-${ARCH}")

    # The Dockerfile places the RPMs in the /output directory.
    # We copy them from the container to the local filesystem.
    echo "Copying RPMs from container to ${OUTPUT_DIR}..."
    docker cp "${CONTAINER_ID}:/output/." "${OUTPUT_DIR}"

    # Remove the temporary container
    echo "Cleaning up temporary container..."
    docker rm "${CONTAINER_ID}" > /dev/null

    echo ""
    echo "Successfully extracted RPMs for ${ARCH} to ${OUTPUT_DIR}:"
    ls -l "${OUTPUT_DIR}"
    echo ""
done
