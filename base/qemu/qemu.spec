%global package_speccommit e3e04d663da896dcd7691699a9cfd626e2eec0e9
%global usver 4.2.1
%global xsver 5.2.9
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit v4.2.1

# submodule ui/keycodemapdb
%define keycodemapdb_cset 22b8996dba9041874845c7446ce89ec4ae2b713d
%define keycodemapdb_path ui/keycodemapdb

# Control whether we build with the address sanitizer.
%define with_asan 0

Summary: qemu-dm device model
Name: qemu
Epoch: 2
Version: 4.2.1
Release: %{?xsrel}%{?dist}
License: GPL
Requires: xcp-clipboardd
Requires: xengt-userspace
## We broke an interface used by xenopsd-xc without version signalling
## so we have to carry a conflicts line to say we broke it.
Conflicts: xenopsd-xc < 0.123.0
Source0: qemu-4.2.1.tar.gz
Source2: keycodemapdb-22b8996dba9041874845c7446ce89ec4ae2b713d.tar.gz
Patch0: 0001-usb-fix-setup_len-init-CVE-2020-14364.patch
Patch1: 0001-scripts-checkpatch.pl-Only-allow-Python-3-interprete.patch
Patch2: 0002-scripts-Explicit-usage-of-Python-3-scripts-with-__ma.patch
Patch3: 0003-scripts-minikconf-Explicit-usage-of-Python-3.patch
Patch4: 0004-scripts-tracetool-Remove-shebang-header.patch
Patch5: 0005-scripts-Explicit-usage-of-Python-3-scripts-without-_.patch
Patch6: 0006-scripts-signrom-remove-Python-2-support-add-shebang.patch
Patch7: 0001-tests-qemu-iotests-check-Allow-use-of-python3-interp.patch
Patch8: 0001-tests-qemu-iotests-Explicit-usage-of-Python-3-script.patch
Patch9: 0002-tests-qemu-iotests-Explicit-usage-of-Python3-scripts.patch
Patch10: 0007-make-all-Python-scripts-executable.patch
Patch11: 0002-drop-from-__future__-import-print_function.patch
Patch12: 0001-aio-posix-fix-use-after-leaving-scope-in-aio_poll.patch
Patch13: 0003-scripts-qmp-Use-Python-3-interpreter.patch
Patch14: 0001-scripts-qmp-Fix-shebang-and-imports.patch
Patch15: 0001-xen-rework-pci_piix3_xen_ide_unplug.patch
Patch16: 0001-hw-ehci-destroy-sglist-in-error-path.patch
Patch17: 0002-hw-ehci-check-return-value-of-usb_packet_map.patch
Patch18: 0003-usb-hcd-ehci-Fix-error-handling-on-missing-device-fo.patch
Patch19: 0001-pci-assert-configuration-access-is-within-bounds.patch
Patch20: 0006-block-Avoid-stale-pointer-dereference-in-blk_get_aio.patch
Patch21: 0001-configure-Do-not-ignore-malloc-value.patch
Patch22: 0001-ide-atapi-assert-that-the-buffer-pointer-is-in-range.patch
Patch23: 0001-xen-bus-reduce-scope-of-backend-watch.patch
Patch24: 0001-ide-atapi-check-logical-block-address-and-read-size-.patch
Patch25: 0001-ui-update-keycodemapdb-submodule-commit.patch
Patch26: 0001-e1000-fail-early-for-evil-descriptor.patch
Patch27: 0001-net-introduce-qemu_receive_packet.patch
Patch28: 0002-e1000-switch-to-use-qemu_receive_packet-for-loopback.patch
Patch29: 0003-rtl8139-switch-to-use-qemu_receive_packet-for-loopba.patch
Patch30: 0001-xen-mapcache-avoid-a-race-on-memory-map-while-using-.patch
Patch31: 0001-net-eth-Use-correct-in6_address-offset-in-_eth_get_r.patch
Patch32: 0002-net-eth-Simplify-_eth_get_rss_ex_dst_addr.patch
Patch33: 0003-net-eth-Better-describe-_eth_get_rss_ex_dst_addr-s-o.patch
Patch34: 0004-net-eth-Check-size-earlier-in-_eth_get_rss_ex_dst_ad.patch
Patch35: 0005-net-eth-Check-iovec-has-enough-data-earlier.patch
Patch36: 0006-net-eth-Read-ip6_ext_hdr_routing-buffer-before-acces.patch
Patch37: 0007-net-eth-Add-an-assert-and-invert-if-statement-to-sim.patch
Patch38: 0001-build-no-pie-is-no-functional-linker-flag.patch
Patch39: 0001-input-Add-lang1-and-lang2-to-QKeyCode.patch
Patch40: 0001-xen-hvm-Allow-disabling-buffer_io_timer.patch
Patch41: 0001-xen-mapcache-Avoid-entry-lock-overflow.patch
Patch42: 0001-block-qdict-Fix-Werror-maybe-uninitialized.patch
Patch43: 0001-pc-bios-optionrom-compile-with-Wno-array-bounds.patch
Patch44: 0001-xen-pass-through-merge-emulated-bits-correctly.patch
Patch45: 0001-xen-pass-through-don-t-create-needless-register-grou.patch
Patch46: 0001-hw-xen-set-pci-Atomic-Ops-requests-for-passthrough-d.patch
Patch47: 0001-hw-xen-xen_pt-fix-uninitialized-variable.patch
Patch48: xen_pt-Emulate-multifunction-bit-in-header-type.patch
Patch49: hw-ide__check_null_block_before__cancel_dma_sync.patch
Patch50: xen-platform-add-device-id-property.patch
Patch51: xen-platform-add-class-id-property.patch
Patch52: xen-platform-add-revision-property.patch
Patch53: 0001-xen-platform-Handle-write-of-four-byte-build-number-.patch
Patch54: 0002-xen-platform-Provide-QMP-query-commands-for-XEN-PV-d.patch
Patch55: 0003-xen-platform-Emit-XEN_PLATFORM_PV_DRIVER_INFO-after-.patch
Patch56: dont-set-a20-on-xen.patch
Patch57: dont-init-cpus-on-xen.patch
Patch58: 0001-xen-Emit-RTC_CHANGE-upon-TIMEOFFSET-ioreq.patch
Patch59: remove-ioapic.patch
Patch60: ignore-rtc-century-changes.patch
Patch61: 0001-CP-33348-Allow-media-replace-qmp-command-to-take-a-n.patch
Patch62: tpm_crb-mark-command-buffer-as-dirty-on-request-comp.patch
Patch63: tpm_emulator-Avoid-double-initialization-during-migr.patch
Patch64: tpm_crb-Avoid-backend-startup-just-before-shutdown-u.patch
Patch65: token-bucket-event-throttling.patch
Patch66: xen-hvm-Avoid-livelock-while-handling-buffered-ioreq.patch
Patch67: 0001-pc-Do-not-expect-to-have-a-fw_cfg-device.patch
Patch68: 0003-xen-apic-Implement-unrealize.patch
Patch69: 0004-hotplug-Implement-legacy-CPU-hot-unplug.patch
Patch70: igd-upt.patch
Patch71: check-unmigratable-devices-when-saving.patch
Patch72: query-migratable.patch
Patch73: 0001-nvme-simplify-namespace-code.patch
Patch74: 0002-nvme-move-device-parameters-to-separate-struct.patch
Patch75: 0003-nvme-fix-lpa-field.patch
Patch76: 0004-nvme-add-missing-fields-in-identify-controller.patch
Patch77: 0005-nvme-populate-the-mandatory-subnqn-and-ver-fields.patch
Patch78: 0006-nvme-support-completion-queue-in-cmb.patch
Patch79: 0007-nvme-support-Abort-command.patch
Patch80: 0008-nvme-refactor-device-realization.patch
Patch81: 0009-nvme-support-Asynchronous-Event-Request-command.patch
Patch82: 0010-nvme-support-Get-Log-Page-command.patch
Patch83: 0011-nvme-add-missing-mandatory-Features.patch
Patch84: 0012-nvme-bump-supported-NVMe-revision-to-1.3d.patch
Patch85: 0013-nvme-simplify-dma-cmb-mappings.patch
Patch86: 0014-nvme-support-multiple-block-requests-per-request.patch
Patch87: 0015-nvme-support-scatter-gather-lists.patch
Patch88: 0016-nvme-support-multiple-namespaces.patch
Patch89: nvme-ns-fix-null.patch
Patch90: nvme-ns-allow-inactive.patch
Patch91: nvme-close-backend.patch
Patch92: 0001-Add-qemu-qcode-support-for-keys-F13-to-F24.patch
Patch93: 0001-ps2-Don-t-send-key-release-event-for-Lang1-Lang2-key.patch
Patch94: 0001-CP-20436-Introduce-a-config-option-for-machines-comp.patch
Patch95: pci-add-subsystem-id-properties.patch
Patch96: pci-add-revision_id-property.patch
Patch97: force-lba-geometry.patch
Patch98: 0001-CP-21767-Don-t-accidently-unplug-ourselves-if-PCI_CL.patch
Patch99: 0001-CP-21434-Implement-VBE-LFB-physical-address-register.patch
Patch100: 0001-CA-256542-Workaround-unassigned-accesses-caused-by-b.patch
Patch101: match-xen-pvdevice-location.patch
Patch102: 0001-CA-289906-Use-legacy-HID-descriptors-for-USB-Tablet-.patch
Patch103: revert_hw-i386__remove_deprecated_machines_pc-0.10_and_pc-0.11.patch
Patch104: 0001-CP-17697-Initial-port-of-NVIDIA-VGPU-support-from-QEMU-trad.patch
Patch105: usb-batch-frames.patch
Patch106: 0001-CP-23753-Talk-to-new-clipboard-daemon.patch
Patch107: gvt-g.patch
Patch108: allocate-guest-ram-reserved.patch
Patch109: unplug-nvme-devices.patch
Patch110: do_not_register_xen_backend_for_qdisk.patch
Patch111: add-an-ide-read-cache.patch
Patch112: disable-dirty-vram-tracking.patch
Patch113: build-configuration.patch
Patch114: 0001-CP-46162-Resolve-the-Null-pointer-error-in-configure.patch
BuildRequires: python3-devel
BuildRequires: libaio-devel glib2-devel
BuildRequires: libjpeg-devel libpng-devel pixman-devel xenserver-libdrm-devel
BuildRequires: xen-dom0-libs-devel xen-libs-devel libusbx-devel
BuildRequires: libseccomp-devel
%if %{with_asan} == 0
BuildRequires: jemalloc-devel
%else
BuildRequires: libasan
%endif
%{?_cov_buildrequires}

