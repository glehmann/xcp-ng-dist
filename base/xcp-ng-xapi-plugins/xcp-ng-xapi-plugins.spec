Summary: XAPI additional plugins for XCP-ng
Name: xcp-ng-xapi-plugins
Version: 1.8.0
Release: 1%{?dist}
URL: https://github.com/xcp-ng/xcp-ng-xapi-plugins
Source0: https://github.com/xcp-ng/xcp-ng-xapi-plugins/archive/v%{version}/%{name}-%{version}.tar.gz
License: AGPLv3

BuildArch: noarch

Obsoletes: xcp-ng-updater <= 1.3.0

%description
Collection of XAPI plugins specific to XCP-ng.
- Updater plugin to interact with the underlying
- A plugin for ZFS discovery
- ...

%prep
%autosetup -p1

%install
install -d %{buildroot}/etc/xapi.d/plugins/
install -d %{buildroot}/etc/xapi.d/plugins/xcpngutils/
install -d %{buildroot}/var/lib/xcp-ng-xapi-plugins/
install SOURCES/etc/xapi.d/plugins/*.py %{buildroot}/etc/xapi.d/plugins/
install SOURCES/etc/xapi.d/plugins/xcpngutils/*.py %{buildroot}/etc/xapi.d/plugins/xcpngutils/

%files
%doc LICENSE README.md
/etc/xapi.d/plugins/*
%dir /var/lib/xcp-ng-xapi-plugins

%changelog

* Mon Jun 12 2023 Ronan Abhamon <ronan.abhamon@vates.fr> - 1.8.0-1
- Add a way to install packages with updater.py
- xcp-ng-linstor is now a default repo of updater.py

* Fri Feb 03 2023 Benjamin Reis <benjamin.reis@vates.fr> - 1.7.3-1
- Add LVM plugin to list and create PVs, VGs and LVs
- RAID plugin: handle gracefully when no RAID is present

* Fri Sep 16 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.7.2-2
- Rebuild for XCP-ng 8.3

* Fri May 20 2022 Benjamin Reis <benjamin.reis@vates.fr> - 1.7.2-1
- Really disable unwanted repos when running yum update
- Fix exception handling when a command fails

* Thu Feb 10 2022 Ronan Abhamon <ronan.abhamon@vates.fr> - 1.7.1-1
- Fix invalid `run_command` implementation
- Fix installation of netdata package

* Fri Dec 17 2021 Benjamin Reis <benjamin.reis@vates.fr> - 1.7.0-1
- Fix lock in updater plugin (See: https://github.com/xcp-ng/xcp/issues/523)
- Normalize plugins output
- Add plugin to display return of lsblk

* Wed Jul 01 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.6.1-3
- Rebuild for XCP-ng 8.2.0

* Fri Dec 20 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.6.1-2
- Rebuild for XCP-ng 8.1.0

* Fri Nov 29 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.6.1-1
- Add plugin to handle netdata installation and configuration

* Fri Jul 19 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.5.0-1
- Prevent concurrent runs of the updater plugin
- Use versioned obsoletes
- Remove test_updater.sh

* Tue Jun 11 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.4.0-1
- Add hyperthreading detection plugin

* Mon Jun 03 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.3.0-2
- Renamed to xcp-ng-xapi-plugins
- Obsoletes xcp-ng-updater

* Fri May 31 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.3.0-1
- New version 1.3.0 with added zfs discovery plugin

* Thu May 02 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.2.0-1
- New version 1.2.0 with proxy configuration support

* Thu Sep 13 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.1.0-3
- Rebuild for XCP-ng 7.6.0

* Fri Jul 27 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.1.0-2
- Version of last published package was actually 1.1, updating

* Fri Jun 29 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.0-1
- Initial package.
