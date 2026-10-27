# Working with the installer in a VM

This is the detailed reference for the [installer-vm skill](../SKILL.md).

Use a disposable QEMU VM to test installer changes, inspect failures, and boot the installed host.
Keep its disk, firmware variables, control sockets, and logs together so another agent can resume the session.

## VM setup

The development version of `xcraft boot` in the adjacent `xcraft` checkout launches persistent UEFI sessions, and
`xcraft vm` controls them. The version pinned by this repository may not include these commands yet. Run the
development checkout from this repository with `uv run --project ../xcraft xcraft ...` when necessary.

```sh
uv run --project ../xcraft xcraft boot --background --iso .xcraft/iso/xcp-ng-8.99.0.iso
uv run --project ../xcraft xcraft vm status
uv run --project ../xcraft xcraft vm console --wait 'Select Keymap' --timeout 90
```

Sessions default to `.xcraft/vm/<arch>/`. Use `boot --vm-dir /tmp/my-vm` for a separate session, then put
`--vm-dir /tmp/my-vm` before each `vm` subcommand. Keep the same session directory for `boot --installed` so the
disk and UEFI variables are reused. `--disk` alone changes only the disk path.

The tested configuration uses:

- x86 QEMU with KVM, 8 GiB RAM, and four CPUs.
- A disposable 80 GiB qcow2 disk.
- UEFI with OVMF. The installer rejected the BIOS boot attempt.
- A read-only OVMF CODE image and a writable, per-VM copy of OVMF VARS.
- User networking with guest SSH port 22 forwarded to localhost port 2222 by default. The older prototype used 2223.
- A QMP Unix socket for screenshots, keyboard events, and lifecycle control.
- Serial input and a raw serial transcript captured from startup.

On this host the firmware templates are `/usr/share/edk2/ovmf/OVMF_CODE.fd` and
`/usr/share/edk2/ovmf/OVMF_VARS.fd`. Preserve the VM's writable VARS copy when booting its installed disk.

## Inspecting and controlling the installer

```sh
uv run --project ../xcraft xcraft vm text --escape '\t\r'
uv run --project ../xcraft xcraft vm text --escape '\x1b[B'
uv run --project ../xcraft xcraft vm key ctrl alt f2
uv run --project ../xcraft xcraft vm screenshot /tmp/diagnostic-shell.png
uv run --project ../xcraft xcraft vm text --physical --enter 'tail -60 /tmp/install-log'
```

Render the serial transcript with `pyte` to obtain the current 80-by-24 screen. Reading raw ANSI output as plain text
can make old screen contents look current. Wait for expected screen text and a brief period without output before
sending the next input. Always use a timeout and capture the screen on failure.

`xcraft vm console` handles rendering and stable-text waits. On timeout it automatically saves host-side diagnostics
in the session directory. Raw serial output is captured from boot to `serial.log` even between agent sessions;
`serial.in` is the persistent input FIFO. `qemu.log` records QEMU diagnostics separately.

Serial input works for the installer UI. QMP physical keyboard events also work and can switch to a diagnostic
virtual terminal with Ctrl-Alt-F2. Commands typed there need physical keyboard input; writing to the serial input
does not necessarily reach that shell. QMP screenshots help identify which console currently has focus.

