%global  __requires_exclude devel\\(/lib/libNoVersion\\)

%define  major   5
%define  libname %mklibname geotiff %{major}
%define  libdev  %mklibname geotiff -d

Name:           geotiff
Summary:        Cartographic software
Version:        1.6.0
Release:        1
Group:          Sciences/Geosciences
License:        MIT-like
URL:            https://github.com/OSGeo/libgeotiff
#https://github.com/OSGeo/libgeotiff/archive/libgeotiff-%%{version}.tar.gz
Source0:        http://download.osgeo.org/geotiff/libgeotiff/libgeotiff-%{version}.tar.gz
BuildRequires:  pkgconfig(libtiff-4) >= 3.6.0
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(proj)

Requires:       proj

Conflicts:      %libname < 1.4.2-7

%description
This library is designed to permit the extraction and parsing of the
"GeoTIFF" Key directories, as well as definition and installation
of GeoTIFF keys in new files.

%package -n %libname
Summary:        Cartographic software - Libraries
Group:          Sciences/Geosciences

%description -n %libname
This library is designed to permit the extraction and parsing of the
"GeoTIFF" Key directories, as well as definition and installation
of GeoTIFF keys in new files. For more information about GeoTIFF
specifications, projection codes and use, see the WWW web page at:

%package -n %libdev
Summary:        Cartographic software - Development files
Group:          Sciences/Geosciences
Requires:       %libname = %{version}
Provides:       geotiff-devel = %{version}-%{release}
Obsoletes:      %{libname}-devel

%description -n %libdev
libgeotiff development files.

%prep
%setup -q -n libgeotiff-%{version}
%autopatch -p1

%build
%configure \
	--disable-static \
	--includedir=%{_includedir}/lib%{name}/ \
	--with-jpeg \
	--with-zip \
	--enable-incode-epsg
%make_build

%install
%make_install

chmod 644 %{buildroot}%{_includedir}/lib%{name}/*

# install manualy some file
install -p -m 755 bin/makegeo %{buildroot}%{_bindir}

# install pkgconfig file
cat > %{name}.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/lib%{name}

Name: %{name}
Description: GeoTIFF file format library
Version: %{version}
Libs: -L\${libdir} -lgeotiff
Cflags: -I\${includedir}
EOF

mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -p -m 644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

find %{buildroot} -name '*.la' -delete

%files
%license LICENSE
%doc ChangeLog
%{_bindir}/geotifcp
%{_bindir}/applygeo
%{_bindir}/listgeo
%{_bindir}/makegeo
%{_mandir}/man1/*.1*

%files -n %libname
%{_libdir}/*.so.%{major}{,.*}

%files -n %libdev
%{_libdir}/*.so
%{_includedir}/lib%{name}/
%{_libdir}/pkgconfig/%{name}.pc
