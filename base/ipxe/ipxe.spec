%global package_speccommit 9047e9f1fa9daad02098fb628df6270f760fdf4e
%global usver 20121005
%global xsver 1.0.6
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit a712dae709a

# Resulting binary formats we want from iPXE
%global formats rom

# We only build the ROMs if on an x86 build host. The resulting
# binary RPM will be noarch, so other archs will still be able
# to use the binary ROMs.
#
# We do cross-compilation for 32->64-bit, but not for other arches
# because EDK II does not support big-endian hosts.
%global buildarches x86_64

# debugging firmwares does not goes the same way as a normal program.
# moreover, all architectures providing debuginfo for a single noarch
# package is currently clashing in koji, so don't bother.
%global debug_package %{nil}

# Upstream don't do "releases" :-( So we're going to use the date
# as the version, and a GIT hash as the release. Generate new GIT
# snapshots using the folowing commands:
#
# $ hash=`git log -1 --format='%h'`
# $ date=`date '+%Y%m%d'`
# $ git archive --output ipxe-${date}-git${hash}.tar.gz --prefix ipxe-${date}-git${hash}/ ${hash}
#
# And then change these two:
%global date 20121005
%global hash a712dae709a

%define src_name ipxe

Summary: A network boot loader
Name: ipxe
Version: 20121005
Release: %{?xsrel}%{?dist}
License: GPLv2
Source0: ipxe-20121005.tar.gz
Patch0: ipxe-eb5a2ba5962579e514b377f5fdab7292be0fb2a7.patch
Patch1: ipxe-9df238a8aa1c6074f98280d9dfa08c4ea7e1ff86.patch
Patch2: ipxe-66ea4581256449fe9dcb26340851c09ffd9d6290.patch
Patch3: 0001-dhcp-Check-for-matching-chaddr-in-received-DHCP-pack.patch
Patch4: 0001-pxe-Maintain-a-queue-for-received-PXE-UDP-packets.patch
Patch5: pxe-tftp-load-from-program-pxecall.patch
Patch6: ipxe-do-not-implement-UNDI-GET_NEXT-if-PVS.patch
Patch7: ipxe-udp-write-blocking.patch
Patch8: ipxe-no-post-prompt.patch
Patch9: 0001-Check-Vendor-Class-ID-from-PROXYDHCP_SETTINGS_NAME.patch
Patch10: 0001-CA-247413-Make-pxebs-accept-broadcast-DHCP-packets.patch
Patch11: 0001-dhcp-Remove-obsolete-dhcp_chaddr-function.patch
Patch12: 0002-dhcp-Allow-pseudo-DHCP-servers-to-use-pseudo-identif.patch
Patch13: 0003-dhcp-Ignore-ProxyDHCPACKs-without-PXE-options.patch
Patch14: 0004-dhcp-Do-not-skip-ProxyDHCPREQUEST-if-next-server-is-.patch
Patch15: ipxe-238050dfd46e3c4a87329da1d48b4d8dde5af8a1.patch
Patch16: serial-console.patch
BuildArch: noarch

BuildRequires: perl
BuildRequires: syslinux
BuildRequires: mtools
BuildRequires: mkisofs
BuildRequires: binutils-devel
BuildRequires: xz-devel
%{?_cov_buildrequires}

%description
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

%prep
%autosetup -p1 -n %{src_name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} make %{?_smp_mflags} -C src bin/rtl8139.rom
%{?_cov_wrap} make %{?_smp_mflags} -C src bin/8086100e.rom

%install
cat src/bin/rtl8139.rom src/bin/8086100e.rom > src/bin/ipxe.bin
install -D -m 0644 src/bin/ipxe.bin %{buildroot}/%{_datadir}/%{name}/ipxe.bin
%{?_cov_install}

%files
%{_datadir}/%{name}/ipxe.bin

%{?_cov_results_package}

%changelog
* Fri Feb 11 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 20121005-1.0.6
- CP-38416: Enable static analysis

* Tue Nov 30 2021 Ross Lagerwall <ross.lagerwall@citrix.com> - 20121005-1.0.5
- CA-359977: Output to the serial console by default

* Fri Dec 04 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 20121005-1.0.4
- CP-35517: Bump release to rebuild

* Fri Apr 12 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 20121005-1.0.3
- CA-294898: Backport patch for gcc bug

* Mon Sep 24 2018 Sergey Dyasli <sergey.dyasli@citrix.com> - 20121005-1.0.2
- Initial packaging
