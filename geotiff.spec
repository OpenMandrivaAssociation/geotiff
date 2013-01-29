%define major	1

Name: geotiff
Summary: Cartographic software
Version: 1.2.5
Release: 4
Group: Sciences/Geosciences
Source0: libgeotiff-%{version}.tar.gz
Source0: %{name}.rpmlintrc
# fix build
Patch0:    libgeotiff-soname.patch
Patch1:    libgeotiff-1.2.5-fix-str-fmt.patch
License: MIT style
URL: http://www.remotesensing.org/geotiff/geotiff.html
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

%files -n %libname
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

%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-3mdv2011.0
+ Revision: 610840
- rebuild

* Tue Feb 16 2010 Emmanuel Andry <eandry@mandriva.org> 1.2.5-2mdv2010.1
+ Revision: 506861
- fix files encoding
- fix build using gcc -shared instead of ld -shared
- install makegeo
- install pkgconfig file
- generate doxygen docs
- diff P1 to fix format string not literal

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild
    - fix description

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Dec 30 2007 Emmanuel Andry <eandry@mandriva.org> 1.2.4-1mdv2008.1
+ Revision: 139583
- add patch 0 from fedora to fix build

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Helio Chissini de Castro <helio@mandriva.com>
    - New upstream version
    - Recompiling for 2008.0
    - import geotiff-1.2.2-6mdk


* Wed May 11 2005 Buchan Milne <bgmilne@linux-mandrake.com> 1.2.2-6mdk
- fix devel requires

* Wed May 11 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.2.2-5mdk
- Fix URL and description ( thanks rgs)

* Wed May 11 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.2.2-4mdk
- Rebuild

* Mon May 09 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.2.2-3mdk
- Fix BuildRequires
- %%mkrel

* Thu May 27 2004 Olivier Blin <blino@mandrake.org> 1.2.2-2mdk
- merge changelog back

* Wed May 26 2004 Buchan Milne <bgmilne@linux-mandrake.com> 1.2.2-1mdk
- 1.2.2
- Put blino's fixes back

* Wed May 26 2004 Buchan Milne <bgmilne@linux-mandrake.com> 1.2.1-2mdk
-rebuild

* Wed Jan 07 2004 Olivier Blin <blino@mandrake.org> 1.1.4-7mdk
- Patch0: try to fix soname
- rename specfile to please rpmlint
- fix Groups
- fix License
- BuildRequires, drop redundant Requires
- rm -rf $RPM_BUILD_ROOT at beginning of %%install
- mklibname

* Fri Aug 08 2003 Buchan Milne <bgmilne@linux-mandrake.com> 1.2.1-1mdk
- 1.2.1
- fix libname
- drop manual link creation

* Mon Jul 14 2003 Buchan Milne <bgmilne@linux-mandrake.com> 1.2.0-1mdk
- 1.2.0
- build with system tiff (requires tiff>=3.6.0)
- tighten requires

* Wed Jan 29 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.1.4-6mdk
- rebuild

* Wed Oct 16 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.1.4-5mdk
- fix link

* Mon Sep 02 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.1.4-4mdk
- rebuild

* Thu Aug 29 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.1.4-3mdk
- rebuild

* Mon Aug 20 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.1.4-2mdk
- rebuild

* Thu Jun 14 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.1.4-1mdk
- added in contribs by Laurent Grawet <laurent.grawet@ibelgique.com>

