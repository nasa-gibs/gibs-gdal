# This Dockerfile must be run from source root
ARG ALMA_VERSION
FROM almalinux:${ALMA_VERSION}

# Define build arguments and set them as environment variables
ARG GDAL_VERSION
ARG GDAL_RELEASE
ENV GDAL_VERSION=$GDAL_VERSION \
    GDAL_RELEASE=$GDAL_RELEASE

# Add AlmaLinux vault repositories to allow us to use libxml2-devel-2.9.13
RUN cat > /etc/yum.repos.d/almalinux-vault.repo <<'EOF'
[appstream-vault]
name=AlmaLinux Vault 9.4 - AppStream
# mirrorlist=https://mirrors.almalinux.org/mirrorlist/$releasever/appstream
baseurl=https://repo.almalinux.org/vault/9.4/AppStream/$basearch/os/
enabled=1
gpgcheck=1
countme=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-AlmaLinux-9

[baseos-vault]
name=AlmaLinux Vault 9.4 - BaseOS
baseurl=https://repo.almalinux.org/vault/9.4/BaseOS/$basearch/os/
enabled=1
gpgcheck=1
countme=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-AlmaLinux-9
EOF

ADD https://repo.almalinux.org/almalinux/RPM-GPG-KEY-AlmaLinux-9 /etc/pki/rpm-gpg/RPM-GPG-KEY-AlmaLinux-9

RUN dnf install -y dnf-plugins-core
# Install dependencies
RUN dnf -y update && \
    dnf groupinstall -y "Development Tools" && \
    dnf clean all && \
    dnf config-manager --set-enabled crb && \
        dnf install -y epel-release && \
    dnf install -y \
        --enablerepo="appstream-vault" \
        --enablerepo="baseos-vault" \
        swig-4.3.0 \
        rpm-build-4.19.1.1 \
        rpmdevtools-9.6 \
        jansson-devel-2.14 \
        libpng-devel-1.6.40 \
        pcre2-devel-10.44 \
        wget-1.24.5 \
        libyaml-devel-0.2.5 \
        libcurl-devel-8.9.1 \
        libjpeg-turbo-devel-3.0.2 \
        libxml2-devel-2.9.13 \
        cronie-1.7.0 \
        logrotate-3.22.0 \
        fribidi-devel-1.0.14 \
        cairo-devel-1.18.2 \
        cmake-3.30.5 \
        harfbuzz-devel-8.4.0 \
        fcgi-devel-2.4.0 \
        proj-9.5.0 \
        proj-devel-9.5.0 \
        geos-3.13.0 \
        geos-devel-3.13.0 \
        python3-numpy-1.26.4 \
        python3-devel-3.12.9 \
        protobuf-c-devel-1.5.0 && \
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
    /root/rpmbuild/SPECS/gdal.spec
# Copy the built RPM to the output directory
RUN mkdir -p ../output
RUN cp /root/rpmbuild/RPMS/x86_64/*.rpm ../output

WORKDIR /
RUN rm -rf /tmp

