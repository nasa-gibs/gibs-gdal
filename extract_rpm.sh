#!/bin/sh

# This script extracts the built RPM file from the Docker image.

set -e

# Source the version information
. "$(dirname "$0")/version.sh"
OUTPUT_DIR="./dist/${RPM_VERSION}"

# Ensure the output directory exists
mkdir -p "${OUTPUT_DIR}"

# Create a temporary container from the image
echo "Creating temporary container from ${IMAGE_NAME}..."
CONTAINER_ID=$(docker create "${IMAGE_NAME}")

# The Dockerfile places the RPMs in the /output directory.
# We copy them from the container to the local filesystem.
echo "Copying RPMs from container to ${OUTPUT_DIR}..."
docker cp "${CONTAINER_ID}:/output/." "${OUTPUT_DIR}"

# Remove the temporary container
echo "Cleaning up temporary container..."
docker rm "${CONTAINER_ID}" > /dev/null

echo "\nSuccessfully extracted RPMs to ${OUTPUT_DIR}:"
ls -l "${OUTPUT_DIR}"
