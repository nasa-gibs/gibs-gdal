# GDAL RPM Build with Brunsli Support

This project provides a Dockerfile and RPM spec file to build GDAL from source with Brunsli compression support.

## Overview

This project simplifies the process of building GDAL with Brunsli support by:

* **Dockerized Build:** Using a Docker image to provide a consistent and isolated build environment.
* **RPM Packaging:**  Creating an RPM package for distribution and installation on RPM-based systems.
* **Brunsli Integration:**  Including the necessary steps to build and integrate Brunsli into the GDAL build process.

## Prerequisites

* **Docker:** Make sure you have Docker installed and running on your system.
* **Git:**  Git is required to clone the Brunsli source code.

## Build Instructions

### Using the Build Script

The easiest way to build the GDAL Docker image with Brunsli support is to use the provided build script:

```bash
./build_gibs-gdal_image.sh
```

This script:
- Sources image name and version information from `version.sh`
- Detects CPU architecture and adds platform options if needed
- Passes version variables to the Docker build process
- Builds the Docker image using [docker/Dockerfile](docker/Dockerfile)


### Extracting the RPM

After building the Docker image, you can extract the RPM files using the provided script:

```bash
./extract_rpm.sh
```

This script:
- Creates a temporary container from the built image
- Copies the RPM files from the container to a local `./dist/${RPM_VERSION}` directory, where `${RPM_VERSION}` is automatically set based on the version information in `version.sh`.
- Removes the temporary container

## RPM Installation

```bash
sudo dnf install ./path/to/gdal-${RPM_VERSION}.x86_64.rpm
```
   
## Verification
    Run gdalinfo --version
## Brunsli Support
    gdal_translate -of JPEG2000 -co QUALITY=50 input.tif output.jp2 #Brunsli Support
    Compare the file size of output.jp2 with a JPEG2000 file generated without Brunsli. The Brunsli-compressed file should be 22% smaller.

## Customization

* **Version Information**: Edit the `version.sh` file to change the GDAL version, release number, or AlmaLinux version.
* **Dependencies**: Adjust the dnf install commands in the Dockerfile to install any additional dependencies required for your specific needs.
* **CMake Options**: Modify the CMake options in the `%build` section of the gdal.spec file to customize the GDAL build.
* **Output Directory**: The extracted RPMs will be placed in `./dist/${RPM_VERSION}` by default.

## License
    *This project is licensed under the Apache License, Version 2.0 - see the LICENSE  file for details
