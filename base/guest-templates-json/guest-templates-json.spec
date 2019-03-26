Name:    guest-templates-json
Summary: Creates the default guest templates
Version: 1.7.11
Release: 1%{dist}
License: BSD
Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/%{name}/archive?at=v%{version}&format=tar.gz&prefix=%{name}-%{version}#/%{name}-%{version}.tar.gz
BuildArch: noarch

Requires: xapi-core
BuildRequires: python2-devel
BuildRequires: python-setuptools

%description
Creates the default guest templates during first boot or package
install/upgrade.

%package data-linux
Summary: Contains the default Linux guest templates
Requires(post): %{name} = %{version}-%{release}

%description data-linux
Contains the default Linux guest templates.

%package data-windows
Summary: Contains the default Windows guest templates
Requires(post): %{name} = %{version}-%{release}

%description data-windows
Contains the default Windows guest templates.

%package data-xenapp
Summary: Contains the default XenApp guest templates
Requires: %{name}-data-windows = %{version}-%{release}
Requires(post): %{name} = %{version}-%{release}

%description data-xenapp
Contains the default XenApp guest templates.

%package data-other
Summary: Contains the default other guest templates
Requires(post): %{name} = %{version}-%{release}

%description data-other
Contains the default other guest templates.

%define templatedir %{_datadir}/xapi/vm-templates

%prep
%autosetup -p1

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --root %{buildroot}

install -d %{buildroot}%{templatedir}
install -m 644 json/*.json %{buildroot}%{templatedir}
install -d %{buildroot}%{_sysconfdir}/xapi.d/vm-templates

install -d %{buildroot}%{_sysconfdir}/firstboot.d
install -m 755 62-create-guest-templates %{buildroot}%{_sysconfdir}/firstboot.d

%post
/usr/bin/create-guest-templates > /dev/null ||:

%post data-linux
/usr/bin/create-guest-templates > /dev/null ||:

%post data-windows
/usr/bin/create-guest-templates > /dev/null ||:

%post data-xenapp
/usr/bin/create-guest-templates > /dev/null ||:

%post data-other
/usr/bin/create-guest-templates > /dev/null ||:

%files
%{_bindir}/*
%{python2_sitelib}/*
%dir %{templatedir}
%{_sysconfdir}/xapi.d/*
%{_sysconfdir}/firstboot.d/*

%files data-linux
%{templatedir}/asianux*.json
%{templatedir}/base-debian*.json
%{templatedir}/base-el*.json
%{templatedir}/base-hvmlinux.json
%{templatedir}/base-kylin*.json
%{templatedir}/base-pvlinux.json
%{templatedir}/base-sl*.json
%{templatedir}/base-ubuntu*.json
%{templatedir}/centos*.json
%{templatedir}/coreos.json
%{templatedir}/debian*.json
%{templatedir}/kylin*.json
%{templatedir}/linx*.json
%{templatedir}/oel*.json
%{templatedir}/rhel*.json
%{templatedir}/sl*.json
%{templatedir}/turbo*.json
%{templatedir}/ubuntu*.json
%{templatedir}/yinhe*.json

%files data-windows
%{templatedir}/base-windows*.json
%{templatedir}/legacy-windows.json
%{templatedir}/windows*.json

%files data-xenapp
%{templatedir}/base-xenapp*.json
%{templatedir}/xenapp*.json

%files data-other
%{templatedir}/other-install-media.json

%changelog
* Thu Jun 28 2018 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.7.11-1
- CA-292656: Fix device-model typo

* Mon Jun 25 2018 Simon Rowe <simon.rowe@citrix.com> - 1.7.10-1
- CP-28459: Add new Ubuntu 18.04 template for Lima

* Wed May 30 2018 Simon Rowe <simon.rowe@citrix.com> - 1.7.9-1
- CA-290004: Change SLE.12 PV templates to use 'hvc' as their console

* Wed Mar 28 2018 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.7.8-1
- CP-17721: Use qemu-upstream-compat for new VMs
- Increment user_version for QEMU upstream changes

* Tue Mar 27 2018 Samson Danziger <samson.danziger@citrix.com> - 1.7.7-1
- Increase user version on sle 12.3 templates
- Remove unnecessary config, and generate new uuid
- Add HVM templates for SLE.123 HVM

* Mon Mar 26 2018 Simon Rowe <simon.rowe@citrix.com> - 1.7.6-1
- CP-23798: Add template support for Network SR-IOV

* Mon Mar 26 2018 Simon Rowe <simon.rowe@citrix.com> - 1.7.5-1
- Bump user version
- CP-27447: Rename Windows 8 templates to Windows 8.1
- CA-286130: Set Debian 9 min memory to 256 MiB

* Mon Mar 26 2018 Simon Rowe <simon.rowe@citrix.com> - 1.7.4-1
- Add the user_version to the oel6 x64 template
- Add crashkernel=no as an extra PV arg for oel6 x64 guests
- CA-275747 Remove old, untested/supported guests
- CP-27055: Remove templates for removed guests

* Mon Oct 23 2017 Simon Rowe <simon.rowe@citrix.com> - 1.7.3-1
- CP-24360: Initialise VM.platform['device-model'] values - Stage 1

* Tue Oct 10 2017 Simon Rowe <simon.rowe@citrix.com> - 1.7.2-1
- CA-268286: Make all EL7 guests have at least 2G RAM

* Wed Sep 27 2017 Simon Rowe <simon.rowe@citrix.com> - 1.7.1-1
- CA-267449: fix typo in SLES template

* Wed Sep 20 2017 Simon Rowe <simon.rowe@citrix.com> - 1.7.0-1
- Add Debian Stretch 9 guest template
- Update CoreOS (Container Linux) disk and RAM requirements for v1465.7.0
- Add SLES 12.2 template assuming PV
- Add SLED 12.2 template
- Add SLES and SLED 12 SP3 for PV

* Fri Aug 18 2017 Deli Zhang <deli.zhang@citrix.com> - 1.6.0-1
- CP-22495: Add Linux guest template for NeoKylin Linux Security OS 5.0 (Update8) x64

* Thu Jun 08 2017 Wei Xie <wei.xie@citrix.com> - v1.5.0-1
- CA-256319: Rocky6 configured with 8 vCPUs installation failure via XenCenter
- CP-22352: Add support for Yinhe Kylin 4.
- CA-255653: Change Linx 6 to HVM mode.
- CP-22351: Add support for Linx Linux 6 and 8.

* Fri Jun 02 2017 Wei Xie <wei.xie@citrix.com> - v1.4.0-1
- CP-22097: Add Linux guest template for Turbo Linux.
- CP-21799: And new VM templates for Asianux 4 Linux.

* Thu May 04 2017 Simon Rowe <simon.rowe@citrix.com> - 1.2.1-1
- CP-251550: Update legacy windows template

* Wed Apr 26 2017 Simon Rowe <simon.rowe@citrix.com> - 1.2.0-1
- Update base Windows template to use 2 vCPUs
- CP-21446: Remove old templates from XenServer.
- CP-21988 Remove Vista template
- CP-21988 Add legacy windows template

