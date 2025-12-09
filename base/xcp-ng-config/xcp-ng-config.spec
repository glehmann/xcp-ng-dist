Name:           xcp-ng-config
Version:        0
Release:        0.ydi.2%{?dist}

Summary:        XCP-ng configuration files
Group:          System Environment/Base
License:        GPL-2.0-or-later
URL:            https://xcp-ng.org

%description
XCP-ng configuration files

%install
# enable persistent systemd journal
install -d -m755 %{buildroot}/var/log/journal

# pin Almalinux version to avoid upgrade to 10.1+
mkdir -p %{buildroot}/etc/dnf/vars
echo "10.0" > %{buildroot}/etc/dnf/vars/releasever

%files
/etc/dnf/vars/releasever
/var/log/journal

%changelog
* Fri Nov 28 2025 Yann Dirson <yann.dirson@vates.tech> - 0-0.ydi.2
- Initial release
