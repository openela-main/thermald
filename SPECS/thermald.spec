# Explicitly turn on hardening, if required.
%if 0%{?rhel} && 0%{?rhel} <= 7
%global _hardened_build 1
%endif

%global pkgname thermal_daemon


Name:		thermald
Version:	2.5.1
Release:	1%{?dist}
Summary:	Thermal Management daemon

License:	GPLv2+
URL:		https://github.com/intel/%{pkgname}
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# No cpuid.h on other arches.
ExclusiveArch:	%{ix86} x86_64

BuildRequires:	autoconf autoconf-archive
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gcc-c++
BuildRequires:	libxml2-devel
BuildRequires:	systemd-devel
BuildRequires:  upower-devel
BuildRequires:  libevdev-devel
BuildRequires:  gtk-doc

Requires:	dbus%{?_isa}

Requires(pre):	glibc-common
Requires(pre):	shadow-utils

%{?systemd_requires}

# Upstream removed the internal copy of qcustomplot, add it back as we don't have it in RHEL.
# The alternative would be removing the GUI package
Patch9000:      qcustomplot.patch
# G_SOURCE_FUNC only exists with GLib >= 2.58
Patch9001:      g-source-func.patch

%description
%{name} monitors and controls platform temperature.

Thermal issues are important to handle proactively to reduce performance
impact.  %{name} uses the existing Linux kernel infrastructure and can
be easily enhanced.


%package monitor
Summary:	Application for monitoring %{name}
License:	GPLv3+

BuildRequires:	qt5-qtbase-devel

Requires:	hicolor-icon-theme
Requires:	%{name}%{?_isa}		== %{version}-%{release}

%description monitor
This package contains an Application to monitor %{name} for system
developers who want to enable application developers and their
customers with the responsive and flexible thermal management,
supporting optimal performance in desktop, clam-shell, mobile and
embedded devices.


%prep
%autosetup -n %{pkgname}-%{version} -p 1

# Create tmpfiles.d config.
%{__mkdir} -p fedora_addons
%{__cat} << EOF > fedora_addons/%{name}.conf
d %{_rundir}/%{name} 0755 root root -
EOF

# Create desktop-file for the monitor-app.
%{__cat} << EOF > fedora_addons/%{name}-monitor.desktop
[Desktop Entry]
Name=%{name} Monitor
Comment=Application for monitoring %{name}
Icon=%{name}-monitor
Categories=System;Settings;
Exec=%{_bindir}/ThermalMonitor
Type=Application
StartupNotify=true
Terminal=false
EOF

# Create icon for the monitor-app.
%{__cat} << EOF > fedora_addons/%{name}-monitor.svg
<?xml version="1.0" encoding="iso-8859-1"?>
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">
<path style="fill:#EFEFEF;" d="M501.106,256c0,33.661-6.787,65.732-19.064,94.927L256,239.66L29.957,350.927
	C17.68,321.732,10.894,289.661,10.894,256C10.894,120.636,120.636,10.894,256,10.894S501.106,120.636,501.106,256z"/>
<path style="fill:#F15A29;" d="M430.294,256c0,22.43-4.238,43.869-11.961,63.564l-96.202-47.355c1.264-5.196,1.95-10.621,1.95-16.21
	c0-18.802-7.626-35.818-19.935-48.15l75.101-75.101C410.783,164.298,430.294,207.872,430.294,256z"/>
<path style="fill:#FBA026;" d="M418.332,319.564c-25.393,64.828-88.5,110.734-162.337,110.734
	c-73.826,0-136.933-45.895-162.337-110.723C85.935,299.879,81.698,278.43,81.698,256c0-96.256,78.042-174.298,174.298-174.298
	c48.128,0,91.702,19.51,123.25,51.047l-75.101,75.101c12.31,12.332,19.935,29.347,19.935,48.15c0,5.588-0.686,11.013-1.95,16.21
	L418.332,319.564z"/>
<path style="fill:#27AAE1;" d="M482.038,350.927c-37.093,88.227-124.34,150.179-226.043,150.179S67.046,439.154,29.953,350.927
	l63.706-31.352l96.212-47.365c-1.264-5.196-1.961-10.621-1.961-16.21c0-37.605,30.491-68.085,68.085-68.085
	c18.802,0,35.818,7.626,48.15,19.935c12.31,12.332,19.935,29.347,19.935,48.15c0,5.588-0.686,11.013-1.95,16.21l96.202,47.355
	L482.038,350.927z"/>
