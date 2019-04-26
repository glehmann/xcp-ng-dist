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
Version: %{date}
Release: 1.0.2%{?dist}
License: GPLv2

Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/ipxe/archive?at=a712dae709a&format=tar.gz&prefix=ipxe-20121005#/ipxe-20121005.tar.gz

Patch0: makefile.patch
Patch1: ipxe-eb5a2ba5962579e514b377f5fdab7292be0fb2a7.patch
Patch2: ipxe-9df238a8aa1c6074f98280d9dfa08c4ea7e1ff86.patch
Patch3: ipxe-66ea4581256449fe9dcb26340851c09ffd9d6290.patch
Patch4: 0001-dhcp-Check-for-matching-chaddr-in-received-DHCP-pack.patch
Patch5: 0001-pxe-Maintain-a-queue-for-received-PXE-UDP-packets.patch
Patch6: pxe-tftp-load-from-program-pxecall.patch
Patch7: ipxe-do-not-implement-UNDI-GET_NEXT-if-PVS.patch
Patch8: ipxe-udp-write-blocking.patch
Patch9: ipxe-no-post-prompt.patch
Patch10: 0001-Check-Vendor-Class-ID-from-PROXYDHCP_SETTINGS_NAME.patch
Patch11: 0001-CA-247413-Make-pxebs-accept-broadcast-DHCP-packets.patch
Patch12: 0001-dhcp-Remove-obsolete-dhcp_chaddr-function.patch
Patch13: 0002-dhcp-Allow-pseudo-DHCP-servers-to-use-pseudo-identif.patch
Patch14: 0003-dhcp-Ignore-ProxyDHCPACKs-without-PXE-options.patch
Patch15: 0004-dhcp-Do-not-skip-ProxyDHCPREQUEST-if-next-server-is-.patch

Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/ipxe/archive?at=a712dae709a&format=tar.gz&prefix=ipxe-20121005#/ipxe-20121005.tar.gz) = a712dae709adc76c76646fa1c86d2cfb5c3edfbc
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/ipxe.pg/archive?at=1.0.2&format=tar#/ipxe-source.patches.tar) = 6ff61ccd153684e00f25d38f9b7d807010c459a9

BuildArch: noarch

BuildRequires: perl
BuildRequires: syslinux
BuildRequires: mtools
BuildRequires: mkisofs
BuildRequires: binutils-devel
BuildRequires: xz-devel

%description
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

%prep
%autosetup -p1 -n %{src_name}-%{version}

%build
make %{?_smp_mflags} -C src bin/rtl8139.rom
make %{?_smp_mflags} -C src bin/8086100e.rom

%install
cat src/bin/rtl8139.rom src/bin/8086100e.rom > src/bin/ipxe.bin
install -D -m 0644 src/bin/ipxe.bin %{buildroot}/%{_datadir}/%{name}/ipxe.bin

%files
%{_datadir}/%{name}/ipxe.bin

%changelog
* Mon Sep 24 2018 Sergey Dyasli <sergey.dyasli@citrix.com> - 20121005-1.0.2
- Initial packaging
