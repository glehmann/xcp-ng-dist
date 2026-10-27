# Testing the installer in a VM

## Choose the test mode

Use an answerfile by default for installation, package, filesystem, configuration, and snapshot/rollback tests.
It makes runs repeatable and avoids spending time navigating unrelated dialogs. Drive the installer UI through
`pyte` only when testing actual user interaction, dialog behavior, or message display. Console rendering and
screenshots remain useful for diagnosing either kind of test.

Run the commands below from the distribution repository. They use the adjacent development xcraft checkout.

## VM setup

Inspect an existing session before starting another instance. Keep the disk, UEFI variables, control sockets, and
logs together under `.xcraft/`. Use disk-backed storage for large artifacts; `/tmp` may be tmpfs.

```sh
uv run --project ../xcraft xcraft boot --background --memory 4096 \
    --iso .xcraft/iso/xcp-ng-8.99.0.iso
uv run --project ../xcraft xcraft vm status
```

The tested configuration is x86 with KVM, four CPUs, 4 GiB RAM, an 80 GiB disposable disk, and UEFI with OVMF.
Sessions default to `.xcraft/vm/<arch>/`. For a separate session, pass `--vm-dir .xcraft/my-vm` to `boot` and before
each `vm` subcommand. Keep that directory when booting the installed disk so its disk and writable UEFI VARS persist.
User networking forwards guest SSH to localhost port 2222 by default, but the guest must configure its interface
and start sshd before that forwarding is useful.

## Answerfile-driven installation

Adapt this example to the test's disk and network interface:

```xml
<installation mode="fresh">
  <primary-disk guest-storage="false" fs-type="btrfs">sda</primary-disk>
  <source type="local" />
  <admin-interface name="eth0" proto="dhcp" />
  <root-password type="plaintext">test-password</root-password>
  <hostname>installer-test</hostname>
  <timezone>Etc/GMT</timezone>
  <ntp source="default" />
  <keymap>us</keymap>
</installation>
```

For PXE, supply the answerfile URL through the `rt_answerfile=URL` boot argument and use the appropriate repository
source. For an ISO VM, an answerfile can also be placed in the guest and run from its diagnostic shell:

```sh
systemctl stop installer
cd /opt/xensource/installer
./init --rt_answerfile=file:///tmp/answer.xml --console=hvc0 > /tmp/installer-console.log 2>&1
```

Use default NTP for ordinary tests; `source="none"` has triggered a separate time-setup error. Redirect verbose
output to a guest file rather than streaming RPM debug logs over serial. Check `/tmp/install-log` for
`The installation completed successfully.`; the process exit status alone is insufficient.

## UI testing and diagnostic consoles

```sh
uv run --project ../xcraft xcraft vm console --wait 'Select Keymap' --timeout 90
uv run --project ../xcraft xcraft vm text --escape '\t\r'
uv run --project ../xcraft xcraft vm key ctrl alt f2
uv run --project ../xcraft xcraft vm screenshot /tmp/diagnostic-shell.png
uv run --project ../xcraft xcraft vm text --physical --enter 'tail -60 /tmp/install-log'
```

`console` uses `pyte` to render the serial transcript and waits for stable expected text. Use timeouts; on timeout,
xcraft saves diagnostics in the session. Raw ANSI output can make stale screen contents look current.

Use serial input for the installer UI. Ctrl-Alt-F2 opens the installer diagnostic shell; type commands there with
`--physical`, since serial input may still target the installer UI. Use screenshots to check keyboard focus.
For installed-host access, prefer SSH or its serial login. A graphical login was available on Ctrl-Alt-F3.

## Logs and failure diagnosis

Collect `/tmp/install-log`, relevant journal/package-manager output, and host-side diagnostics before rebooting:

```sh
uv run --project ../xcraft xcraft vm logs .xcraft/installer-diagnostics
uv run --project ../xcraft python .agents/skills/installer-vm/scripts/get-log.py \
    --vm-dir .xcraft/vm/x86_64_v2 --ssh --identity /path/to/key \
    --output .xcraft/installer-diagnostics/install-log.txt
```

The helper reads the forwarded SSH port from `session.json`. For password authentication, use
`--password-env VARIABLE_NAME` instead of `--identity`; this requires sshpass. Without SSH, open the diagnostic
shell and omit `--ssh` and `--identity`. The fallback physically types a numbered base64 transfer through
`/dev/hvc0` and verifies size and SHA-256. It needs guest Python, a US keyboard layout, and an open shell prompt.
The installed host needs Xen serial output enabled for this fallback; otherwise use SSH.

Use `--guest-path` for another guest file. Compress large logs in the guest first, then retrieve the gzip file.
A Xen UART diagnostic can interrupt serial transfer; retry if verification fails. The helper does not overwrite
existing output files. Keep logs local and review them for credentials before sharing.

For GPG failures, check that the ISO's key bundle includes the keys for retained upstream RPM signatures.
Distinguish filesystem/install failures from unrelated installed-host service or management-network failures.

## Installed boot and snapshot checks

After a successful install, stop the VM and boot its disk without the ISO:

```sh
uv run --project ../xcraft xcraft vm stop
uv run --project ../xcraft xcraft boot --installed --background --memory 4096
```

Verify login and the actual mounted filesystems before reporting success. For rollback tests, add
`<system-snapshot name="installed" />` to the answerfile to create a root-and-EFI baseline before first boot.
The existing `xcp-ng-config` package owns the private helpers and their instructions at `/usr/libexec/xcp-ng/README`.
Use `/usr/libexec/xcp-ng/system-snapshot` for a post-boot baseline and `/usr/libexec/xcp-ng/system-restore` to restore
and reboot. Confirm system and EFI changes disappear, `/var/log` changes survive, and the baseline remains reusable.
A pre-first-boot baseline reruns pending initialization and excludes any test access configuration added later.

OVMF's persistent BootOrder can override QEMU's ISO boot order on later rescue boots. Select the DVD in the firmware
menu or set its BootNext entry; do not assume that entry's number survives removal of the ISO. If broken installed
GRUB configuration leaves a prompt, an attached ISO can be booted with:

```text
set root=(cd0)
set prefix=(cd0)/EFI/BOOT
configfile /EFI/BOOT/grub.cfg
```

Report the test input, observed result, and artifact location. Keep session history with the local artifacts rather
than appending it to this runbook.
