# This Dockerfile must be run from source root
FROM almalinux:latest

RUN dnf install -y dnf-plugins-core
# Install dependencies
RUN dnf -y update && \
    dnf groupinstall -y "Development Tools" && \
    dnf clean all && \
    dnf config-manager --set-enabled crb && \
        dnf install -y epel-release && \
    dnf install -y \
        swig \
        rpm-build \
        rpmdevtools \
        jansson-devel \
        libpng-devel \
        pcre-devel \
        wget \
        libyaml-devel \
        libcurl-devel \
        libjpeg-turbo-devel \
        libxml2-devel \
        cronie \
        logrotate \
        fribidi-devel \
        cairo-devel \
        cmake \
        harfbuzz-devel \
        fcgi-devel \
        proj \
        proj-devel \
        geos \
        geos-devel \
        python3-numpy \
        python3-devel \
        protobuf-c-devel && \
        dnf clean all

WORKDIR /tmp
RUN rpmdev-setuptree
# Copy SPEC file
COPY ../../rpmbuild/SPEC/gdal.spec /root/rpmbuild/SPECS/
# Build the RPM
RUN rpmbuild -bb --clean /root/rpmbuild/SPECS/gdal.spec
# Copy the built RPM to the output directory
RUN cp /root/rpmbuild/RPMS/x86_64/*.rpm /output/
