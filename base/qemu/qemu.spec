Summary: qemu-dm device model
Name: qemu
Epoch: 2
Version: 2.10.2
Release: 4.2.0
License: GPL
Requires: jemalloc
Requires: xs-clipboardd
Requires: xengt-userspace

Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/qemu/archive?at=v2.10.2&format=tar.gz&prefix=qemu-2.10.2#/qemu-2.10.2.tar.gz
Source1: SOURCES/qemu/qemu_trad_image.py

Patch0: 0001-seccomp-changing-from-whitelist-to-blacklist.patch
Patch1: 0002-seccomp-add-obsolete-argument-to-command-line.patch
Patch2: 0003-seccomp-add-elevateprivileges-argument-to-command-li.patch
Patch3: 0004-seccomp-add-spawn-argument-to-command-line.patch
Patch4: 0005-seccomp-add-resourcecontrol-argument-to-command-line.patch
Patch5: 0006-buildsys-Move-seccomp-cflags-libs-to-per-object.patch
Patch6: 0001-vnc-use-QEMU_ALIGN_DOWN.patch
Patch7: 0002-vnc-use-DIV_ROUND_UP.patch
Patch8: 0004-ui-add-tracing-of-VNC-operations-related-to-QIOChann.patch
Patch9: 0005-ui-add-tracing-of-VNC-authentication-process.patch
Patch10: 0006-ui-Always-remove-an-old-VNC-channel-watch-before-add.patch
Patch11: 0004-vga-migration-Update-memory-map-in-post_load.patch
Patch12: 0007-vga-add-ram_addr_t-cast.patch
Patch13: 0008-cirrus-fix-oob-access-in-mode4and5-write-functions.patch
Patch14: 0009-vga-fix-region-checks-in-wraparound-case.patch
Patch15: 0001-xen-pt-allow-QEMU-to-request-MSI-unmasking-at-bind-t.patch
Patch16: 0007-vnc-fix-debug-spelling.patch
Patch17: 0008-ui-remove-sync-parameter-from-vnc_update_client.patch
Patch18: 0009-ui-remove-unreachable-code-in-vnc_update_client.patch
Patch19: 0010-ui-remove-redundant-indentation-in-vnc_client_update.patch
Patch20: 0011-ui-avoid-pointless-VNC-updates-if-framebuffer-isn-t-.patch
Patch21: 0012-ui-track-how-much-decoded-data-we-consumed-when-doin.patch
Patch22: 0013-ui-introduce-enum-to-track-VNC-client-framebuffer-up.patch
Patch23: 0014-ui-correctly-reset-framebuffer-update-state-after-pr.patch
Patch24: 0015-ui-refactor-code-for-determining-if-an-update-should.patch
Patch25: 0016-ui-fix-VNC-client-throttling-when-audio-capture-is-a.patch
Patch26: 0017-ui-fix-VNC-client-throttling-when-forced-update-is-r.patch
Patch27: 0018-ui-place-a-hard-cap-on-VNC-server-output-buffer-size.patch
Patch28: 0019-ui-add-trace-events-related-to-VNC-client-throttling.patch
Patch29: 0020-ui-mix-misleading-comments-return-types-of-VNC-I-O-h.patch
Patch30: 0021-ui-avoid-sign-extension-using-client-width-height.patch
Patch31: 0010-vga-check-the-validation-of-memory-addr-when-draw-te.patch
Patch32: 0001-vga-fix-region-calculation.patch
Patch33: 0001-migration-Don-t-leak-IO-channels.patch
Patch34: 0001-io-Fix-QIOChannelFile-when-creating-and-opening-read.patch
Patch35: 0001-io-Don-t-call-close-multiple-times-in-QIOChannelFile.patch
Patch36: 0001-io-Add-dev-fdset-support-to-QIOChannelFile.patch
Patch37: 0001-migration-xen-Check-return-value-of-qemu_fclose.patch
Patch38: 0001-xen-pvdevice-Introduce-a-simplistic-xen-pvdevice-sav.patch
Patch39: 0001-xen-hvm-correct-reporting-of-modified-memory-under-p.patch
Patch40: 0001-xen_pt-Present-the-size-of-64-bit-BARs-correctly.patch
Patch41: 0001-xen-pt-use-address_space_memory-object-for-memory-re.patch
Patch42: 0001-xen-Use-newly-added-dmops-for-mapping-VGA-memory.patch
Patch43: 0001-xen-hvm-create-separate-function-for-ioreq-server-in.patch
Patch44: 0001-xen-hvm-try-to-use-xenforeignmemory_map_resource-to-.patch
Patch45: 0003-nvme-don-t-unref-ctrl_mem-when-device-unrealized.patch
Patch46: 0004-nvme-free-cmbuf-in-nvme_exit.patch
Patch47: 0005-nvme-fix-oob-access-issue-CVE-2018-16847.patch
Patch48: 0001-nvme-call-blk_drain-in-NVMe-reset-code-to-avoid-lock.patch
Patch49: xen-platform-add-device-id-property.patch
Patch50: xen-platform-add-class-id-property.patch
Patch51: xen-platform-add-revision-property.patch
Patch52: 0001-xen-platform-Handle-write-of-four-byte-build-number-.patch
Patch53: 0002-xen-platform-Provide-QMP-query-commands-for-XEN-PV-d.patch
Patch54: 0003-xen-platform-Emit-XEN_PLATFORM_PV_DRIVER_INFO-after-.patch
Patch55: dont-set-a20-on-xen.patch
Patch56: dont-init-cpus-on-xen.patch
Patch57: 0001-xen-Emit-RTC_CHANGE-upon-TIMEOFFSET-ioreq.patch
Patch58: remove-ioapic.patch
Patch59: ignore-rtc-century-changes.patch
Patch60: 0001-pc-Do-not-expect-to-have-a-fw_cfg-device.patch
Patch61: 0003-xen-apic-Implement-unrealize.patch
Patch62: 0004-hotplug-Implement-legacy-CPU-hot-unplug.patch
Patch63: 0001-xen-link-against-xentoolcore.patch
Patch64: 0002-xen-restrict-use-xentoolcore_restrict_all.patch
Patch65: 0003-xen-defer-call-to-xen_restrict-until-just-before-os_setup_post.patch
Patch66: 0004-xen-destroy_hvm_domain-Move-reason-into-a-variable.patch
Patch67: 0005-xen-move-xc_interface-compatibility-fallback-further-up-the-file.patch
Patch68: 0006-xen-destroy_hvm_domain-Try-xendevicemodel_shutdown.patch
Patch69: 0007-os-posix-Provide-new--runas-uid-.-gid-facility.patch
Patch70: xenstore-ignore-state-write-error.patch
Patch71: igd-upt.patch
Patch72: pt-avoid-invalid-bar-registers.patch
Patch73: check-unmigratable-devices-when-saving.patch
Patch74: query-migratable.patch
Patch75: 0001-CP-20436-Introduce-a-config-option-for-machines-comp.patch
Patch76: pci-add-subsystem-id-properties.patch
Patch77: pci-add-revision_id-property.patch
Patch78: force-lba-geometry.patch
Patch79: 0001-CP-21767-Don-t-accidently-unplug-ourselves-if-PCI_CL.patch
Patch80: 0001-CP-21434-Implement-VBE-LFB-physical-address-register.patch
Patch81: 0001-CA-256542-Workaround-unassigned-accesses-caused-by-b.patch
Patch82: match-xen-pvdevice-location.patch
Patch83: 0001-CA-289906-Use-legacy-HID-descriptors-for-USB-Tablet-.patch
Patch84: 0001-CP-17697-Initial-port-of-NVIDIA-VGPU-support-from-QEMU-trad.patch
Patch85: usb-batch-frames.patch
Patch86: 0001-CP-23753-Talk-to-new-clipboard-daemon.patch
Patch87: rtc-no-ratelimit.patch
Patch88: gvt-g.patch
Patch89: 0001-Update-fd-handlers-to-support-sysfs_notify.patch
Patch90: 0002-Fix-up-PCI-command-register-for-AMD-ATI-GPU-VFs.patch
Patch91: 0003-Add-interception-layer-for-BAR-ops.patch
Patch92: 0004-Add-AMD-code.patch
Patch93: allocate-vram-reserved.patch
Patch94: 0001-CA-239469-Avoid-bind-listen-race-on-a-socket-with-SO.patch
Patch95: set-so_reuseaddr.patch
Patch96: unplug-nvme-devices.patch
Patch97: do_not_register_xen_backend_for_qdisk.patch
Patch98: add-an-ide-read-cache.patch
Patch99: disable-dirty-vram-tracking.patch
Patch100: build-configuration.patch

Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/qemu/archive?at=v2.10.2&format=tar.gz&prefix=qemu-2.10.2#/qemu-2.10.2.tar.gz) = ba87166e14ffd7299c35badc4c11f3fa3c129ec6
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/qemu.pg/archive?format=tar&at=v4.2.0#/qemu.pg.tar) = c743aade3b240447d6cf313afce23e4e20d65120

