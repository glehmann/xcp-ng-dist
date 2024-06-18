%global package_speccommit 625e0d471768b079d3ea755ea73c9e821dac8b31
%global usver 20220801
%global xsver 1.7.5
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit edk2-stable202208

# submodule CryptoPkg/Library/OpensslLib/openssl
%define openssllib_cset d82e959e621a3d597f1e0d50ff8c2d8b96915fd7
%define openssllib_path CryptoPkg/Library/OpensslLib/openssl

# submodule BaseTools/Source/C/BrotliCompress/brotli
%define brotli_basetools_cset f4153a09f87cbb9c826d8fc12c74642bb2d879ea
%define brotli_basetools_path BaseTools/Source/C/BrotliCompress/brotli

# submodule MdeModulePkg/Library/BrotliCustomDecompressLib/brotli
%define brotli_lib_cset f4153a09f87cbb9c826d8fc12c74642bb2d879ea
%define brotli_lib_path MdeModulePkg/Library/BrotliCustomDecompressLib/brotli

Name: edk2
Summary: EFI Development Kit II
Version: 20220801
Release: %{?xsrel}.1%{?dist}

License: BSD and MIT
URL: https://github.com/tianocore/edk2
Source0: edk2-20220801.tar.gz
Source1: calc-pcrs.py
Source2: openssl-d82e959e621a3d597f1e0d50ff8c2d8b96915fd7.tar.gz
Source3: brotli-basetools-f4153a09f87cbb9c826d8fc12c74642bb2d879ea.tar.gz
Source4: brotli-lib-f4153a09f87cbb9c826d8fc12c74642bb2d879ea.tar.gz
Patch0: ovmfpkg-xenpvblkdxe__fix_memory_barrier_macro.patch
Patch1: ovmfxen-add-tpm-support.patch
Patch2: MdePkg-SecPeiDxeTimerLibCpu-Support-for-dynamic-PcdF.patch
Patch3: OvmfPkg-OvmfXen-Use-RuntimeTimerLibCpu-for-DXE_DRIVER.patch
Patch4: add-option-to-disable-bgrt.patch
Patch5: use-rtc.patch
Patch6: move-xenconnect-later.patch
Patch7: nvidia-vgpu-support.patch
Patch8: gvt-g-support.patch
Patch9: embed-nic-drivers.patch
Patch10: add-xen-variable.patch
Patch11: add-xen-platform-device-id.patch
Patch12: disable-modules.patch
Patch13: xenorder.patch
Patch14: keep-caching-enabled.patch
Patch15: remove-unused-crypto.patch
Patch16: add-Tcg2PhysicalPresenceLibXen.patch
Patch17: tcg2config-fix-operation-parameter-prompt.patch
Patch18: set-tpm2-acpi-table-revision.patch
Patch19: disable-config-option-in-TCG2-config-screen.patch
Patch20: shadow-pei-for-consistent-measurements.patch
Patch21: set-default-resolution-1024-768.patch
Patch22: add-debugging-info.patch
Patch23: pixiefail-p1.patch
Patch24: pixiefail-p2.patch
Patch25: pixiefail-p3.patch
Patch26: pixiefail-p4.patch
Patch27: pixiefail-p5.patch
Patch28: pixiefail-p6.patch
Patch29: pixiefail-p7.patch
Patch30: pixiefail-p8.patch
Patch31: pixiefail-p9.patch
Patch32: pixiefail-p10.patch
Patch33: pixiefail-p11.patch
Patch34: pixiefail-p12.patch

# XCP-ng patches
Patch1001: UefiCpuPkg-CpuMpPei-Workaround-page-table-allocation.patch

BuildRequires: devtoolset-11-binutils
BuildRequires: devtoolset-11-gcc
BuildRequires: devtoolset-11-gcc-c++
BuildRequires: python3
BuildRequires: libuuid-devel
BuildRequires: nasm >= 2.15
BuildRequires: iasl
BuildRequires: ipxe-efi
%{?_cov_buildrequires}


%description
Provides the Open Virtual Machine Firmware (OVMF) built for x64.
This is a build of the EFI Development Kit II suitable for using
as firmware in a virtual machine.


%prep
%autosetup -p1
%{?_cov_prepare}

# submodule CryptoPkg/Library/OpensslLib/openssl
tar xzf %{SOURCE2}
# submodule BaseTools/Source/C/BrotliCompress/brotli
tar xzf %{SOURCE3}
# submodule MdeModulePkg/Library/BrotliCustomDecompressLib/brotli
tar xzf %{SOURCE4}


%build

source /opt/rh/devtoolset-11/enable

cp %{_datadir}/ipxe/10ec8139.efi .
cp %{_datadir}/ipxe/8086100e.efi .

# Add "-D DEBUG_ON_HYPERVISOR_CONSOLE" to print logs to Xen's console and avoid
# the need to change qemu-wrapper.

