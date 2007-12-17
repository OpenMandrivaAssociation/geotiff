
%define  _requires_exceptions devel(/lib/libNoVersion)

Name: geotiff
Summary: Cartographic software
Version: 1.2.4
Release: %mkrel 1
Group: Sciences/Geosciences
Source0: libgeotiff-%{version}.tar.gz
License: MIT style
URL: http://www.remotesensing.org/geotiff/geotiff.html
Requires: proj
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

%files 
%defattr(-,root,root)
%{_bindir}/*
%doc docs/*

#------------------------------------------------------------

%define libname %mklibname geotiff 1

%package -n %libname
Summary: Cartographic software - Libraries
Group: Sciences/Geosciences

%description -n %libname
This library is designed to permit the extraction and parsing of the
"GeoTIFF" Key directories, as well as definition and installation
of GeoTIFF keys in new files. For more information about GeoTIFF
specifications, projection codes and use, see the WWW web page at:

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -n %libname
%defattr(-,root,root)
%{_libdir}/*.so.*

#------------------------------------------------------------

%define libdev %mklibname geotiff -d

%package -n %libdev
Summary: Cartographic software - Development files
Group: Sciences/Geosciences
Requires: %libname = %{version}
Provides: geotiff-devel = %{version}-%{release}
Requires: libtiff-devel >= 3.6.0
Obsoletes: %{libname}-devel

%description -n %libdev
libgeotiff development files.

%files -n %libdev
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/*.a

%prep
%setup -q -n libgeotiff-%version

%build

%configure \
	--with-proj=%{_prefix} \
	--with-jpeg=%{_prefix} \
	--with-libtiff=%{_prefix} \
    --without-static \
	--enable-incode-epsg

make COPTS="$RPM_OPT_FLAGS -fPIC" LDFLAGS="$LDFLAGS -lc"

%install
rm -Rf %{buildroot}
%makeinstall
chmod 644 $RPM_BUILD_ROOT%{_includedir}/*

rm -rf $RPM_BUILD_ROOT%_datadir/*.csv

%clean
rm -rf $RPM_BUILD_ROOT



