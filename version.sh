#!/bin/sh

# GDAL version information
export GDAL_VERSION="3.13.0"
export GDAL_RELEASE="2"

# AlmaLinux version
export ALMA_VERSION="10.0"

# RPM full version
export RPM_VERSION="${GDAL_VERSION}-${GDAL_RELEASE}.el${ALMA_VERSION%%.*}"

# Defines the Docker image name and tag for the project
export IMAGE_NAME="gibs/gibs-gdal:${GDAL_VERSION}-${GDAL_RELEASE}"