%{?_cov_wrap} OvmfPkg/build.sh \
    -D SECURE_BOOT_ENABLE=TRUE \
    -D BGRT_ENABLE=FALSE \
    -D NETWORK_IP6_ENABLE=TRUE \
    -D IPXE_ENABLE=TRUE \
    -D NETWORK_HTTP_BOOT_ENABLE=FALSE \
    -D NETWORK_TLS_ENABLE=FALSE \
    -D NETWORK_ISCSI_ENABLE=FALSE \
    -D XEN_VARIABLE_ENABLE=TRUE \
    -D EXTRA_MODULES_ENABLE=FALSE \
    -D FD_SIZE_2MB \
    -D TPM1_ENABLE=FALSE \
    -D TPM2_ENABLE \
    -b DEBUG \
    --pcd gEfiMdePkgTokenSpaceGuid.PcdDebugPrintErrorLevel=0xFFFFFF4F \
    --pcd gUefiCpuPkgTokenSpaceGuid.PcdCpuMaxLogicalProcessorNumber=96 \
    -p OvmfPkg/OvmfXen.dsc -n %{?_smp_flags}

cp Build/OvmfXen/DEBUG_GCC*/FV/OVMF.fd OVMF-debug.fd
python3 %{SOURCE1} Build/OvmfXen/DEBUG_GCC*/FV/PEIFV.Fv Build/OvmfXen/DEBUG_GCC*/FV/DXEFV.Fv > OVMF-debug.pcrs
rm -rf Build/OvmfXen/DEBUG_GCC*

%{?_cov_wrap} OvmfPkg/build.sh \
    -D SECURE_BOOT_ENABLE=TRUE \
    -D BGRT_ENABLE=FALSE \
    -D NETWORK_IP6_ENABLE=TRUE \
    -D IPXE_ENABLE=TRUE \
    -D NETWORK_HTTP_BOOT_ENABLE=FALSE \
    -D NETWORK_TLS_ENABLE=FALSE \
    -D NETWORK_ISCSI_ENABLE=FALSE \
    -D XEN_VARIABLE_ENABLE=TRUE \
    -D EXTRA_MODULES_ENABLE=FALSE \
    -D FD_SIZE_2MB \
    -D TPM1_ENABLE=FALSE \
    -D TPM2_ENABLE \
    -b DEBUG \
    --pcd gEfiMdePkgTokenSpaceGuid.PcdDebugPrintErrorLevel=0x80000000 \
    --pcd gUefiCpuPkgTokenSpaceGuid.PcdCpuMaxLogicalProcessorNumber=96 \
    -p OvmfPkg/OvmfXen.dsc -n %{?_smp_flags}

cp Build/OvmfXen/DEBUG_GCC*/FV/OVMF.fd OVMF-release.fd
python3 %{SOURCE1} Build/OvmfXen/DEBUG_GCC*/FV/PEIFV.Fv Build/OvmfXen/DEBUG_GCC*/FV/DXEFV.Fv > OVMF-release.pcrs


%install

source /opt/rh/devtoolset-11/enable

install -m 755 -d %{buildroot}/%{_datadir}/%{name}
install -m 644 OVMF-debug.fd %{buildroot}/%{_datadir}/%{name}/OVMF-debug.fd
install -m 644 OVMF-release.fd %{buildroot}/%{_datadir}/%{name}/OVMF-release.fd
ln -sf OVMF-release.fd %{buildroot}/%{_datadir}/%{name}/OVMF.fd

install -m 644 OVMF-debug.pcrs %{buildroot}/%{_datadir}/%{name}/OVMF-debug.pcrs
install -m 644 OVMF-release.pcrs %{buildroot}/%{_datadir}/%{name}/OVMF-release.pcrs

cp OvmfPkg/License.txt License.ovmf
# cp CryptoPkg/Library/OpensslLib/openssl-xs/LICENSE LICENSE.openssl

%{?_cov_install}


%files
%license License.txt
%license License.ovmf
#%license LICENSE.openssl
%{_datadir}/%{name}

%{?_cov_results_package}


%changelog
* Tue Jun 18 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 20220801-1.7.5.1
- Sync with 20220801-1.7.5
- *** Upstream changelog ***
- * Wed Mar 20 2024 Ross Lagerwall <ross.lagerwall@citrix.com> - 20220801-1.7.5
- - CA-390410: Disable some unneeded modules
- - CA-390410: Downgrade some errors to warnings

