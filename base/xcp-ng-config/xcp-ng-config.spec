Name:           xcp-ng-config
Version:        0
Release:        0.ydi.6%{?dist}

Summary:        XCP-ng configuration files
Group:          System Environment/Base
License:        GPL-2.0-or-later
URL:            https://xcp-ng.org
Source0:        system-snapshot
Source1:        system-snapshots.txt

Requires: bash btrfs-progs coreutils findutils tar util-linux systemd

Obsoletes:      xcp-ng-release < 8.99.0-0.8.ydi.17

%description
XCP-ng configuration files

%install
install -D -m700 %{SOURCE0} %{buildroot}%{_libexecdir}/xcp-ng/system-snapshot
install -D -m700 %{SOURCE0} %{buildroot}%{_libexecdir}/xcp-ng/system-restore
install -m644 %{SOURCE1} %{buildroot}%{_libexecdir}/xcp-ng/README

# enable persistent systemd journal
install -d -m755 %{buildroot}/var/log/journal

# pin Almalinux version to avoid upgrade to 10.1+
mkdir -p %{buildroot}/etc/dnf/vars
echo "10.0" > %{buildroot}/etc/dnf/vars/releasever

# Add xcp-ng repo.  The ID has to match XAPI updater.py plugin.
install -d -m 755 %{buildroot}%{_sysconfdir}/yum.repos.d
# install -m 644 xcp-ng.repo %{buildroot}%{_sysconfdir}/yum.repos.d
cat > %{buildroot}%{_sysconfdir}/yum.repos.d/xcp-ng.repo <<'EOF'
[xcp-ng-base]
name=XCP-ng 9 proto
baseurl=https://repo.vates.tech/xcp-ng/9/8.99/base/x86_64_v2/
priority=1
failovermethod=priority
skip_if_unavailable=False
# nothing signed yet
#gpgkey=https://xcp-ng.org/RPM-GPG-KEY-xcpng
gpgcheck=0
EOF

%files
%dir %{_libexecdir}/xcp-ng
%{_libexecdir}/xcp-ng/system-snapshot
%{_libexecdir}/xcp-ng/system-restore
%{_libexecdir}/xcp-ng/README
%{_sysconfdir}/dnf/vars/releasever
/var/log/journal
%{_sysconfdir}/yum.repos.d/

%changelog
* Wed Oct 28 2026 Gaëtan Lehmann <gaetan.lehmann@vates.tech> - 0-0.ydi.6
- Package system snapshot helpers

* Tue Dec 16 2025 Yann Dirson <yann.dirson@vates.tech> - 0-0.ydi.5
- Initial release