<circle style="fill:#EFEFEF;" cx="256" cy="256" r="21.787"/>
<g>
	<path style="fill:#231F20;" d="M191.566,307.802l-77.373,38.086c-5.398,2.657-7.62,9.187-4.963,14.584
		c1.895,3.851,5.762,6.085,9.781,6.085c1.614,0,3.255-0.362,4.802-1.122l77.373-38.087c5.398-2.657,7.62-9.187,4.963-14.584
		C203.495,307.369,196.965,305.147,191.566,307.802z"/>
	<path style="fill:#231F20;" d="M245.106,457.532c0,6.017,4.878,10.894,10.894,10.894c28.936,0,57.027-5.721,83.495-17.005
		c26.031-11.098,49.226-27.021,68.936-47.325c4.192-4.316,4.088-11.213-0.228-15.405c-4.317-4.19-11.213-4.087-15.405,0.229
		c-36.133,37.22-84.715,57.719-136.799,57.719C249.985,446.638,245.106,451.515,245.106,457.532z"/>
	<path style="fill:#231F20;" d="M415.931,379.26c1.884,1.293,4.028,1.912,6.153,1.912c3.47,0,6.88-1.655,8.993-4.731l0.15-0.219
		c3.403-4.961,2.142-11.742-2.82-15.145c-4.958-3.403-11.74-2.142-15.145,2.819l-0.15,0.219
		C409.708,369.076,410.969,375.856,415.931,379.26z"/>
	<path style="fill:#231F20;" d="M288.681,256.002c0-18.02-14.661-32.681-32.681-32.681s-32.681,14.661-32.681,32.681
		S237.98,288.683,256,288.683S288.681,274.022,288.681,256.002z M245.106,256.002c0-6.007,4.887-10.894,10.894-10.894
		c6.007,0,10.894,4.887,10.894,10.894c0,6.007-4.887,10.894-10.894,10.894C249.993,266.896,245.106,262.009,245.106,256.002z"/>
	<path style="fill:#231F20;" d="M512,256c0-68.378-26.628-132.665-74.982-181.017S324.379,0,256,0
		C187.622,0,123.335,26.629,74.982,74.983C26.629,123.335,0,187.622,0,256c0,34.321,6.685,67.638,19.868,99.032
		c0.015,0.039,0.026,0.078,0.042,0.118C59.97,450.433,152.639,512,255.996,512s196.025-61.567,236.085-156.851
		c0,0,0-0.001,0.001-0.002l0.002,0.003C505.299,323.726,512,290.367,512,256z M255.996,490.213
		c-91.135,0-173.186-52.313-211.823-134.142l150.511-74.087c4.58-2.255,6.98-7.387,5.774-12.348
		c-1.097-4.507-1.653-9.095-1.653-13.636c0-31.536,25.657-57.191,57.191-57.191c15.265,0,29.632,5.949,40.44,16.738
		c10.802,10.822,16.751,25.188,16.751,40.453c0,4.57-0.552,9.157-1.642,13.636c-1.206,4.961,1.194,10.094,5.775,12.348
		l150.499,74.086C429.182,437.898,347.131,490.213,255.996,490.213z M92.591,256c0-90.101,73.303-163.404,163.404-163.404
		c39.988,0,77.792,14.274,107.592,40.406l-59.981,59.984c-13.652-10.349-30.203-15.964-47.611-15.964
		c-43.549,0-78.979,35.429-78.979,78.979c0,3.354,0.218,6.721,0.651,10.076l-77.795,38.292
		C95.042,288.781,92.591,272.563,92.591,256z M378.993,148.407C405.126,178.206,419.4,216.011,419.4,256
		c0,16.559-2.443,32.779-7.276,48.367l0.001,0.002l-77.797-38.297c0.43-3.344,0.646-6.712,0.646-10.072
		c0-17.413-5.618-33.97-15.981-47.631l0.031,0.01L378.993,148.407z M431.875,314.091c6.176-18.676,9.312-38.169,9.312-58.091
		c0-45.811-16.535-89.081-46.766-123.018l5.449-5.448c4.254-4.254,4.254-11.152,0-15.406c-4.253-4.254-11.149-4.254-15.407,0
		l-5.449,5.449c-33.938-30.232-77.207-46.768-123.018-46.768C153.881,70.809,70.804,153.885,70.804,256
		c0,19.926,3.134,39.421,9.309,58.095L35.774,335.92c-9.286-25.546-13.986-52.377-13.986-79.92
		C21.787,126.855,126.854,21.787,256,21.787S490.213,126.855,490.213,256c0,27.547-4.701,54.378-13.987,79.922l0.002,0.003
		L431.875,314.091z"/>
</g>
</svg>
EOF

# Create ReadMe.txt for the monitor-app.
%{__cat} << EOF > fedora_addons/%{name}-monitor.ReadMe.txt
Running the thermald-monitor-app
--------------------------------

To communicate with thermald via dbus, the user has to be member
of the "power" group.  So make sure to add your user id to this
group before using the thermald-monitor-app.
EOF

NO_CONFIGURE=1 ./autogen.sh


%build
%configure									\
	--disable-option-checking						\
	--disable-silent-rules

%make_build

# Build the monitor-app.
pushd tools/thermal_monitor
%{__mkdir} -p %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..
%make_build
popd
popd


%install
%make_install

# Install management-script.
%{__install} -Dpm 0755 tools/thermald_set_pref.sh				\
	%{buildroot}%{_bindir}/%{name}-set-pref

