%define major	1.2
%define libname %mklibname geotiff %{major}
%define devname %mklibname geotiff -d

Summary:	Cartographic software
Name:		geotiff
Version:	1.2.5
Release:	12
Group:		Sciences/Geosciences
License:	MIT style
Url:		http://trac.osgeo.org/geotiff/
Source0:	ftp://ftp.remotesensing.org/pub/geotiff/libgeotiff/libgeotiff-%{version}.tar.gz
#Source100:	geotiff.rpmlintrc
# fix build
Patch0:		libgeotiff-soname.patch
Patch1:		libgeotiff-1.2.5-fix-str-fmt.patch

BuildRequires:	doxygen
BuildRequires:	jpeg-devel 
BuildRequires:	tiff-devel >= 3.6.0 
BuildRequires:	pkgconfig(proj)
BuildRequires:	pkgconfig(zlib)
Requires:	proj

%description
This library is designed to permit the extraction and parsing of the
"GeoTIFF" Key directories, as well as definition and installation
of GeoTIFF keys in new files.

%package -n %{libname}
Summary:	Cartographic software - Libraries
Group:		Sciences/Geosciences
Obsoletes:	%{_lib}geotiff1 < 1.2.5-5

%description -n %{libname}
This package contains a shared library for %{name}.

%package -n %{devname}
Summary:	Cartographic software - Development files
Group:		Sciences/Geosciences
Requires:	%{libname} = %{version}
Provides:	geotiff-devel = %{version}-%{release}

%description -n %{devname}
libgeotiff development files.

%prep
%setup -qn libgeotiff-%{version}
%apply_patches

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

%make

%install
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

Name:	%{name}
Description:	GeoTIFF file format library
Version:	%{version}
Libs:	-L\${libdir} -lgeotiff
Cflags:	-I\${includedir}
EOF

mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -p -m 644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

#clean up junks
rm -rf %{buildroot}%{_datadir}/*.csv
rm -rf %{buildroot}%{_libdir}/*.a

# generate docs
doxygen

%files 
%doc docs/*
%{_bindir}/geotifcp
%{_bindir}/listgeo
%{_bindir}/makegeo

%files -n %{libname}
%{_libdir}/libgeotiff.so.1
%{_libdir}/libgeotiff.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc

