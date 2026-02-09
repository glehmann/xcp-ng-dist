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

# journald config overrides
install -d -m755 %{buildroot}%{_prefix}/lib/systemd/journald.conf.d
cat > %{buildroot}%{_prefix}/lib/systemd/journald.conf.d/00-xcpng.conf <<'EOF'
[Journal]
# allow use of 3G of the 3.3G log filesystem (default was 10%)
SystemMaxUse=3G
EOF
# place for users to set their own overrides
install -d -m755 %{buildroot}%{_sysconfdir}/systemd/journald.conf.d
cat > %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/90-custom.conf <<'EOF'
# This file is reserved for user customisation, preserved on upgrade
EOF

%files
%config(noreplace) %{_sysconfdir}/systemd/journald.conf.d/90-custom.conf
%{_prefix}/lib/systemd/
/var/log/journal/

%changelog
* Mon Nov 09 2026 Yann Dirson <yann.dirson@vates.tech> - 0-1
- Initial release
- Enable persistent systemd journal with suitably large size, enable user overrides
