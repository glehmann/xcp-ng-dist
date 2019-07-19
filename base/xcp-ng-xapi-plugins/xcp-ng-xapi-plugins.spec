Summary: XAPI additional plugins for XCP-ng
Name: xcp-ng-xapi-plugins
Version: 1.5.0
Release: 1%{?dist}
URL: https://github.com/xcp-ng/xcp-ng-xapi-plugins
Source0: https://github.com/xcp-ng/xcp-ng-xapi-plugins/archive/v%{version}/%{name}-%{version}.tar.gz
License: AGPLv3

BuildArch: noarch

Obsoletes: xcp-ng-updater

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
%doc LICENSE README.md test_updater.sh
/etc/xapi.d/plugins/*
%dir /var/lib/xcp-ng-xapi-plugins

%changelog
* Fri Jul 19 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.5.0-1
- Prevent concurrent runs of the updater plugin

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

