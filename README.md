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

git clone\
cd gdal-brunsli-rpm\
docker build -t gdal-builder .\
docker run -it -v $(pwd)/output:/output gdal-builder\
   
 ## RPM Installation
   sudo dnf install /path/to/gdal-3.6.4-1.el9.x86_64.rpm
   
## Verification
    Run gdalinfo --version
## Brunsli Support
    gdal_translate -of JPEG2000 -co QUALITY=50 input.tif output.jp2 #Brunsli Support
    Compare the file size of output.jp2 with a JPEG2000 file generated without Brunsli. The Brunsli-compressed file should be 22% smaller.

## Customization
    *GDAL Version: Change the GDAL_VERSION argument in the Dockerfile to build a different version of GDAL.
    *Dependencies: Adjust the dnf install commands in the Dockerfile to install any additional dependencies required for your specific needs.
    *CMake Options: Modify the CMake options in the %build section of the gdal.spec file to customize the GDAL build.
    *Output Directory: Change the volume mount in the docker run command to specify a different output directory for the RPM package.

## License
    *This project is licensed under the Apache License, Version 2.0 - see the LICENSE  file for details
