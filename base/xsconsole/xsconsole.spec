%global package_speccommit 022075fd2250025dcf7bd675722a3c8f8acd34af
%global usver 11.0.2
%global xsver 1
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit v11.0.2

Summary: XCP-ng Host Configuration Console
Name: xsconsole
Version: 11.0.2
Release: %{?xsrel}.1%{?dist}
License: GPL2
Group: Administration/System
Source0: xsconsole-11.0.2.tar.gz
Patch0: CP-43942.patch
Provides: xsconsole0
BuildRequires: python3-devel
BuildRequires: systemd
Requires: ipmitool
Requires: python3-pam
Requires: pciutils
Requires: dmidecode
Requires: ncurses >= 6.4-2
%if 0%{?xenserver} > 8
Requires: glibc-langpack-en
%endif

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

# XCP-ng patches
Patch1000: xsconsole-10.1.9-rebrand-xsconsole-service.XCP-ng.patch
Patch1001: xsconsole-10.1.13-define-xcp-ng-colors.XCP-ng.patch
# PR pending merge
Patch1002: xsconsole-11.0.2-support-ipv6.XCP-ng.patch

%description
Console tool for configuring a XCP-ng installation.

%prep
%autosetup -p1

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__make} install-base DESTDIR=%{buildroot}
%{__make} install-oem DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post
%systemd_post xsconsole.service

%preun
%systemd_preun xsconsole.service