# XCP-ng: explicit build dep on gcc
BuildRequires: gcc

%description
This package contains Qemu.

%prep
%autosetup -p1
%{?_cov_prepare}

# submodule ui/keymapcodedb
tar xzf %{SOURCE2}

%build
%if %{with_asan}
extra_configure_argument+=('--enable-sanitizers')
extra_configure_argument+=('--enable-debug')
# Help to get better stack trace
extra_configure_argument+=('--extra-cflags=-fno-omit-frame-pointer')
# avoid: "WARNING: ASan doesn't fully support makecontext/swapcontext functions and may produce false positives in some cases!"
# extra_configure_argument+=('--with-coroutine=sigaltstack')

%else
extra_configure_argument+=('--enable-jemalloc')
%endif

./configure --cc=gcc --cxx=/dev/null --enable-xen --target-list=i386-softmmu \
    --prefix=%{_prefix} --bindir=%{_libdir}/xen/bin --datadir=%{_datarootdir} \
    --localstatedir=%{_localstatedir} --libexecdir=%{_libexecdir} --sysconfdir=%{_sysconfdir} \
    --enable-werror --enable-libusb --enable-trace-backend=log \
    --disable-kvm --disable-docs --disable-guest-agent --disable-sdl \
    --disable-curses --disable-curl --disable-gtk --disable-bzip2 \
    --disable-strip --disable-gnutls --disable-nettle --disable-gcrypt \
    --disable-vhost-net --disable-vhost-scsi --disable-vhost-vsock --disable-vhost-user \
    --disable-lzo --disable-virtfs --disable-tcg --disable-tcg-interpreter \
    --disable-replication --disable-qom-cast-debug --disable-slirp \
    --audio-drv-list= --disable-coroutine-pool --disable-live-block-migration \
    --disable-bochs --disable-cloop --disable-dmg --disable-vvfat --disable-qed \
    --disable-parallels --disable-sheepdog --disable-capstone --disable-fdt \
    --without-default-devices \
    --enable-seccomp "${extra_configure_argument[@]}"

