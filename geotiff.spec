
%define  _requires_exceptions devel(/lib/libNoVersion)
%define major	1

Name: geotiff
Summary: Cartographic software
Version: 1.2.5
Release: %mkrel 2
Group: Sciences/Geosciences
Source0: libgeotiff-%{version}.tar.gz
# fix build
Patch0:    libgeotiff-soname.patch
Patch1:    libgeotiff-1.2.5-fix-str-fmt.patch
License: MIT style
URL: http://www.remotesensing.org/geotiff/geotiff.html
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires: proj
BuildRequires: libtiff-devel >= 3.6.0 
BuildRequires: libjpeg-devel 
BuildRequires: zlib-devel 
BuildRequires: proj-devel
BuildRequires: doxygen

%description
This library is designed to permit the extraction and parsing of the
"GeoTIFF" Key directories, as well as definition and installation
of GeoTIFF keys in new files.

%files 
%defattr(-,root,root)
%{_bindir}/geotifcp
%{_bindir}/listgeo
%{_bindir}/makegeo
%doc docs/*

#------------------------------------------------------------

%define libname %mklibname geotiff %{major}

%package -n %libname
Summary: Cartographic software - Libraries
Group: Sciences/Geosciences

%description -n %libname
This library is designed to permit the extraction and parsing of the
"GeoTIFF" Key directories, as well as definition and installation
of GeoTIFF keys in new files. For more information about GeoTIFF
specifications, projection codes and use, see the WWW web page at:

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -n %libname
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

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
%{_libdir}/pkgconfig/%{name}.pc

%prep
%setup -q -n libgeotiff-%version
%patch0 -p1 -b .soname~
%patch1 -p0

# fix wrongly encoded files from tarball
 	set +x
 	for f in `find . -type f` ; do
 	if file $f | grep -q ISO-8859 ; then
 	set -x
 	iconv -f ISO-8859-1 -t UTF-8 $f > ${f}.tmp && \
 	mv -f ${f}.tmp $f
 	set +x
 	fi
 	if file $f | grep -q CRLF ; then
 	set -x
 	sed -i -e 's|\r||g' $f
 	set +x
 	fi
 	done
 	set -x 

%build

# disable -g flag removal
 	sed -i 's| \| sed \"s\/-g \/\/\"||g' configure
 	
# use gcc -shared instead of ld -shared to build with -fstack-protector
 	sed -i 's|LD_SHARED=@LD_SHARED@|LD_SHARED=@CC@ -shared|' Makefile.in 

%configure2_5x \
	--with-proj=%{_prefix} \
	--with-jpeg=%{_prefix} \
	--with-libtiff=%{_prefix} \
    	--without-static \
	--enable-incode-epsg

make COPTS="$RPM_OPT_FLAGS -fPIC" LDFLAGS="$LDFLAGS -lc"

%install
rm -Rf %{buildroot}
%makeinstall
chmod 644 %{buildroot}%{_includedir}/*

# install manualy some file
install -p -m 755 bin/makegeo %{buildroot}%{_bindir}

# install pkgconfig file
cat > %{name}.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/%{name}

Name: %{name}
Description: GeoTIFF file format library
Version: %{version}
Libs: -L\${libdir} -lgeotiff
Cflags: -I\${includedir}
EOF

mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -p -m 644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

#clean up junks
rm -rf %{buildroot}%{_datadir}/*.csv

# generate docs
doxygen

%clean
rm -rf %{buildroot}