%postun
%systemd_postun xsconsole.service

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/xsconsole/*.py*
%{_libdir}/xsconsole/plugins-base
%{_bindir}/xsconsole
%dir %{_libdir}/xsconsole/plugins-oem
%exclude %{_libdir}/xsconsole/plugins-oem/*
%{_unitdir}/xsconsole.service

%changelog
* Wed Jun 19 2024 Benjamin Reis <benjamin.reis@vates.tech> - 11.0.2-1.1
- Update to 11.0.2-1
- Redo xsconsole-11.0.2-support-ipv6.XCP-ng.patch (now contains xsconsole-10.1.14-ipv6-autoconf.XCP-ng.patch)
- Drop xsconsole-10.1.14-display-vlan.XCP-ng.patch
- *** Upstream changelog ***
- * Tue Mar 19 2024 Gerald Elder-Vass <gerald.elder-vass@cloud.com> - 11.0.2-1
- - CA-369899: Add NTP config control for DHCP|Default|Manual|None options
- - CA-389475: Update the timezone when it changes
- * Thu Feb 29 2024 Mark Syms <mark.syms@citrix.com> - 11.0.1-1
- - CA-389275: return insrtype if no translation
- * Thu Feb 29 2024 Fei Su<fei.su@cloud.com> - 11.0.0-2
- - CP-48192 Requires glibc-langpack-en to fix the locale.Error on xs9
- * Mon Feb 05 2024 Stephen Cheng <stephen.cheng@cloud.com> - 11.0.0-1
- - CP-44690: Upgrade to python 3

* Fri Feb 16 2024 Benjamin Reis <benjamin.reis@vates.tech> - 10.1.14-2.2
- Add xsconsole-10.1.14-ipv6-autoconf.XCP-ng.patch

* Mon Sep 18 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 10.1.14-2.1
- Update to 10.1.14-2
- *** Upstream changelog ***
- * Fri Jul 14 2023 Alex Brett <alex.brett@cloud.com> - 10.1.14-2
- - CP-43942: Remove Portable SR feature

* Mon Jul 17 2023 Benjamin Reis <benjamin.reis@vates.fr> - 10.1.14-1.3
- Add xsconsole-10.1.14-display-vlan.XCP-ng.patch

* Wed May 10 2023 Benjamin Reis <benjamin.reis@vates.fr> - 10.1.14-1.2
- Add xsconsole-10.1.14-support-ipv6.XCP-ng.patch

* Wed Dec 07 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 10.1.14-1.1
- Update from XS 8.3 pre-release updates
- *** Upstream changelog ***
- * Tue Oct 04 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 10.1.14-1
- - CP-40640: Show the textual rather than numeric product version

* Mon Nov 14 2022 Yann Dirson <yann.dirson@vates.fr> - 10.1.13-1.2
- Update colors to match new branding
- Bump patchname to xsconsole-10.1.13-define-xcp-ng-colors.XCP-ng.patch

* Tue Aug 30 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 10.1.13-1.1
- Rebase on CH 8.3 Preview
- Re-remove incloudsphere subpackage
- Keep xsconsole-10.1.9-rebrand-xsconsole-service.XCP-ng.patch
- Keep xsconsole-10.1.9-define-xcp-ng-colors.XCP-ng.patch

* Fri Jul 09 2021 Ross Lagerwall <ross.lagerwall@citrix.com> - 10.1.13-1
- Switch upstream to GitHub
- Display 'Ext' instead of 'Ext3' for `ext` SRs
- CA-355872: Use XAPI to edit DNS entries within xsconsole
- Display clearer error message when XAPI unreachable
- rework is_master to raise in case of failure

* Fri Feb 19 2021 Ross Lagerwall <ross.lagerwall@citrix.com> - 10.1.12-1
- Add version to tarball filename
- CA-348699: Fix full version display if the build number is empty

* Wed Jan 08 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 10.1.11-1
- CA-310799: Fix performance information

* Thu Oct 31 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 10.1.10-1
- CP-30221: Switch to chrony from ntp

* Mon Sep 16 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 10.1.9-2
- CA-324927: Don't restart xsconsole during upgrade

* Wed Jan 16 2019 Aaron Robson <aaron.robson@citrix.com> - 10.1.9-1
- CA-304344: Makefile warning due to missing file XSFeatureInstallLicence.py
- CA-304345: Integrate xsconsole with Travis CI
- 'make clean' and 'make test' implemented
- include suitable .gitgnore

* Thu Aug 30 2018 Simon Rowe <simon.rowe@citrix.com> - 10.1.8-1
- CA-293996: XSConsole status bar showed wrong product brand and version after upgrading.

* Mon Apr 23 2018 Simon Rowe <simon.rowe@citrix.com> - 10.1.7-1
- CA-288312: use /etc/hostname

* Thu Feb 01 2018 Simon Rowe <simon.rowe@citrix.com> - 10.1.6-1
- SCTX-2620 Handle xapi login error
- SCTX-2620 Guard against a null _session log out

* Mon Nov 20 2017 Ross Lagerwall <ross.lagerwall@citrix.com> - 10.1.5-1
- CA-272803: Write `xentemp` bridge if VLAN is specified

* Tue Nov 14 2017 Simon Rowe <simon.rowe@citrix.com> - 10.1.4-1
- CA-273753: Correct typo in getting PRODUCT_BRAND from inventory

* Tue Nov 07 2017 Simon Rowe <simon.rowe@citrix.com> - 10.1.3-1
- CA-186510: Fetch version data directly from /etc/xensource-inventory

* Mon Oct 16 2017 Simon Rowe <simon.rowe@citrix.com> - 10.1.2-1
- CA-267484: Fix regexp for finding host CPU metrics

* Wed Sep 20 2017 Simon Rowe <simon.rowe@citrix.com> - 10.1.1-1
- CA-263057 if IP address is statically configured allow DNS to be configured

* Mon Jun 05 2017 Simon Rowe <simon.rowe@citrix.com> - 10.1.0-1
- CP-14030: Update xsconsole to allow Emergency Network Reset on a VLAN.
- CP-22247: Add temporary vlan bridge to inventory for management vlan.
- fix CA-255166: also displaying vlan value if it is higher than -1
- CA-255173: fix typo creating extra quote in management.conf
- CA-255099: Use strip() instead of slicing

* Wed Apr 26 2017 Simon Rowe <simon.rowe@citrix.com> - 10.0.3-1
- Remove stale files
- CP-21612: Add XSFeatureLicenseNag.py

* Thu Apr 20 2017 Simon Rowe <simon.rowe@citrix.com> - 10.0.2-1
- Remove the build number from the console

* Mon Mar 27 2017 Simon Rowe <simon.rowe@citrix.com> - 10.0.1-1
- CA-248121: Handle failed open()s correctly
- CA-248121: Don't look in /etc/xcp for config files