# DBus config belongs into %%{_datadir}.
%{__mkdir} -p %{buildroot}%{_datadir}
%{__mv} -f %{buildroot}%{_sysconfdir}/dbus-1/* %{buildroot}%{_datadir}/dbus-1/

# No Upstart.
%{__rm} -fr %{buildroot}%{_sysconfdir}/init

# Setup tmpfiles.d
%{__install} -Dpm 0644 fedora_addons/%{name}.conf				\
	%{buildroot}%{_tmpfilesdir}/%{name}.conf
%{__install} -dm 0755 %{buildroot}%{_rundir}/%{name}
/bin/echo "%{name}_pid" > %{buildroot}%{_rundir}/%{name}/%{name}.pid
%{__chmod} -c 0644 %{buildroot}%{_rundir}/%{name}/%{name}.pid

# Install the monitor-app.
%{__install} -Dpm 0755 tools/thermal_monitor/%{_target_platform}/ThermalMonitor	\
	%{buildroot}%{_bindir}/ThermalMonitor
%{__install} -Dpm 0644 fedora_addons/%{name}-monitor.desktop			\
	%{buildroot}%{_datadir}/applications/%{name}-monitor.desktop
%{__install} -Dpm 0644 fedora_addons/%{name}-monitor.svg			\
	%{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}-monitor.svg


%check
%{_bindir}/desktop-file-validate						\
	%{buildroot}%{_datadir}/applications/*.desktop


%pre
/bin/getent group power >/dev/null || /sbin/groupadd -r power
exit 0


%post
%systemd_post thermald.service


%preun
%systemd_preun thermald.service


%postun
%systemd_postun_with_restart thermald.service

%files
%config(noreplace) %{_sysconfdir}/%{name}
%doc README.txt thermal_daemon_usage.txt
%ghost %dir %{_rundir}/%{name}
%ghost %{_rundir}/%{name}/%{name}.pid
%license COPYING
%{_bindir}/%{name}-set-pref
%{_datadir}/dbus-1/system-services/org.freedesktop.%{name}.service
%{_datadir}/dbus-1/system.d/org.freedesktop.%{name}.conf
%{_mandir}/man5/thermal-conf.xml.5*
%{_mandir}/man8/%{name}.8*
%{_sbindir}/%{name}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service


%files monitor
%doc fedora_addons/%{name}-monitor.ReadMe.txt
%license tools/thermal_monitor/qcustomplot/GPL.txt
%{_bindir}/ThermalMonitor
%{_datadir}/applications/%{name}-monitor.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}-monitor.svg


%changelog
* Mon Dec 19 2022 Bastien Nocera <bnocera@redhat.com> - 2.5.1-1
- Update to 2.5.1
Resolves: rhbz#2114048

* Mon Jul 25 2022 Benjamin Berg <bberg@redhat.com> - 2.5-3
- Accept 2.5 as package version
  Related: #2040080

* Mon Jul 25 2022 Benjamin Berg <bberg@redhat.com> - 2.5-2
- Fix version test script
  Related: #2040080

* Fri Jul 22 2022 Benjamin Berg <bberg@redhat.com> - 2.5-1
- Update to 2.5
  Resolves: #2040080

* Fri Nov 12 2021 Benjamin Berg <bberg@redhat.com> - 2.4.6-1
- Update to 2.4.6 and newer CPU model support
  Resolves: #1999368

* Thu Dec 10 2020 Benjamin Berg <bberg@redhat.com> - 2.4.1-2
- Fix problems reported by coverity
  Related: #1875505

* Tue Dec 08 2020 Benjamin Berg <bberg@redhat.com> - 2.4.1-1
- Update to thermald 2.4.1
  Resolves: #1875505

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 18 2019 Benjamin Berg <bberg@redhat.com> - 1.9.1-1
- New upstream release 1.9 (rhbz#1782249)
- Drop Patch0, it has been merged upstream

* Fri Sep 20 2019 Christian Kellner <ckellner@redhat.com> - 1.9-1
- New upstream release 1.9 (rhbz#1742290)
- Update patch0 (taken from upstream, commit dcdaf52...)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 17 2019 Benjamin Berg <bberg@redhat.com> - 1.8-2
- Fix build on i686

* Fri May 17 2019 Benjamin Berg <bberg@redhat.com> - 1.8-1
- New upstream release (#1582506)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 28 2017 Björn Esser <besser82@fedoraproject.org> - 1.7.1-1
- New upstream release (#1505144)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 01 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-6
- Add upstreamed patch to silence compiler warnings

* Sat Jul 01 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-5
- Replace fix for rhbz#1464548 from upstream commit
- Add upstream patch to fix README

* Fri Jun 30 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-4
- Add upstream patch to fix ThermalMonitor (rhbz#1464548)
- Add several fixes from upstream

* Tue Apr 11 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-3
- Explicitly turn on hardening, if required

* Tue Apr 11 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-2
- Fix missing trailing semicolon in desktop-file

* Tue Apr 11 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-1
- Initial import (rhbz#1440406)

* Mon Apr 10 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-0.4
- Use qmake_qt5-macro and build out of tree

* Sat Apr 08 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-0.3
- Small packaging improvements

* Sat Apr 08 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-0.2
- Add management-script

* Sat Apr 08 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-0.1
- Initial rpm-release (rhbz#1440406)