BuildRequires: libaio-devel glib2-devel
BuildRequires: libjpeg-devel libpng-devel pixman-devel xenserver-libdrm-devel
BuildRequires: xen-dom0-devel xen-libs-devel libusbx-devel
BuildRequires: libseccomp-devel

%description
This package contains Qemu.

%prep
%autosetup -p1

%build
./configure --cc=gcc --cxx=/dev/null --enable-xen --target-list=i386-softmmu --source-path=. \
    --prefix=%{_prefix} --bindir=%{_libdir}/xen/bin --datadir=%{_datarootdir} \
    --localstatedir=%{_localstatedir} --libexecdir=%{_libexecdir} --sysconfdir=%{_sysconfdir} \
    --enable-werror --enable-libusb --enable-trace-backend=log \
    --disable-kvm --disable-docs --disable-guest-agent --disable-sdl \
    --disable-curses --disable-curl --disable-gtk --disable-bzip2 \
    --disable-strip --disable-gnutls --disable-nettle --disable-gcrypt \
    --disable-vhost-net --disable-vhost-scsi --disable-vhost-vsock --disable-vhost-user \
    --disable-lzo --disable-tpm --disable-virtfs --disable-tcg --disable-tcg-interpreter \
    --disable-replication --disable-qom-cast-debug --disable-slirp \
    --audio-drv-list= --disable-coroutine-pool --disable-live-block-migration \
    --enable-seccomp
%{?cov_wrap} %{__make} %{?_smp_mflags} all

%install
mkdir -p %{buildroot}%{_libdir}/xen/bin

rm -rf %{buildroot}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
rm -rf %{buildroot}/usr/include %{buildroot}%{_libdir}/pkgconfig %{buildroot}%{_libdir}/libcacard.*a \
       %{buildroot}/usr/share/locale
%{__install} -D -m 644 %{SOURCE1} %{buildroot}%{_libdir}/xen/bin/qemu_trad_image.py
cp -r scripts/qmp %{buildroot}%{_datarootdir}/qemu

%files
%{_libdir}/xen/bin
%{_datarootdir}/qemu
%{_libexecdir}/*

%changelog
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

