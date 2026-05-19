# Explicitly turn on hardening, if required.
%if 0%{?rhel} && 0%{?rhel} <= 7
%global _hardened_build 1
%endif

%global pkgname thermal_daemon


Name:		thermald
Version:	2.5.9
Release:	1%{?dist}
Summary:	Thermal Management daemon

# thd_cdev_modem.{cpp,h} is currently GPLv2 only
# https://github.com/intel/thermal_daemon/issues/306
License:	GPLv2
URL:		https://github.com/intel/%{pkgname}
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# No cpuid.h on other arches.
ExclusiveArch:	%{ix86} x86_64

BuildRequires: make
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


%description
%{name} monitors and controls platform temperature.

Thermal issues are important to handle proactively to reduce performance
impact.  %{name} uses the existing Linux kernel infrastructure and can
be easily enhanced.


%prep
%autosetup -n %{pkgname}-%{version} -p 1

# Create tmpfiles.d config.
%{__mkdir} -p fedora_addons
%{__cat} << EOF > fedora_addons/%{name}.conf
d %{_rundir}/%{name} 0755 root root -
EOF

NO_CONFIGURE=1 ./autogen.sh


%build
%configure									\
	--disable-option-checking						\
	--disable-silent-rules

%make_build


%install
%make_install

# Install management-script.
%{__install} -Dpm 0755 tools/thermald_set_pref.sh				\
	%{buildroot}%{_bindir}/%{name}-set-pref

# No Upstart.
%{__rm} -fr %{buildroot}%{_sysconfdir}/init

# Setup tmpfiles.d
%{__install} -Dpm 0644 fedora_addons/%{name}.conf				\
	%{buildroot}%{_tmpfilesdir}/%{name}.conf
%{__install} -dm 0755 %{buildroot}%{_rundir}/%{name}
/bin/echo "%{name}_pid" > %{buildroot}%{_rundir}/%{name}/%{name}.pid
%{__chmod} -c 0644 %{buildroot}%{_rundir}/%{name}/%{name}.pid


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


%changelog
* Tue Sep 09 2025 Kate Hsuan <hpa@redhat.com> - 2.5.9-1
- Update to 2.5.9
- Drop thermeld-monitor since the qcustomplot patch was out of date
  Resolves: RHEL-97639

* Tue Aug 22 2023 Kate Hsuan <hpa@redhat.com> - 2.5.3-1
- Update to 2.5.3
  Resolves: rhbz#2221062

* Thu Feb 23 2023 Bastien Nocera <bnocera@redhat.com> - 2.5.2-1
- Update to 2.5.2
Resolves: rhbz#2172590

* Mon Dec 19 2022 Bastien Nocera <bnocera@redhat.com> - 2.5.1-1
- Update to 2.5.1
Resolves: rhbz#2114049

* Mon Jul 25 2022 Benjamin Berg <bberg@redhat.com> - 2.5-3
- Accept 2.5 as package version
  Related: #2040081

* Mon Jul 25 2022 Benjamin Berg <bberg@redhat.com> - 2.5-2
- Fix version test script
  Related: #2040081

* Fri Jul 22 2022 Benjamin Berg <bberg@redhat.com> - 2.5-1
- Update to 2.5
  Resolves: #2040081

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 2.4.6-2
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Jun 10 2021 Benjamin Berg <bberg@redhat.com> - 2.4.6-1
- Update to 2.4.6 (#1965783)
- Update main license to GPLv2 only for now
- Add bundled(qcustomplot) for monitor subpackage
- Resolves: #1961047

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 2.4.1-4
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Feb 02 2021 Benjamin Berg <bberg@redhat.com> - 2.4.1-3
- Add upstream patch fixing parsing of passive targets

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 01 2020 Benjamin Berg <bberg@redhat.com> - 2.4.1-1
- New upstream release (#1903094)

* Thu Nov 26 2020 Benjamin Berg <bberg@redhat.com> - 2.4-1
- New upstream release (#1901810)
  Resolves: #1894178
  Resolves: #1892534

* Tue Sep 01 2020 Benjamin Berg <bberg@redhat.com> - 2.3-2
- Fix Lenovo kill switch (#1874462)

* Tue Aug 25 2020 Benjamin Berg <bberg@redhat.com> - 2.3-1
- New upstream release 2.3 (rhbz#1866784)
- Add patch to fix printf on non-64 bit

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 08 2020 Benjamin Berg <bberg@redhat.com> - 2.2-1
- New upstream release 2.2 (rhbz#1827883)

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
