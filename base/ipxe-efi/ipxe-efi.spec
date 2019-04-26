%global ipxe_date 20180514
%global ipxe_githash e7f67d5

Name: ipxe-efi
Summary: iPXE EFI drivers
Version: %{ipxe_date}git%{ipxe_githash}
Release: 1.0.0%{?dist}

License: GPLv2

Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/ipxe/archive?at=e7f67d5&format=tar.gz&prefix=ipxe-efi-20180514gite7f67d5#/ipxe-efi-20180514gite7f67d5.tar.gz

Patch0: increase-heap-size.patch
Patch1: realtek-increase-rx-desc.patch
Patch2: efi-snp-limit-rx-queue.patch

Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/ipxe/archive?at=e7f67d5&format=tar.gz&prefix=ipxe-efi-20180514gite7f67d5#/ipxe-efi-20180514gite7f67d5.tar.gz) = e7f67d5a4c6e9f06aa7a9db1b4245f5e16f00bb2
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/ipxe-efi.pg/archive?at=v1.0.0&format=tar#/ipxe-efi.patches.tar) = b869c2c2a13c274ca59e583bbac4dec9c8f80f14



%description
A build of iPXE in the form of EFI NIC drivers that can be used in an
UEFI environment or embedded into OVMF.


%prep
%autosetup -p1


%build
make -C src %{?_smp_mflags} bin-x86_64-efi/10ec8139.drv.efi CONFIG=qemu
make -C src %{?_smp_mflags} bin-x86_64-efi/8086100e.drv.efi CONFIG=qemu


%install
install -m 755 -d %{buildroot}/%{_datadir}/ipxe
install -m 644 src/bin-x86_64-efi/10ec8139.drv.efi %{buildroot}/%{_datadir}/ipxe/10ec8139.efi
install -m 644 src/bin-x86_64-efi/8086100e.drv.efi %{buildroot}/%{_datadir}/ipxe/8086100e.efi


%files
%license COPYING
%license COPYING.GPLv2
%{_datadir}/ipxe


%changelog
* Wed Jul 04 2018 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180514gite7f67d5-1
- Package iPXE for EFI builds