* Mon Apr 08 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 20220801-1.7.4.1
- Sync with 20220801-1.7.4
- *** Upstream changelog ***
- * Fri Feb 02 2024 Ross Lagerwall <ross.lagerwall@citrix.com> - 20220801-1.7.4
- - CA-388017: Fix most PixieFail vulnerabilities
- - Fix CVE-2023-45229 - Integer underflow when processing IA_NA/IA_TA options in a DHCPv6 Advertise message
- - Fix CVE-2023-45230 - Buffer overflow in the DHCPv6 client via a long Server ID option
- - Fix CVE-2023-45231 - Out of Bounds read when handling a ND Redirect message with truncated options
- - Fix CVE-2023-45232 - Infinite loop when parsing unknown options in the Destination Options header
- - Fix CVE-2023-45233 - Infinite loop when parsing a PadN option in the Destination Options header
- - Fix CVE-2023-45234 - Buffer overflow when processing DNS Servers option in a DHCPv6 Advertise message
- - Fix CVE-2023-45235 - Buffer overflow when handling Server ID option from a DHCPv6 proxy Advertise message

* Wed Jan 31 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 20220801-1.7.3.2
- Rebuild for ipxe-efi-20180514gite7f67d5-1.0.3.xcpng8.3

* Wed Jan 24 2024 Thierry Escande <thierry.escande@vates.tech> - 20220801-1.7.3.1
- Add patch to workaround crash in page table allocation

* Tue Nov 28 2023 Alejandro Vallejo <alejandro.vallejo@cloud.com> - 20220801-1.7.3
- CP-46796: Allow booting up to 96 vCPUs

* Wed Sep 20 2023 Ross Lagerwall <ross.lagerwall@citrix.com> - 20220801-1.7.2
- CA-383046: Use the emulated RTC to implement time services
- CA-383095: Add a patch to fix an unusual Windows PXE boot hang
- CP-45175: Add debug messages to XenVariable
- CP-45175: Disable the BGRT
- CP-45175: Add extra debug statements
- CP-45175: Tweak debug levels
- Include g++ from devtoolset as a build requirement

* Fri May 26 2023 Ross Lagerwall <ross.lagerwall@citrix.com> - 20220801-1.7.1
- CA-377781: Set default resolution back to 1024x768

* Thu Mar 30 2023 Anthony PERARD <anthony.perard@citrix.com> - 20220801-1.7.0
- Update to newer version, edk2-stable202208 release.

* Wed Mar 29 2023 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.6.0
- CP-41446: Enable IPv6 support

* Fri Nov 11 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.5.1
- CA-372205: OVMF: Shadow PEI for consistent measurements
- CA-372205: Calculate PCR 0 and 2 at build time

* Wed Aug 17 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.5.0
- Add TPM support

* Mon Aug 01 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.8
- CA-343027: Fix hang in OVMF

* Fri Jun 17 2022 Mark Syms <mark.syms@citrix.com> - 20180522git4b8552d-1.4.7
- Fix script typo which breaks static analysis

* Mon Feb 21 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.6
- CP-38416: Enable static analysis

* Mon Jan 18 2021 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.5
- CA-350259: Fix PCI passthrough of devices with 64+ GB BARs

* Fri Dec 04 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.4
- CP-35517: Bump release to rebuild

* Wed Jun 24 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.3
- CA-337679: Fix triple fault while booting on a heavy loaded host

* Thu Jul 04 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.2
- CA-322248: Prevent guest attempting to accessing priv regsiters

* Wed Jun 19 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.1
- CA-321788: make vGPU console work with all NVidia cards
- Replace local fixes with upstream backports

* Thu May 30 2019 Edwin Török <edvin.torok@citrix.com> - 20180522git4b8552d-1.4.0
- CP-30786: Turn off cryptopkg when secure boot is off
- Fix typo in secure boot enable condition
- CA-314662: Don't accidentally switch off MTRRs in SEC phase
- CA-309841: reenable PV drivers in OVMF
- CP-30787: disable unneeded crypto code, simplify patchqueue

* Tue Dec 18 2018 Edwin Török <edvin.torok@citrix.com> - 20180522git4b8552d-1.2.0
- CA-293636: Add support for NVIDIA vGPU on top of UEFI
- CA-293633: Set default video resoultion to 1024x768
- CA-293634: Various fixes to make GPU/PCI passthrough work
- Add a config option to use iPXE drivers
- Cleanup XenVariable integration
- CA-297602: Speedup boot by enabling PV drivers
- CA-298449: Add basic support for Intel GVT-g on top of UEFI
- Fix race finding XenVariable PCI device
- CA-296489: Allow boot ordering to be set from XS
- CA-296489: Make Xen boot ordering work with normal boot entries
- Remove unused patches
- CA-296489: XenBootOrder: Fix a typo
- CP-28675: XenVariable: Make some functions static
- CP-28675: XenVariable: Move useful functions into a header file
- CP-28675: XenVariable: Notify dom0 on Security Violation
- CP-29100: Remove PCI Device and expose IO port for communication with varstored.
- CP-29100: Remove previous workaround related to Xen Variable PCI device
- CA-297688: Keep caching enabled during SEC phase

* Thu May 17 2018 Ross Lagerwall <ross.lagerwall@citrix.com> - 20170920git947f373-1.0.0
- Initial packaging.
