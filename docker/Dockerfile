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
# Need to copy SPEC file 
