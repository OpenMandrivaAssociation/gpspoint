%define name	gpspoint
%define version	2.030521
%define release  %mkrel 4

%define major	1
%define libname %mklibname %name %major

Name: 	 	%{name}
Summary: 	Garmin GPS data transfer utility
Version: 	%{version}
Release: 	%{release}

Source:		%{name}-%{version}.tar.bz2
URL:		http://gpspoint.dnsalias.net/gpspoint2/
License:	GPL
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
With gpspoint you can interact with a garmin gps device. Most importantly you
can down- and upload waypoints, routes and tracks.  It also dialog based
frontend mgpspoint.

%package -n 	%{libname}
Summary:        Dynamic libraries from %name
Group:          System/Libraries
#Provides:	%name
#Obsoletes:	%name = %version-%release

%description -n %{libname}
Dynamic libraries from %name.

%package -n 	%{libname}-devel
Summary: 	Header files and static libraries from %name
Group: 		Development/C
Requires: 	%{libname} >= %{version}
Provides: 	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%name-devel

%description -n %{libname}-devel
Libraries and includes files for developing programs based on %name.

%prep
%setup -q

%build
%configure2_5x
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

#menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): command="m%{name}" \
icon="more_applications_other_section.png" \
needs="text" \
title="MGPSPoint" \
longtitle="GPS Data Transfer" \
section="More applications/Other"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
		
%postun
%clean_menus

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README AUTHORS ChangeLog COPYING NEWS TODO
%{_bindir}/%name
%{_bindir}/m%name
%{_mandir}/man1/*
%{_menudir}/%name

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/gpspoint2
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la

