# The headers of the kernel's API, apart from the kernel, which all the packages are built with: they do not change
# with its patches, none of which changes the API, nor with its release. The version and the archive are the kernel's,
# whose build requires this version.
%global debug_package %{nil}
# the architecture of the kernel, whose headers differ by architecture
%ifarch aarch64
%global kernel_arch arm64
%else
%global kernel_arch x86
%endif

Name: kernel-headers
Version: 6.12.0
Release: 3%{dist}
License: GPLv2
Summary: Header files for the Linux kernel for use by glibc
URL: https://www.kernel.org/
Source0: UEK8-6.12.0-206.100.3.1.tar.xz
BuildRequires: gcc
BuildRequires: make
BuildRequires: rsync
Obsoletes: glibc-kernheaders < 3.0-46
Provides: glibc-kernheaders = 3.0-46
Conflicts: kernel-headers < %{version}
# for the kernel's build, which requires these headers, not Alma's of the same version
Provides: kernel-headers-xcpng = %{version}
ExclusiveArch: %{x86_64} aarch64

%description
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%prep
%autosetup -n linux-%{version}

%build

%install
make ARCH=%{kernel_arch} INSTALL_HDR_PATH=%{buildroot}/usr headers_install

%check
# the system calls of the architecture: read is 63 on arm64, which has the headers of SVE too, and 0 on x86
%ifarch aarch64
grep -q '^#define __NR_read 63$' %{buildroot}/usr/include/asm/unistd_64.h
test -e %{buildroot}/usr/include/asm/sve_context.h
%else
grep -q '^#define __NR_read 0$' %{buildroot}/usr/include/asm/unistd_64.h
%endif

%files
/usr/include/*

%changelog
* Thu Nov 05 2026 Gaëtan Lehmann <gaetan.lehmann@vates.tech> - 6.12.0-3
- The headers of the architecture built, arm64 ones for aarch64, rather than x86 ones for all

* Sat Oct 31 2026 Gaëtan Lehmann <gaetan.lehmann@vates.tech> - 6.12.0-2
- The headers of the kernel rebased on top of 6.12.0-206-100.3.1

* Wed Oct 21 2026 Gaëtan Lehmann <gaetan.lehmann@vates.tech> - 6.12.0-1
- The headers of the kernel, apart from it