%if %{with_asan}
# Check that address sanitizers is enabled, because QEMU's ./configure will not fail
grep -qe '-fsanitize=address' config-host.mak
%endif

%{?_cov_wrap} %{__make} %{?_smp_mflags} all

%install
mkdir -p %{buildroot}%{_libdir}/xen/bin

rm -rf %{buildroot}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
rm -rf %{buildroot}/usr/include %{buildroot}%{_libdir}/pkgconfig %{buildroot}%{_libdir}/libcacard.*a \
       %{buildroot}/usr/share/locale
rm -rf %{buildroot}/usr/share/icons/
rm -rf %{buildroot}/usr/share/applications/

# QMP scripts
%{__install} -d -m 755 %{buildroot}%{python3_sitelib}/
cp -r python/qemu %{buildroot}%{python3_sitelib}/
cp -r scripts/qmp %{buildroot}%{_datarootdir}/qemu
%{?_cov_install}

%files
%{_libdir}/xen/bin
%{_datarootdir}/qemu
%{_libexecdir}/*
%{python3_sitelib}/qemu

%{?_cov_results_package}

%changelog
* Mon Apr 08 2024 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.2.1-5.2.9
- CA-391031: Reinstate rate limiting of RTC_CHANGE events
- CA-391069: Avoid livelock due to buffered ioreqs

* Mon Feb 12 2024 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.2.1-5.2.8
- Disable capstone and fdt explicitly
- CP-42792: Backport a patch to avoid unncessary buffered ioreq polling

* Wed Jan 31 2024 Andrew Cooper <andrew.cooper3@citrix.com> - 4.2.1-5.2.7
- Rebuild against Xen 4.17

* Fri Jan 19 2024 Fei Su <fei.su@cloud.com> - 4.2.1-5.2.6
- CP-45970 remove qemu_trad_image.py

* Fri Jan 05 2024 Stephen Cheng <stephen.cheng@cloud.com> - 4.2.1-5.2.5
- CP-46162: Backport patches for building qemu with rawhide(xs9) toolchain
  - Do not ignore malloc value
  - Fix the null pointer errors in configure
  - Fix -Werror=maybe-uninitialized build failure
  - Fix net/eth.c compile errors
  - Compile with -Wno-array-bounds
  - Remove -no-pie linker flag

* Tue Nov 21 2023 Bernhard Kaindl <bernhard.kaindl@cloud.com> - 4.2.1-5.2.4
- CP-46102: Backport bugfixes for PCI passthrough using multifunction devices
  - hw/xen: set pci Atomic Ops requests for passthrough device
  - hw/xen/xen_pt: fix uninitialized variable
  - xen/pass-through: don't create needless register group
  - xen/pass-through: merge emulated bits correctly
  - Emulate the multifunction bit and set it based on the multifunction
    property of the PCIDevice (which can be set using QAPI).

* Tue Apr 18 2023 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.2.1-5.2.2
- CA-376325: XSI-1393: Backport: xen-bus: reduce scope of backend watch

* Fri Mar 03 2023 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.2.1-5.2.1
- CA-374355: Fix use of Lang1/Lang2 keys

* Wed Jan 25 2023 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.2.1-5.2.0
- CP-41777: Migrate to Python 3

* Tue Dec 13 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.2.1-5.1.1
- CA-370278: tpm_crb: Avoid backend startup just before shutdown

* Wed Aug 17 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.2.1-5.1.0
- CP-40114: Remove mxGPU patches
- Enable TPM support

* Tue Jun 14 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.2.1-5.0.6
- CA-366527: Fix passthrough of multiple different devices

* Fri Feb 25 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.2.1-5.0.5
- CA-362592: Fix mapcache/iothread SIGBUS

* Thu Feb 10 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.2.1-5.0.4
- CP-38416: Enable static analysis

* Mon May 10 2021 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.2.1-5.0.3
- CA-352456: Backport aio-posix: fix use after leaving scope in aio_poll()
- Fix patch Update-fd-handlers-to-support-sysfs_notify
- CA-352456: Fix QEMU memory corruption during migration

* Tue Apr 13 2021 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.2.1-5.0.2
- CP-36580: Replace legacy xen-dom0-devel alias
- CA-352135: Fix CVE-2021-20257 - e1000 infinite loop
- CA-352998: Fix CVE-2021-3416 - infinite loop in net loopback mode

* Fri Feb 19 2021 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.2.1-5.0.1
- CA-351961: Fix OOB accesses in ATAPI emulation

* Thu Jan 28 2021 Anthony PERARD <anthony.perard@citrix.com> - 4.2.1-5.0.0
- CP-33898: Upgrade QEMU to 4.2.1 upstream release

* Thu Sep 10 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.10.2-4.6.0
- CA-343524: XSA-335: Buffer overrun in QEMU USB subsystem
- CA-343531: CVE-2018-17598: Buffer overflow in rtl8139_do_receive

* Thu Apr 30 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.10.2-4.5.2
- CA-3216958: Move vgpu fifo to tempfs

* Mon Apr 20 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.10.2-4.5.1
- CA-337460 - Allow commit lists to be imported chronologically.
- CP-33051 - Forward port preopened sockets in monitor fdset.
- Fix patch context
- CP-33348 - Allow preopend nbd sockets to be passed to running qemu instance via qmp command.

* Thu Mar 26 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.10.2-4.5.0
- Fix patch context
- CA-336055: nvme: Disassociate block driver state during unplug
- CA-299551: Fix sporadic cpu_physical_memory_snapshot_get_dirty assertion

* Fri Feb 21 2020 Steven Woods <steven.woods@citrix.com> - 2.10.2-4.4.2
- CP33120: Add Coverity build macros

* Thu Nov 07 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.10.2-4.4.1
- CA-330047: Fix QEMU crash with discontiguous NVME namespaces

* Sat Aug 24 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.10.2-4.4.0
- CA-320079: Add NVME namespace support

* Wed Mar 27 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.10.2-4.3.0
- CA-309161: make the import script work with the new planex

* Tue Dec 18 2018 Edwin Török <edvin.torok@citrix.com> - 2.10.2-4.1.4
- CP-29626: Call blk_drain in NVMe reset code to avoid lockups
- CP-29898: Implement NVME migration workaround
- CP-29935: Add a command to allow querying whether the VM is migratable
- CP-29827: Don't conflate RTC_CENTURY bit with trad-compat
- CP-29827: Make legacy CPU unplug work for all machine types
- Fix patch context
- Backport NVMe fixes from upstream, including a CVE
- CA-303616: Expose LFB address when GVT-g is enabled

* Fri Nov 23 2018 Simon Rowe <simon.rowe@citrix.com> - 2.10.2-4.1.3
- CP-29194: Tidy up the patchqueue

* Tue Nov 06 2018 Simon Rowe <simon.rowe@citrix.com> - 2.10.2-4.1.2
- CP-28652: enable nvme for guest uefi

* Fri Oct 12 2018 Simon Rowe <simon.rowe@citrix.com> - 2.10.2-4.1.1
- Revert "CA-290135: Add debug patch to catch the unhandled access"

* Fri Sep 28 2018 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.10.2-4.1.0
- CA-293487: Allocate VRAM in a reserved area
- CA-290135: Add debug patch to catch the unhandled access
- Enable the ISA debug device for OVMF logging

* Thu Aug 16 2018 Igor Druzhinin <igor.druzhinin@citrix.com> - 2.10.2-4.0.4
- CA-290647 50% regression in vm<->vm intrahost network throughput

* Fri Jul 27 2018 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.10.2-4.0.3
- CA-290135: Make the debug message more obvious
- CA-294052: Recreate PCIBUS section properly on upgrade

* Thu Jul 12 2018 Simon Rowe <simon.rowe@citrix.com> - 2.10.2-4.0.2
- CA-290135 Reinforce unhandled unassigned access processing

* Tue Jul 03 2018 Simon Rowe <simon.rowe@citrix.com> - 2.10.2-4.0.1
- CA-293221: Fix upgrade from Clearwater

* Thu Jun 28 2018 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.10.2-4.0.0
- CA-289906: Fix USB Tablet failure on every even migration during live-upgrade

* Mon Jun 25 2018 Simon Rowe <simon.rowe@citrix.com> - 2.10.2-3.0.8
- CA-286948: Fix resume when PV device location changes

* Wed May 30 2018 Simon Rowe <simon.rowe@citrix.com> - 2.10.2-3.0.7
- Print error code on foreign map failure

* Tue May 15 2018 Simon Rowe <simon.rowe@citrix.com> - 2.10.2-3.0.6
- CA-288638: Correct reporting of modified VRAM during migration
- CP-27696: Accomodate customised xen-pvdevice and NIC device ids into live-upgrade script
- CA-289321: Fix PCI passthrough edge cases
- CP-27572: vGPU should use shmem instead of xenstore+buffer hackery.

* Tue May 15 2018 Simon Rowe <simon.rowe@citrix.com> - 2.10.2-3.0.5
- CA-288638: Correct reporting of modified VRAM during migration
- CP-27696: Accomodate customised xen-pvdevice and NIC device ids into live-upgrade script
- CA-289321: Fix PCI passthrough edge cases
- CP-27572: vGPU should use shmem instead of xenstore+buffer hackery.

* Fri Apr 20 2018 Simon Rowe <simon.rowe@citrix.com> - 2.10.2-3.0.4
- CA-288286: Avoid built-in QEMU crypto

* Wed Apr 18 2018 marksy <mark.syms@citrix.com> - 2.10.2-3.0.3
- IDE read cache

* Mon Apr 16 2018 Simon Rowe <simon.rowe@citrix.com> - 2.10.2-3.0.2
- Return swallowed error messages
- CA-285493: Fix unmap issues with NVIDIA GPU passthrough

* Wed Mar 28 2018 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.10.2-3.0.0
- Adjust dmops patch after backporting final version
- CA-266841: Improve VNC performance over long, thin pipes
- migration: Check return value of qemu_fclose
- CP-25629: Don't record QEMU's state in xenstore
- CA-267326: Backport VGA fixes including CVE-2018-5683
- CP-26998: Reintroduce QEMU vCPU hot-(un)plug patches
- CA-283664: Fix using QEMU upstream with libxl
- CP-23325: GVT-g: Save errno earlier
- CP-23325: Fix error handling issues in AMD GPU patch
- CP-23325: GVT-g: Check for allocation failure
- CP-23325: vgpu: Log sendto errors
- CP-24243: GVT-d: Use UPT instead of legacy mode
- CA-284366: Fix use of MSI-X with passthrough devices
- CP-23969 Introduce xen-pvdevice save state and upgrade into it
- CA-267326: Fix cirrus crash found by fuzzing
- CA-285409: Fix Windows RTC issues
- Enable e1000 device model for debug purposes
- CP-27303: Change QEMU vGPU communication with DEMU to fifo
- CA-285385: Backport qemu-trad vgpu-migrate patch, to allow vgpu migration
- CA-285493: Turn on PCI passthrough permissive mode

* Thu Aug 31 2017 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.10.0-1
- Update to QEMU v2.10.0.

* Tue Jun 16 2015 Ross Lagerwall <ross.lagerwall@citrix.com>
- Update for Xen 4.5.

* Tue Apr 8 2014 Frediano Ziglio <frediano.ziglio@citrix.com>
- First packaging
