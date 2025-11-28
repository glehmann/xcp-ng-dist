Name:           xcp-ng-config
Version:        0
Release:        0.ydi.1%{?dist}

Summary:        %{dist_name} configuration files
Group:          System Environment/Base
License:        GPL-2.0-or-later
URL:            https://xcp-ng.org

%description
%{dist_name} configuration files

%install
# enable persistent systemd journal
install -d -m755 %{buildroot}/var/log/journal

%files
/var/log/journal

%changelog
* Fri Nov 28 2025 Yann Dirson <yann.dirson@vates.tech> - 0-0.ydi.1
- Initial release