The upstream [serial automation PR](https://github.com/xcp-ng/xcp-ng-tests/pull/725) is a useful reference for attaching
before boot, rendering the console, editing boot arguments, and retrieving diagnostics over SSH.

## Retrieving logs

Start with `/tmp/install-log` inside the installer. Also collect relevant journal and package-manager logs, the raw
serial transcript, a rendered screen, a screenshot, and the VM launch configuration.

Prefer SSH when available. Port forwarding alone does not enable the installer SSH server. Verify this installer's
supported boot arguments and configure development access explicitly. The upstream PR uses arguments such as
`sshpassword`, `network_device`, and `atexit`; their behavior still needs checking with this installer version.

Collect the host-side bundle into a new directory:

```sh
uv run --project ../xcraft xcraft vm logs /tmp/installer-diagnostics
```

For a guest file, use the bundled helper. It needs the development xcraft package. With SSH configured, it reads the
forwarded port from `session.json` and saves the file directly:

```sh
uv run --project ../xcraft python .agents/skills/installer-vm/scripts/get-log.py \
    --vm-dir .xcraft/vm/x86_64_v2 --ssh --identity /path/to/key \
    --output /tmp/installer-diagnostics/install-log.txt
```

For password authentication, supply `--password-env VARIABLE_NAME` instead of `--identity`; this requires `sshpass`
and the named environment variable. The password is not placed in command arguments. SSH host keys are retained in
the session's `known_hosts` file. Failed SSH transfers can leave a partial destination file; inspect/remove it before
retrying with the same output path.

Without SSH, switch to the diagnostic terminal with Ctrl-Alt-F2 and verify the root shell prompt in a screenshot.
Then run the helper without `--ssh`:

```sh
uv run --project ../xcraft python .agents/skills/installer-vm/scripts/get-log.py \
    --vm-dir .xcraft/vm/x86_64_v2 --output /tmp/installer-diagnostics/install-log.txt
```

The helper physically types a Python command into that shell, exports numbered base64 chunks through `/dev/hvc0`,
and verifies file size and SHA-256 before writing the result. Guest Python 3, a US keyboard layout, and an open shell
prompt are required. Use `--guest-path` for another file, `--device` for another guest serial device, or `--transcript`
for a nonstandard raw serial log. The helper fails rather than overwriting an existing output file. A damaged or
incomplete transfer fails verification; inspect the screenshot and retry. This method was verified against the real
installer's `/tmp/install-log` and a 256 KiB binary file.

To collect the journal, first type `journalctl --no-pager > /tmp/installer-journal.txt` into the shell, then retrieve
that path with `--guest-path /tmp/installer-journal.txt` and a separate local output file.

For large logs, compress in the guest first, for example `gzip -c /tmp/install-log > /tmp/install-log.gz`, and retrieve
the compressed file. RPM debug logging can produce more than 10 MiB of text during installation. The transfer parser
accepts repeated carriage returns before a newline, which can occur after running the installer on the diagnostic
terminal.

The `/dev/hvc0` transfer assumes Xen's console is connected to QEMU serial. It worked in the installer, but not in
the installed host with its default boot arguments. For installed-host files, configure SSH or enable Xen's serial
console before using this fallback. The tested installed host has its login terminal on Ctrl-Alt-F3; Ctrl-Alt-F2 shows
system messages.

Logs can contain installation credentials. Keep diagnostic artifacts local and review them before sharing.

## Original session handoff, 2026-10-27

The temporary controller is `/tmp/opencode/control-installer.py`. It contains machine-specific paths and is not yet
a repository tool. Its artifacts are in `/tmp/opencode/installer-agent/`:

| File | Purpose |
| --- | --- |
| `disk.qcow2` | Disposable installation target |
| `OVMF_VARS.fd` | Persistent UEFI variables |
| `qmp.sock`, `input`, `pid` | Control socket, serial input FIFO, and launcher PID |
| `installer.log` | Raw installer serial transcript, including the attempted log export |
| `installed.log` | Serial transcript when booting the installed disk |
| `diagnostic-shell.png` | Screenshot taken after switching to the diagnostic terminal |

Check the existing VM before launching another one. The helper's start operation replaces socket paths.

```sh
python /tmp/opencode/control-installer.py status
python /tmp/opencode/control-installer.py screen current
uv run --no-project --with pyte --cache-dir /tmp/opencode/uv-cache \
    python /tmp/opencode/control-installer.py console
```

Examples of control operations:

```sh
# Serial input: Tab followed by Enter, or the down arrow.
python /tmp/opencode/control-installer.py text '\t\r'
python /tmp/opencode/control-installer.py text '\x1b[B'

# Physical keyboard input: switch terminal, then type a command and press Enter.
python /tmp/opencode/control-installer.py key ctrl alt f2
python /tmp/opencode/control-installer.py physical 'tail -60 /tmp/install-log'
python /tmp/opencode/control-installer.py screen diagnostic

# Wait up to 60 seconds for specific serial screen text.
uv run --no-project --with pyte --cache-dir /tmp/opencode/uv-cache \
    python /tmp/opencode/control-installer.py console 'Error occurred' 60
```

The `physical` operation supports only the characters mapped by the prototype and always presses Enter afterward.
The `console` operation currently reads `installer.log` even after an installed-disk boot.

To stop the VM, use `python /tmp/opencode/control-installer.py quit`. Once it has stopped, `start` boots the ISO and
`installed` boots the same disk without the ISO. Neither operation resets the disk or firmware variables.

The ISO under test is `.xcraft/iso/xcp-ng-8.99.0.iso`. Installation used US keymap, local ISO packages, DHCP,
hostname `xcraft-installer-test`, Etc/GMT, default NTP servers, and no guest VM storage repository.

Installation reached package installation and failed with **Error installing packages**. The cause was unknown then;
see the signature investigation below for the diagnosis and verified fix.
The diagnostic shell accepted physical keyboard input, but SSH timed out during banner exchange. The next step is
to retrieve `/tmp/install-log` reliably and identify the package-install failure. Installed-host boot has not been
verified.

## Control-tool verification, 2026-10-27

A fresh smoke-test VM booted the existing ISO through the new xcraft controls, reached keymap selection, and opened
the diagnostic root shell. The helper retrieved its installer log and verified a 262144-byte binary transfer. Its
artifacts are in `/tmp/opencode/installer-control-test/`, including the host diagnostics bundle. The smoke-test VM was
stopped afterward. The earlier `/tmp/opencode/installer-agent/` QMP socket was stale when checked; that VM was no
longer running.

## Signature failure investigation, 2026-10-27

The original log was recovered to `/tmp/opencode/installer-agent/recovered-install-log.txt`. Its base64 export was
interrupted by a Xen UART diagnostic, which explained the original decoding failure. Removing that diagnostic made
the log readable. DNF rejected the upstream RPMs with `Public key ... is not installed` and `Error: GPG check FAILED`.

The ISO exported only its local signing key, but retained the upstream RPM signatures. This build uses the AlmaLinux
OS 10 key and the AlmaLinux EPEL 10 AltArch key as well. The installer's `repository.py` reads only the first key file
listed in `.treeinfo`, so listing additional key files would not fix this version.

The xcraft fix exports trusted upstream public keys from the build image's RPM database during ISO creation, then
bundles them with the local signing key in `RPM-GPG-KEY-xcpng`. The tested ISO is
`/tmp/opencode/xcp-ng-8.99.0-keys.iso`. Signature verification remained enabled. DNF imported all three keys, both
package transactions completed, and the installer logged `The installation completed successfully.`

The disposable session is `/tmp/opencode/installer-keys-test/`. Useful artifacts include:

- `success-diagnostics/`: raw installer console, rendered screen, and launch details captured after installation.
- `install-log.gz`: the complete guest installer log, retrieved with checksum verification.
- `disk.qcow2` and `OVMF_VARS.fd`: the installed disk and its UEFI state.
- `installed-boot-4g.png`: service failures observed during installed-host startup.
- `installed-tty3.png` and `installed-shell.png`: the installed host's login prompt and successful root login.

The first installed-disk boot at 8 GiB was killed by the host OOM killer, confirmed in the host kernel journal.
Booting with `--memory 4096` reached the XCP-ng host and root shell. Several services failed and no management IP was
configured; installed-host health still needs investigation. A boot journal was saved inside that guest as
`/tmp/boot-journal.gz` and failed-unit output as `/tmp/failed-units.txt`, but the default installed-host console did not
forward their export to serial. The session is stopped; resume with:

```sh
uv run --project ../xcraft xcraft boot --installed --background --memory 4096 \
    --vm-dir /tmp/opencode/installer-keys-test --ssh-port 2223
```

The unattended verification used a local answerfile with `sda`, no guest storage, `eth0` DHCP, hostname
`xcraft-installer-test`, Etc/GMT, and default NTP. Running with `<ntp source="none" />` failed earlier in time setup
with a `datetime`/`NoneType` subtraction error; using default NTP avoided that separate answerfile issue. The
temporary orchestration script is `/tmp/opencode/run-installer-answerfile.py`; its initial XML still contains the
failing NTP selection and needs changing to `default` before reuse.
