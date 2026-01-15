Name: gdal
Version: %{gdal_version}
Release: %{gdal_release}%{?dist}
Summary: Geospatial Data Abstraction Library
License: MIT
URL: https://gdal.org/

Source0: http://download.osgeo.org/gdal/%{version}/gdal-%{version}.tar.gz
Source1: https://github.com/google/brunsli.git

%define debug_package %{nil}

# Add python3-numpy to ensure bindings are built with array support
BuildRequires: python3-numpy
BuildRequires: python3-devel
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
BuildRequires: protobuf-c-devel

%description
GDAL is a translator library for raster and vector geospatial data formats.

%prep
%setup -q -n gdal-%{version}
# Explicitly download the source (if source0 fails or for redundancy)
wget -O gdal-%{version}.tar.gz http://download.osgeo.org/gdal/%{version}/gdal-%{version}.tar.gz
export LD_LIBRARY_PATH=:/usr/local/lib:$LD_LIBRARY_PATH

# Download Brunsli source
pushd %{_builddir}
git clone --depth=1 https://github.com/google/brunsli.git brunsli
pushd brunsli
git submodule update --init --recursive
popd
popd

# Build Brunsli
%build
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
# Note: "target install" here installs to the Docker build container /usr/local
# This is needed so ldconfig works and subsequent checks pass
cmake --build . --config Release --target install
ldconfig
popd

%install
pushd build
# Explicitly install to /usr/local inside the buildroot
cmake --install . --prefix %{buildroot}/usr/local

# Removed the manual "pip install" line. 
# CMake -DBUILD_PYTHON_BINDINGS=ON handles this automatically.

# Brunsli: Copy libraries and headers to the RPM buildroot
mkdir -p %{buildroot}/usr/local/lib/
mkdir -p %{buildroot}/usr/local/include/brunsli
cp -a /usr/local/lib/libbrunsli*.so* %{buildroot}/usr/local/lib/
cp -a /usr/local/include/brunsli/* %{buildroot}/usr/local/include/brunsli/
popd

%files
%doc README.md
%doc LICENSE.TXT

# Capture all files installed to /usr/local
/usr/local/bin/*
/usr/local/lib/*
/usr/local/include/*
/usr/local/share/*
/usr/local/lib64/*
