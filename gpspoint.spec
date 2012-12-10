%define major		1
%define libname		%mklibname %{name} %major
%define develname	%mklibname %{name} -d

Name: 	 	gpspoint
Summary: 	Garmin GPS data transfer utility
Version: 	2.030521
Release: 	7
Source0:	%{name}-%{version}.tar.bz2
# These patches are build fixes, from NetBSD - AdamW 2008/08
Patch0:		gpspoint-2.030521-netbsd-patch-ab
Patch1:		gpspoint-2.030521-netbsd-patch-ac
Patch2:		gpspoint-2.030521-netbsd-patch-ad
Patch3:		gpspoint-2.030521-netbsd-patch-ae
Patch4:		gpspoint-2.030521-netbsd-patch-af
# GCC 4.3 build fixes, by me - AdamW 2008/08
Patch5:		gpspoint-2.030521-gcc43.patch
Patch6:		gpspoint-2.030521-link.patch
License:	GPLv2+
Group:		Communications

%description
With gpspoint you can interact with a Garmin GPS device. Most
importantly you can download and upload waypoints, routes and tracks.
It also includes a dialog-based frontend, mgpspoint.

%package -n 	%{libname}
Summary:        Dynamic libraries from %{name}
Group:          System/Libraries

%description -n %{libname}
Dynamic libraries from %{name}.

%package -n 	%{develname}
Summary: 	Header files and static libraries from %{name}
Group: 		Development/C
Requires: 	%{libname} >= %{version}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%{name}-devel
Obsoletes:	%{mklibname gpspoint 1 -d}

%description -n %{develname}
Development libraries and headers for developing programs based on
%{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p1 -b .gcc43
%patch6 -p0 -b .link

%build
autoreconf -fi
%configure2_5x --disable-static
make
										
%install
rm -rf %{buildroot}
%makeinstall_std

#menu
mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=m%{name}
Icon=more_applications_other_section
Name=MGPSPoint
Comment=GPS Data Transfer
Categories=Utility;
EOF

%files
%defattr(-,root,root)
%doc README AUTHORS ChangeLog COPYRIGHT NEWS TODO
%{_bindir}/%{name}
%{_bindir}/m%{name}
%{_mandir}/man1/*
%{_datadir}/applications/mandriva-%{name}.desktop

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/gpspoint2
%{_libdir}/*.so



%changelog
* Fri Feb 19 2010 Funda Wang <fwang@mandriva.org> 2.030521-7mdv2010.1
+ Revision: 508369
- fix linkage

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sat Aug 23 2008 Adam Williamson <awilliamson@mandriva.org> 2.030521-6mdv2009.0
+ Revision: 275285
- package COPYRIGHT not COPYING
- protect major in file list (not like it's ever going to increment...heh)
- add gcc43.patch: fix build with GCC 4.3
- add netbsd-patch-ab through netbsd-patch-af: from NetBSD, build fixes
- new devel policy
- new license policy
- spec clean

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - auto convert menu to XDG
    - kill re-definition of %%buildroot on Pixel's request
    - use %%mkrel
    - import gpspoint

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Sat Jun 5 2004 Austin Acton <austin@mandrake.org> 2.030521-4mdk
- new menu
- configure 2.5

* Fri Feb 20 2004 David Baudens <baudens@mandrakesoft.com> 2.030521-3mdk
- Fix menu

* Tue Jul 15 2003 Austin Acton <aacton@yorku.ca> 2.030521-2mdk
- rebuild for rpm

* Fri May 23 2003 Austin Acton <aacton@yorku.ca> 2.030521-1mdk
- initial package
