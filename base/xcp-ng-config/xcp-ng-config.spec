Name:           xcp-ng-config
Version:        0
Release:        1.3%{?dist}

Summary:        XCP-ng configuration files
Group:          System Environment/Base
License:        GPL-2.0-or-later
URL:            https://github.com/xcp-ng-rpms/xcp-ng-config
Source0:        system-snapshot
Source1:        system-snapshots.txt

Requires: bash btrfs-progs coreutils findutils tar util-linux systemd

Obsoletes:      xcp-ng-release < 8.99.0-0.8.ydi.17

# the directory of the repository of the architecture: x86_64_v2's, as $basearch is x86_64 there
%ifarch aarch64
%global repo_arch aarch64
%else
%global repo_arch x86_64_v2
%endif

%description
XCP-ng configuration files

%install
install -D -m700 %{SOURCE0} %{buildroot}%{_libexecdir}/xcp-ng/system-snapshot
install -D -m700 %{SOURCE0} %{buildroot}%{_libexecdir}/xcp-ng/system-restore
install -m644 %{SOURCE1} %{buildroot}%{_libexecdir}/xcp-ng/README

# enable persistent systemd journal
install -d -m755 %{buildroot}/var/log/journal

# journald config overrides
install -d -m755 %{buildroot}%{_prefix}/lib/systemd/journald.conf.d
# no upstream file in Alma 10.0
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

# Add xcp-ng repo.  The [repo-id] has to match XAPI updater.py plugin.
install -d -m 755 %{buildroot}%{_sysconfdir}/yum.repos.d
cat > %{buildroot}%{_sysconfdir}/yum.repos.d/xcp-ng.repo <<'EOF'
# This file will be overwritten on upgrade, do not modify
[xcp-ng-base]
name=XCP-ng 9 proto
baseurl=https://91.98.220.14/repos/9.0/incoming/latest/base/%{repo_arch}/
priority=1
failovermethod=priority
skip_if_unavailable=False
# not checked until all the packages are signed; the installer imports the key of the ISO, like that of CI
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-xcpng file:///etc/pki/rpm-gpg/RPM-GPG-KEY-AlmaLinux-10 file:///etc/pki/rpm-gpg/RPM-GPG-KEY-AlmaLinux-10-EPEL-AltArch file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-10
gpgcheck=0
EOF

# Permit ssh root login
install -d -m 700 %{buildroot}%{_sysconfdir}/ssh/sshd_config.d
# "30" sorts before Alma 10.0's "40" and leaves room for overriding
cat > %{buildroot}%{_sysconfdir}/ssh/sshd_config.d/30-xcpng.conf <<'EOF'
# This file will be overwritten on upgrade, do not modify
PermitRootLogin yes
EOF
cat > %{buildroot}%{_sysconfdir}/ssh/sshd_config.d/00-custom.conf <<'EOF'
# This file is reserved for user customisation, preserved on upgrade
EOF

# Mask services installed by iptables-services
install -d -m 755 %{buildroot}%{_sysconfdir}/systemd/system
ln -s /dev/null %{buildroot}%{_sysconfdir}/systemd/system/iptables.service
ln -s /dev/null %{buildroot}%{_sysconfdir}/systemd/system/ip6tables.service

%files
%dir %{_libexecdir}/xcp-ng
%{_libexecdir}/xcp-ng/system-snapshot
%{_libexecdir}/xcp-ng/system-restore
%{_libexecdir}/xcp-ng/README
%config(noreplace) %{_sysconfdir}/ssh/sshd_config.d/00-custom.conf
%config %{_sysconfdir}/ssh/sshd_config.d/30-xcpng.conf
%{_sysconfdir}/systemd/system/iptables.service
%{_sysconfdir}/systemd/system/ip6tables.service
%config(noreplace) %{_sysconfdir}/systemd/journald.conf.d/90-custom.conf
%{_sysconfdir}/yum.repos.d/
%{_prefix}/lib/systemd/
/var/log/journal/

%changelog
* Wed Nov 25 2026 Gaëtan Lehmann <gaetan.lehmann@vates.tech> - 0-1.3
- Package the system snapshot helpers

* Wed Nov 25 2026 Gaëtan Lehmann <gaetan.lehmann@vates.tech> - 0-1.2
- The repository of the architecture of the host, aarch64's too, rather than x86_64_v2's

* Wed Nov 11 2026 Gaëtan Lehmann <gaetan.lehmann@vates.tech> - 0-1.1
- The repository of xcp-ng-dist, https://91.98.220.14/repos/9.0/incoming/latest/base/x86_64_v2/
- List the keys of the packages in the repository, still not checked as not all signed

* Mon Nov 09 2026 Yann Dirson <yann.dirson@vates.tech> - 0-1
- Initial release
- Enable persistent systemd journal with suitably large size, enable user overrides
- Ship xcp-ng.repo, previously in xcp-ng-release
- Permit ssh root login
- Disable iptables.service
