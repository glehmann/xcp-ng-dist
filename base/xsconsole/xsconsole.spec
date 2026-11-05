%global package_speccommit a8bca11d6d3292935ec3ce8c3465e66b3d202962
%{!?xsrel: %global xsrel 1}
%global package_srccommit v11.1.4

Summary: XCP-ng Host Configuration Console
Name: xsconsole
Version: 11.1.4
Release: %{?xsrel}.1%{?dist}
License: GPL2
Group: Administration/System
Source0: xsconsole-11.1.4.tar.gz
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

# Metadata backup/restore functionality does not work with Xapi versions without
# the scripts present
Conflicts: xapi-core < 24.20.0

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

# upstream master commits
Patch1000: 0001-CA-417645-Refine-Remote-Shell-status-in-xsconsole.patch
Patch1001: 0002-pyproject-use-a-more-correct-requires-python.patch
Patch1002: 0003-pyproject-drop-superseded-license-classifiers.patch
Patch1003: 0004-Convert-all-OpaqueRef-fields-in-host-pool-SR-and-VM-.patch
# https://github.com/xapi-project/xsconsole/pull/73
Patch1004: 0005-XSConsoleImported-switch-from-imp-to-importlib-for-p.patch
# XCP-ng patches
Patch1005: 0006-Replace-XenServer-with-XCP-ng-in-xsconsole.service.patch
Patch1006: 0007-New-theme-colors.patch
# PR pending merge
Patch1007: 0008-Handle-IPv6.patch
Patch1008: 0009-Support-Pool-join-in-IPv6.patch
Patch1009: 0010-XSFeatureNetworkReset-allow-the-user-to-perform-an-e.patch
Patch1010: 0011-XSFeatureInterface-Reset-old-management-interface-co.patch
# https://github.com/xapi-project/xsconsole/pull/90
Patch1011: 0012-Retry-the-xapi-connection-instead-of-latching-it-bro.patch

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
* Thu Nov 05 2026 Yann Dirson <yann.dirson@vates.tech> - 11.1.4-1.1
- Sync with XS9's 11.1.4-1
- Refreshed all patches from git-format-patch, new filenames
- Include post-11.1.4 commits from master and python 3.12 support from #73
- *** Upstream changelog *** (XS9 forked off 11.0.8-1)
  * Fri Dec 19 2025 Changlei Li <changlei.li@cloud.com> - 11.1.4-1
  - CP-308543 Use xenapi to manage timezone and NTP

  * Thu Dec 11 2025 Changlei Li <changlei.li@cloud.com> - 11.1.3-1
  - CA-420524: Do not allow input a non-exist device in network reset
  - CA-421635: Show the real NTP servers in dhcp NTP mode

  * Tue Nov 04 2025 Changlei Li <changlel.li@cloud.com> - 11.1.2-1
  - CP-54442: Update for network devices not being renamed
  - CA-415864: MANAGEMENT_INTERFACE is not cleared in network reset

  * Fri Sep 26 2025 Lin Liu <Lin.Liu01@cloud.com> - 11.1.1-1
  - CA-417641: Update ntp-dhcp server file for updated chrony

  * Thu Jul 31 2025 Lunfan Zhang <Lunfan.Zhang@cloud.com> - 11.1.0-1
  - CP-309227: Enable xsconsole to support control SSH and ssh-auto-mode

  * Wed Jul 16 2025 Chunjie Zhu <chunjie.zhu@cloud.com> - 11.0.11-1
  - CA-413432: convert variant select operation async mode
  - CA-413431: filter OpaqueRef:NULL case

  * Mon Jun 30 2025 Chunjie Zhu <chunjie.zhu@cloud.com> - 11.0.10-1
  - CP-52200: add DMV function
  - NetworkReset: Sync up the network-reset file path with xapi
  - NetworkReset: don't truncate the IPv6 address of the coordinator host
  - CP-48511: Show timezone alongside time in top line
  - Remove unused file
  - CP-50411: Show all SSH host key fingerprints in xsconsole

  * Wed May 28 2025 Chunjie Zhu <chunjie.zhu@cloud.com> - 11.0.9-2
  - CA-411707: deploy dmv-utils in dom0 by default

  * Thu Aug 1 2024 Lin Liu <Lin.Liu01@cloud.com> - 11.0.9-1
  - CA-395025: Local command shell login failed on XS9

* Wed Aug 05 2026 Andrii Sultanov <andriy.sultanov@vates.tech> - 11.0.9.1-1.3
- Retry the xapi connection instead of latching it broken forever

