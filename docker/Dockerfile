# This Dockerfile must be run from source root
FROM almalinux:10.0

# Define build arguments and set them as environment variables
ARG GDAL_VERSION
ARG GDAL_RELEASE
ENV GDAL_VERSION=$GDAL_VERSION \
    GDAL_RELEASE=$GDAL_RELEASE \
    OPENSSL_ia32cap="0"

# Update system, configure repositories, and install pinned dependencies
RUN dnf -y update && \
    dnf groupinstall -y "Development Tools" && \
    dnf install -y 'dnf-command(config-manager)' && \
    dnf install -y 'almalinux-release-devel' && \
    dnf clean all && \
    dnf config-manager --set-enabled crb && \
    dnf config-manager --set-enabled devel && \
    dnf install -y epel-release-10-6.el10 && \
    dnf install -y \
        rpm-build \
        rpmdevtools \
        swig \
        python3-numpy-1.26.4 \
        python3-setuptools \
        python3-wheel \
        fcgi-devel-2.4.7-1.el10_2 \
        proj-9.6.0 \
        proj-devel-9.6.0 \
        fribidi-devel-1.0.14 \
        cairo-devel-1.18.2 \
        cmake \
        geos-3.13.1 \
        geos-devel-3.13.1 \
        harfbuzz-devel-8.4.0 \
        protobuf-c-devel-1.5.0 \
        lua-devel-5.4.6 \
        jansson-devel-2.14 \
        libpng-devel-1.6.40 \
        pcre2-devel-10.44 \
        wget-1.24.5 \
        libyaml-devel-0.2.5 \
        libcurl-devel-8.12.1 \
        libjpeg-turbo-devel-3.0.2 \
        libxml2-devel-2.12.5 \
        mod_ssl-1:2.4.63 \
        openssl-devel \
        luarocks-3.9.2 \
        redis \
        cronie-1.7.0 \
        logrotate-3.22.0 \
        python3-devel \
        zlib-ng-compat-devel \
        parallel && \
    dnf clean all

WORKDIR /tmp
RUN rpmdev-setuptree

# Copy SPEC file
COPY ../../rpmbuild/SPECS/gdal.spec /root/rpmbuild/SPECS/

# Download source files
RUN spectool -g -R --define "gdal_version $GDAL_VERSION" --define "gdal_release $GDAL_RELEASE" /root/rpmbuild/SPECS/gdal.spec

# Build the RPM
RUN rpmbuild -bb --clean \
    --define "gdal_version $GDAL_VERSION" \
    --define "gdal_release $GDAL_RELEASE" \
    --define "_unpackaged_files_terminate_build 0" \
    /root/rpmbuild/SPECS/gdal.spec

# Copy the built RPM to the output directory
RUN mkdir -p ../output
# Use a wildcard for the architecture directory so it works for x86_64, aarch64, and noarch
RUN cp /root/rpmbuild/RPMS/*/*.rpm ../output

WORKDIR /
RUN rm -rf /tmp
