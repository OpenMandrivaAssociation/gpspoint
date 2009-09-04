%define _disable_ld_as_needed		1
%define _disable_ld_no_undefined	1

%define major		1
%define libname		%mklibname %{name} %major
%define develname	%mklibname %{name} -d

Name: 	 	gpspoint
Summary: 	Garmin GPS data transfer utility
Version: 	2.030521
Release: 	%{mkrel 7}
Source0:	%{name}-%{version}.tar.bz2
# These patches are build fixes, from NetBSD - AdamW 2008/08
Patch0:		gpspoint-2.030521-netbsd-patch-ab
Patch1:		gpspoint-2.030521-netbsd-patch-ac
Patch2:		gpspoint-2.030521-netbsd-patch-ad
Patch3:		gpspoint-2.030521-netbsd-patch-ae
Patch4:		gpspoint-2.030521-netbsd-patch-af
# GCC 4.3 build fixes, by me - AdamW 2008/08
Patch5:		gpspoint-2.030521-gcc43.patch
License:	GPLv2+
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-buildroot

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

%build
%configure2_5x
%make
										
%install
rm -rf %{buildroot}
%makeinstall

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

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%endif
		
%if %mdkversion < 200900
%postun
%clean_menus
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

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
%{_libdir}/*.a
%{_libdir}/*.la

