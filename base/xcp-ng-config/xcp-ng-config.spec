Name:           xcp-ng-config
Version:        0
Release:        1%{?dist}

Summary:        XCP-ng configuration files
Group:          System Environment/Base
License:        GPL-2.0-or-later
URL:            https://github.com/xcp-ng-rpms/xcp-ng-config

Obsoletes:      xcp-ng-release < 8.99.0-0.8.ydi.17

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

# Add xcp-ng repo.  The [repo-id] has to match XAPI updater.py plugin.
install -d -m 755 %{buildroot}%{_sysconfdir}/yum.repos.d
cat > %{buildroot}%{_sysconfdir}/yum.repos.d/xcp-ng.repo <<'EOF'
# This file will be overwritten on upgrade, do not modify
[xcp-ng-base]
name=XCP-ng 9 proto
baseurl=https://updates.xcp-ng.org/9/9.0/incoming/x86_64_v2/
priority=1
failovermethod=priority
skip_if_unavailable=False
# nothing signed yet
#gpgkey=https://xcp-ng.org/RPM-GPG-KEY-xcpng
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

# Distro key for RPM signature verification
install -d -m 755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
cat > %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-xcpng9 <<'EOF'
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

mQINBGruDxYBEACpHyGFugkR1Jqj9SAKeD5zCmX/yV+pI7eMM7UG59XZkx/4V1/p
HKrgsF4fBiH93sNjHhWoWKK9RPfMAlvBTRjO59s5Rl4El59WD9zPTdUxJeJDQLks
flXQjAyq9FtnErFK+jRT1i/b7bLsFuKzsz4Pskx3uSUCYxCf2ceUv0K0/NSJ9z3R
59VXI+4GlzgCSCwiggD5hpLNtF092nrnxUorVLqFPrBy+rP/aIXQ3Bjs/dzUz46j
GJPYX1vni6AxkADCvP4GSe2YgkKBvPc3nhcqjn1mnlr/EDVnuydqwFQjnr5lPjUM
bRbDXvqXaE4AaNc2m/q+SngQF478/JEh/hMt10/SLmvnvQf91JyiumlXpMcG9777
Tp2YoZp4OSAqY6Hm8CBWS2mTVKDdKwuAmBSx5XUMn85fuf9XgSh0BYvwPk3tCZ32
q5H5+YqGgVwWo+jT+gy8bRBLR8zOKfv6fll9bK1RH7FJHUdvsp6dIJqLeqsllONo
zFgR4ysOlGlT/mSsFokSHiOlOygH7bTXoiBzD0qgoRucrsbrxaUxKeZfiT+aUyfL
j3Vs8IDdlSXKuEwwllT/LeUXdwXyj6QCrCks/4wp9zBKNCraEeS9wh+XT2C6koyw
udZKIVn3msua40SLpr+orr1693CPO3JylLvYk3nzZIHh2VB7HUfLzvXPdwARAQAB
tEJYQ1AtbmcgOSBLZXkgKFhDUC1uZyA5IE9mZmljaWFsIFNpZ25pbmcgS2V5KSA8
c2VjdXJpdHlAeGNwLW5nLm9yZz6JAjgEEwEIACIFAmruDxYCGwMGCwkIBwMCBhUI
AgkKCwQWAgMBAh4BAheAAAoJEOX2E7m1AZb8CtwP/1KDzY7m/cL678BPkLlnf7S3
KrRBGv17KNX6CKH+l1hBkOazmFCfZFi5/zlIQYgRYuMuTxKeVuYAjqywd+oNS3Ot
j7ruUrT4y4pNgJMFxAUwfz6cKqezdhmXHKfNXKxedIDknhDOWgLf/6ZmCr3w0Ddp
Z/paFTZ1a9Y1bqiGH2hr0Z72EY2pAW0Wpjt3EXPFyqurhtpVKiZoRMX4pe72sA9x
cPNW7jsi4kf4U3Qb/s0AMVA8DVU+EiVOo0NTXlA1KVJiRpL0plngLy+O/Ho/9UTn
fW7VWAJGCsEfL0w3uHxbCfSGzGiGFPirAqovl6pzchdcuHqTZbZG0Z/mbXDO9QM1
vvDI2W7jdN/DbA5a4SqkyTAN9W9NkJrE/cdQ9zSvVPO6OI8r96z2bZ3P9aAp33IL
fq/5oioP+A5h1whIyuLwWRdJTA2/VqzbagCtkTnN2H0bIUZG379xQq8P/Z4nusOw
3yVR9J/vyw7W58YiRIusSsJaFFoZrjIfEoyeYrXnsa2I4E6/zX1i1CzDrs+52O6o
pst5Df3X1HOEHy0wIsjwZxH+oa41HchCNRy0phy5jJZf7nQyynhMOCPxoiKaagnU
WXkBeeAt8tYCd3Yo8OJfoLsRxKhEUhxD/Oc6WKWSJyLK4hG0wRppeeuk0ORs101w
7aLywW75OquORc0lJ4+z
=WlOg
-----END PGP PUBLIC KEY BLOCK-----
EOF

%files
%config(noreplace) %{_sysconfdir}/ssh/sshd_config.d/00-custom.conf
%config %{_sysconfdir}/ssh/sshd_config.d/30-xcpng.conf
%config(noreplace) %{_sysconfdir}/systemd/journald.conf.d/90-custom.conf
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-xcpng9
%{_sysconfdir}/yum.repos.d/
%{_prefix}/lib/systemd/
/var/log/journal/

%changelog
* Mon Nov 09 2026 Yann Dirson <yann.dirson@vates.tech> - 0-1
- Initial release
- Enable persistent systemd journal with suitably large size, enable user overrides
- Ship xcp-ng.repo, previously in xcp-ng-release
- Permit ssh root login
- Include GPG key for XCP-ng 9
