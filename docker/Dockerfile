# This Dockerfile must be run from source root
ARG ALMA_VERSION
FROM almalinux:${ALMA_VERSION}

# Define build arguments and set them as environment variables
ARG GDAL_VERSION
ARG GDAL_RELEASE
ENV GDAL_VERSION=$GDAL_VERSION \
    GDAL_RELEASE=$GDAL_RELEASE

# Install EPEL and enable CRB
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-10.noarch.rpm && \
    dnf install -y dnf-plugins-core && \
    dnf config-manager --set-enabled crb && \
    dnf clean all

# Install Build Dependencies
# Added python3-setuptools and python3-wheel here so rpmbuild finds them in /usr/lib
RUN dnf install -y \
    rpmdevtools \
    dnf-utils \
    rpm-build \
    gcc \
    gcc-c++ \
    make \
    cmake \
    swig \
    wget \
    git \
    # GIS Dependencies
    proj-devel \
    geos-devel \
    fribidi-devel \
    cairo-devel \
    harfbuzz-devel \
    fcgi-devel \
    protobuf-c-devel \
    # Lib Dependencies
    libpng-devel \
    libjpeg-turbo-devel \
    libcurl-devel \
    libxml2-devel \
    libyaml-devel \
    jansson-devel \
    pcre2-devel \
    # Python & Utils
    python3-devel \
    python3-setuptools \
    python3-wheel \
    python3-pip \
    cronie \
    logrotate && \
    dnf clean all

# Python Environment Setup
# Upgrade via pip and use PYTHONPATH to prioritize the pip version.

RUN pip install --upgrade pip==25.3 && \
    pip install numpy==1.26.4 "packaging>=25.0" setuptools wheel --ignore-installed

# Setup RPM Build Tree
WORKDIR /root
RUN mkdir -p rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Copy SPEC file
COPY rpmbuild/SPECS/gdal.spec /root/rpmbuild/SPECS/

# Ensure spectool is installed
RUN dnf install -y rpmdevtools

# 6. Download Source files
RUN spectool -g \
    --define "gdal_version $GDAL_VERSION" \
    --define "gdal_release $GDAL_RELEASE" \
    -C /root/rpmbuild/SOURCES \
    /root/rpmbuild/SPECS/gdal.spec

# Build the RPM
# Set PYTHONPATH so rpmbuild prefers our pip-installed numpy/packaging in /usr/local
ENV PYTHONPATH=/usr/local/lib64/python3.12/site-packages:/usr/local/lib/python3.12/site-packages

RUN rpmbuild -bb --clean --nodeps \
    --define "gdal_version $GDAL_VERSION" \
    --define "gdal_release $GDAL_RELEASE" \
    /root/rpmbuild/SPECS/gdal.spec

# Copy the built RPM to the output directory
RUN mkdir -p ../output
RUN cp /root/rpmbuild/RPMS/x86_64/*.rpm ../output

WORKDIR /
RUN rm -rf /tmp