* Mon Jun 22 2026 Stefanos Gerangelos <stefanos.gerangelos@vates.tech> - 11.0.9.1-1.2
- Backport the user option to allow the network reset without renaming the management interface (upstream PR #85)
- Backport the reset of old management interface configuration when switching to a new one (upstream PR #86)

* Tue Sep 02 2025 Guillaume Thouvenin <guillaume.thouvenin@vates.tech> - 11.0.9.1-1.1
- Sync with 11.0.9.1-1
- Drop xsconsole-11.0.8-sync-network-reset-trigger-file.patch
- Drop xsconsole-11.0.8-do-not-truncate-ipv6-in-pool-config-on-reset.patch
- *** Upstream changelog ***
  * Thu Jul 31 2025 Lunfan Zhang <Lunfan.Zhang@cloud.com> - 11.0.9.1-1
  - CP-309227: Enable xsconsole to support control SSH and ssh-auto-mode
  * Thu Aug 1 2024 Lin Liu <Lin.Liu01@cloud.com> - 11.0.9-1
  - CA-395025: Local command shell login failed on XS9

* Wed Aug 20 2025 David Morel <david.morel@vates.tech> - 11.0.8-1.2
- Backport fix to sync network reset trigger file with current XAPI
- Backport fix for IPv6 truncated in pool.conf on network reset

* Wed Mar 05 2025 Samuel Verschelde <stormi-xcp@ylix.fr> - 11.0.8-1.1
- Sync with 11.0.8-1
- *** Upstream changelog ***
  * Tue Jul 23 2024 Gerald Elder-Vass <gerald.elder-vass@cloud.com> - 11.0.8-1
  - CA-390512: Improved xenapi error handling
  * Tue Jul 23 2024 Alex Brett <alex.brett@cloud.com> - 11.0.7-1
  - CP-49228: Reintroduce Portable SR feature

* Wed Sep 18 2024 Benjamin Reis <benjamin.reis@vates.tech> - 11.0.6-1.2
- Add xsconsole-11.0.6-Ipv6-pool-join.XCP-ng.patch

* Mon Aug 12 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 11.0.6-1.1
- Sync with 11.0.6-1
- *** Upstream changelog ***
  * Fri Jun 07 2024 Stephen Cheng <stephen.cheng@cloud.com> - 11.0.6-1
  - CA-388527: Fix 'timed out' when creating an ISCSI SR
  * Thu May 16 2024 Lin Liu <Lin.Liu01@cloud.com> - 11.0.3-1
  - CA-357771: Remove obsolete strings: StorageLink(CVSM/cslg) leftovers

* Wed Jun 19 2024 Benjamin Reis <benjamin.reis@vates.tech> - 11.0.2-1.1
- Update to 11.0.2-1
- Redo xsconsole-11.0.2-support-ipv6.XCP-ng.patch (now contains xsconsole-10.1.14-ipv6-autoconf.XCP-ng.patch)
- Drop xsconsole-10.1.14-display-vlan.XCP-ng.patch
- *** Upstream changelog ***
  * Tue Mar 19 2024 Gerald Elder-Vass <gerald.elder-vass@cloud.com> - 11.0.2-1
  - CA-369899: Add NTP config control for DHCP|Default|Manual|None options
  - CA-389475: Update the timezone when it changes
  * Thu Feb 29 2024 Mark Syms <mark.syms@citrix.com> - 11.0.1-1
  - CA-389275: return insrtype if no translation
  * Thu Feb 29 2024 Fei Su<fei.su@cloud.com> - 11.0.0-2
  - CP-48192 Requires glibc-langpack-en to fix the locale.Error on xs9
  * Mon Feb 05 2024 Stephen Cheng <stephen.cheng@cloud.com> - 11.0.0-1
  - CP-44690: Upgrade to python 3

* Fri Feb 16 2024 Benjamin Reis <benjamin.reis@vates.tech> - 10.1.14-2.2
- Add xsconsole-10.1.14-ipv6-autoconf.XCP-ng.patch

* Mon Sep 18 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 10.1.14-2.1
- Update to 10.1.14-2
- *** Upstream changelog ***
  * Fri Jul 14 2023 Alex Brett <alex.brett@cloud.com> - 10.1.14-2
  - CP-43942: Remove Portable SR feature

* Mon Jul 17 2023 Benjamin Reis <benjamin.reis@vates.fr> - 10.1.14-1.3
- Add xsconsole-10.1.14-display-vlan.XCP-ng.patch

* Wed May 10 2023 Benjamin Reis <benjamin.reis@vates.fr> - 10.1.14-1.2
- Add xsconsole-10.1.14-support-ipv6.XCP-ng.patch

* Wed Dec 07 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 10.1.14-1.1
- Update from XS 8.3 pre-release updates
- *** Upstream changelog ***
  * Tue Oct 04 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 10.1.14-1
  - CP-40640: Show the textual rather than numeric product version

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
