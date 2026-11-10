%global package_speccommit 379e71369244d7e895220e370b25cd258a94d029
%global usver 0.7.3
%global xsver 6
%global xsrel %{xsver}%{?xscount}%{?xshash}

Name:         biosdevname
Version:      0.7.3
Release: %{?xsrel}.1%{?dist}
Summary:      Helper for naming devices per BIOS names

Group:        System Environment/Base
License:      GPLv2
URL:          http://linux.dell.com/files/%{name}
Provides:     xenserver-biosdevname
# SMBIOS only exists on these arches, and on aarch64 servers with UEFI.  It's also likely that other
# arches don't expect the PCI bus to be sorted breadth-first, or of
# so, there haven't been any comments about that on LKML.
ExclusiveArch: %{ix86} x86_64 ia64 aarch64
# Get from https://github.com/dell/biosdevname
Source0: biosdevname-0.7.3-3.tar.gz
Patch0: biosdevname-disable-udev.patch
Patch1: biosdevname-CA13344.patch
Patch2: biosdevname-revert-default-policy.patch
Patch3: biosdevname-remove-virtual-devices.patch
Patch4: biosdevname-disable-vm-check.patch
Patch5: biosdevname-fix-output-format.patch

BuildRequires: gcc
BuildRequires: pciutils-devel
BuildRequires: zlib-devel
BuildRequires: autoconf libtool
%{?_cov_buildrequires}

%define _default_patch_fuzz 0

%description
biosdevname in its simplest form takes a kernel device name as an
argument, and returns the BIOS-given name it "should" be.  This is necessary
on systems where the BIOS name for a given device (e.g. the label on
the chassis is "Gb1") doesn't map directly and obviously to the kernel
name (e.g. eth0).

%prep
%autosetup -p1
%{?_cov_prepare}

%build
./autogen.sh --disable-rpath --prefix=/ --sbindir=/sbin --mandir=%{_mandir}
%{?_cov_wrap} make %{?_smp_mflags}


%install
make install install-data DESTDIR=%{buildroot}
%{?_cov_install}

%files
%defattr(-,root,root,-)
%doc COPYING README
/sbin/%{name}
%{_mandir}/man1/%{name}.1*.gz

%{?_cov_results_package}


%changelog
* Tue Nov 10 2026 Gaëtan Lehmann <gaetan.lehmann@vates.tech> - 0.7.3-6.1
- Build for aarch64 too. xcp-python-libs and host-installer also need it on
  this architecture 

* Wed Jan 22 2025 XenServer Rebuild <rebuild@xenserver.com> - 0.7.3-6
- CP-53310: XenServer 9 rebuild

* Tue Jan 21 2025 XenServer Rebuild <rebuild@xenserver.com> - 0.7.3-5
- CP-53310: XenServer 9 rebuild

* Thu Jan 16 2025 XenServer Rebuild <rebuild@xenserver.com> - 0.7.3-4
- Add XS8 release branch
- CP-53241: XenServer 9 rebuild

* Mon Jan 29 2024 Gerald Elder-Vass <gerald.elder-vass@cloud.com> - 0.7.3-3
- CP-46269: Fix koji build

* Fri Jan 12 2024 Gerald Elder-Vass <gerald.elder-vass@cloud.com> - 0.7.3-2
- CP-46269: Update to latest biosdevname commit

* Tue Aug 29 2023 Lin Liu <lin.liu@citrix.com> - 0.7.3-1
- CP-45046: Build 0.7.3

