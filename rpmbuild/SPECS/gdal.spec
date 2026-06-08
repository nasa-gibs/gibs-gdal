Name: gdal
Version: %{gdal_version}
Release: %{gdal_release}%{?dist}
Summary: Geospatial Data Abstraction Library
License: MIT
URL: https://gdal.org/

Source0: http://download.osgeo.org/gdal/%{version}/gdal-%{version}.tar.gz

%define debug_package %{nil}

BuildRequires: gcc
BuildRequires: make
BuildRequires: cmake
BuildRequires: jansson-devel
BuildRequires: libpng-devel
BuildRequires: pcre2-devel
BuildRequires: wget
BuildRequires: libyaml-devel
BuildRequires: libcurl-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libxml2-devel
BuildRequires: cronie
BuildRequires: logrotate
BuildRequires: fribidi-devel
BuildRequires: cairo-devel
BuildRequires: harfbuzz-devel
BuildRequires: fcgi-devel
BuildRequires: proj-devel
BuildRequires: geos-devel
BuildRequires: python3-devel
BuildRequires: protobuf-c-devel
# AlmaLinux 10 native zlib-ng
BuildRequires: zlib-ng-compat-devel

%description
GDAL is a translator library for raster and vector geospatial data formats.

%prep
%setup -q -n gdal-%{version}

export LD_LIBRARY_PATH=:/usr/local/lib:$LD_LIBRARY_PATH

# Download Brunsli source
pushd %{_builddir}
git clone --depth=1 https://github.com/google/brunsli.git brunsli
pushd brunsli
git submodule update --init --recursive
popd
popd

%build
# Build Brunsli
pushd %{_builddir}/brunsli
mkdir build
pushd build
cmake -DCMAKE_PREFIX_PATH=/usr/local -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_BUILD_TYPE=Release -B out .. && \
cmake --build out --config Release && \
pushd out && \
make %{?_smp_mflags} && \
make install && \
popd && \
ldconfig
popd
popd

# Build GDAL
mkdir build
pushd build
cmake -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_PREFIX_PATH=/usr/local \
      -DCMAKE_INSTALL_PREFIX=/usr/local \
      -DCMAKE_INSTALL_LIBDIR=lib \
      -DBUILD_SHARED_LIBS=ON \
      -DBUILD_TESTING=OFF \
      -DGDAL_USE_PARQUET=OFF \
      -DGDAL_USE_ARROW=OFF \
      -DGDAL_USE_ARROWDATASET=OFF \
      -DGDAL_ENABLE_HDF5_GLOBAL_LOCK:BOOL=ON \
      -DGDAL_USE_BRUNSLI=ON \
      -DBRUNSLI_INCLUDE_DIR=/usr/local/include/brunsli \
      -DBUILD_PYTHON_BINDINGS:BOOL=ON \
      -DBUILD_JAVA_BINDINGS:BOOL=OFF \
      -DBUILD_CSHARP_BINDINGS:BOOL=OFF \
      ..

cmake --build .
popd

%install
pushd build
# Install GDAL directly into the RPM buildroot
cmake --install . --prefix %{buildroot}/usr/local

# Temporarily add the buildroot bin directory to PATH so pip can find gdal-config
export PATH="%{buildroot}/usr/local/bin:$PATH"
export GDAL_CONFIG="%{buildroot}/usr/local/bin/gdal-config"

# Force the compiler AND linker to look inside the buildroot for headers and libraries
export C_INCLUDE_PATH="%{buildroot}/usr/local/include"
export CPLUS_INCLUDE_PATH="%{buildroot}/usr/local/include"
export LIBRARY_PATH="%{buildroot}/usr/local/lib:%{buildroot}/usr/local/lib64"

# Install Python bindings into the RPM buildroot
pip install --root=%{buildroot} --prefix=/usr/local GDAL==%{version}

# Create custom library and header paths
mkdir -p %{buildroot}/usr/local/lib/
mkdir -p %{buildroot}/usr/local/include/brunsli

# Copy Brunsli into the RPM payload
cp /usr/local/lib/libbrunsli*.so* %{buildroot}/usr/local/lib/
cp /usr/local/include/brunsli/* %{buildroot}/usr/local/include/brunsli/
popd

# Strip debug symbols from all shared objects to remove embedded buildroot paths.
# We append || true so the build doesn't fail if strip encounters a non-strippable file.
find %{buildroot} -type f -name "*.so" -exec strip {} \; || true

%files
%doc README.md
%doc LICENSE.TXT

# Removed /usr/bin, /usr/lib, etc., because CMake is configured 
# with -DCMAKE_INSTALL_PREFIX=/usr/local. We only want to package local.
/usr/local/bin/*
/usr/local/lib/*
/usr/local/lib64/*
/usr/local/include/*
/usr/local/include/brunsli/*
/usr/local/share/*

%changelog
* Fri Jun 05 2026 Custom Build <custom@example.com> - %{version}-%{release}
- Custom GDAL Docker build with native zlib-ng and Brunsli

