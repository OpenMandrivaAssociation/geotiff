%define name geotiff
%define version 1.2.2
%define release %mkrel 6

%define major 1
%define libname %mklibname geotiff %{major}

%define  _requires_exceptions devel(/lib/libNoVersion)

Name:          %name
Summary:       Cartographic software
Version:       %version
Release:       %release
Source:        libgeotiff-%{version}.tar.bz2
Patch:         libgeotiff-%{version}-so_name.patch
License:       MIT style
URL:           http://www.remotesensing.org/geotiff/geotiff.html
Group:         Sciences/Geosciences
BuildRoot:     %{_tmppath}/%{name}-buildroot
Requires:      %{_lib}proj0 >= 4.4.3
BuildRequires: libtiff-devel >= 3.6.0 
BuildRequires: libjpeg-devel 
BuildRequires: zlib-devel 
BuildRequires: proj-devel

%description
This library is designed to permit the extraction and parsing of the
"GeoTIFF" Key directories, as well as definition and installation
of GeoTIFF keys in new files. For more information about GeoTIFF
specifications, projection codes and use, see the WWW web page at:

   http://www.remotesensing.org/geotiff/geotiff.html


%package -n %libname
Summary: Cartographic software - Libraries
Group: Sciences/Geosciences

%description -n %libname
This library is designed to permit the extraction and parsing of the
"GeoTIFF" Key directories, as well as definition and installation
of GeoTIFF keys in new files. For more information about GeoTIFF
specifications, projection codes and use, see the WWW web page at:

%package -n %libname-devel
Summary: Cartographic software - Development files
Group: Sciences/Geosciences
License: MIT style
Requires: %libname = %{version}-%{release}
Provides: libgeotiff-devel = %{version}-%{release}
Provides: geotiff-devel = %{version}-%{release}
Requires: libtiff-devel >= 3.6.0

%description -n %libname-devel
libgeotiff development files.

%prep
%setup -q -n libgeotiff-%version
%patch -p1

%build

%configure \
	--with-proj=%{_prefix} \
	--with-jpeg=%{_prefix} \
	--with-libtiff=%{_prefix} \
	--enable-incode-epsg

make COPTS="$RPM_OPT_FLAGS -fPIC" LDFLAGS="$LDFLAGS -lc"

%install
rm -Rf %{buildroot}
%makeinstall
chmod 644 $RPM_BUILD_ROOT%{_includedir}/*

rm -rf $RPM_BUILD_ROOT%_datadir/*.csv

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%files 
%defattr(-,root,root)
%{_bindir}/*
%doc docs/*

%files -n %libname
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %libname-devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/*.a

