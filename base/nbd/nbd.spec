%global package_speccommit 2bb484be55bd196f9997d5813cae841e1895bfaf
%global usver 3.24
%global xsver 1
%global xsrel %{xsver}%{?xscount}%{?xshash}

Name:    nbd
Version: 3.24
Release: %{?xsrel}%{?dist}
Summary: Network Block Device user-space tools (TCP version)
License: GPLv2
URL:     http://nbd.sourceforge.net
Source0: nbd-3.24.tar.xz
Source1: nbd-server.service
Source2: nbd-server.sysconfig

BuildRequires: make
BuildRequires:  gcc
BuildRequires:  glib2-devel >= 2.26
BuildRequires:  gnutls-devel
BuildRequires:  zlib-devel
BuildRequires:  libnl3-devel
BuildRequires:  bison
BuildRequires:  systemd
%{?systemd_requires}

%description
Tools for the Linux Kernel's network block device, allowing you to use
remote block devices over a TCP/IP network.

%prep
%autosetup -p1
# wait longer for nbd-server to fully start,
# five seconds may not be enough on Koji building infra
sed -i 's/tv_sec = 5/tv_sec = 20/' tests/run/nbd-tester-client.c

%build
%configure --enable-syslog --enable-lfs --enable-gznbd
%make_build

%install
%make_install
install -pDm644 systemd/nbd@.service %{buildroot}%{_unitdir}/nbd@.service
mkdir -p %{buildroot}%{_unitdir}/nbd@.service.d
cat > %{buildroot}%{_unitdir}/nbd@.service.d/modprobe.conf <<EOF
[Service]
ExecStartPre=/sbin/modprobe nbd
EOF
install -pDm644 %{S:1} %{buildroot}%{_unitdir}/nbd-server.service
install -pDm644 %{S:2} %{buildroot}%{_sysconfdir}/sysconfig/nbd-server

%check
# wait longer for nbd-server to fully start,
# one second may not be enough on Koji building infra
DELAY=10 make check

%post
%systemd_post nbd-server.service

%preun
%systemd_preun nbd-server.service

%postun
%systemd_postun nbd-server.service

%files
%doc README.md doc/*.md doc/todo.txt
%license COPYING
%{_bindir}/nbd-server
%{_bindir}/nbd-trdump
%{_bindir}/nbd-trplay
%{_bindir}/gznbd
%{_mandir}/man*/nbd*
%{_sbindir}/nbd-client
%{_sbindir}/min-nbd-client
%config(noreplace) %{_sysconfdir}/sysconfig/nbd-server
%{_unitdir}/nbd-server.service
%{_unitdir}/nbd@.service
%{_unitdir}/nbd@.service.d

%changelog
* Fri Feb 03 2023 Tim Smith <tim.smith@citrix.com> - 3.24-1
- First local build
