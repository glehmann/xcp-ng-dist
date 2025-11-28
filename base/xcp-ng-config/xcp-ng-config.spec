Name:           xcp-ng-config
Version:        0
Release:        1%{?dist}

Summary:        XCP-ng configuration files
Group:          System Environment/Base
License:        GPL-2.0-or-later
URL:            https://github.com/xcp-ng-rpms/xcp-ng-config

%description
XCP-ng configuration files

%install
# enable persistent systemd journal
install -d -m755 %{buildroot}/var/log/journal

%files
/var/log/journal/

%changelog
* Mon Nov 09 2026 Yann Dirson <yann.dirson@vates.tech> - 0-1
- Initial release
- Enable persistent systemd journal
