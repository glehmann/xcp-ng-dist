---
name: installer-vm
description: Boot and control the XCP-ng installer in a disposable QEMU VM, navigate its serial UI, inspect diagnostic consoles, retrieve installation logs, and boot the installed host. Use when testing host-installer or installation ISO changes, resuming an installer VM session, or diagnosing installation failures such as package-install errors.
---

# Installer VM

Read [the runbook](references/runbook.md) before controlling a VM. It records tested setup, command examples,
known limitations, and a dated session handoff. Check whether the referenced temporary helper and artifacts still
exist before using them.

## Workflow

1. Inspect the existing VM and its artifacts before starting another instance. Reuse its control endpoints when
   resuming a session; the prototype launcher replaces socket paths.
2. For a new VM, use a disposable qcow2 disk and UEFI firmware with a writable, per-VM variables file. Attach serial
   capture before boot. Record the launch configuration and artifact paths so another session can attach.
3. Render serial output with `pyte`. Wait for expected screen contents and output stability with a timeout before
   sending input. Use QMP screenshots when serial output does not explain the current state.
4. Use `xcraft vm` for status, rendered console, serial input, keyboard events, screenshots, and diagnostics. Send
   installer UI input through serial. Use QMP physical keyboard events for virtual-terminal switching and
   commands in the diagnostic shell. Serial input may not reach that shell.
5. On failure, collect `/tmp/install-log`, relevant journal and package-manager logs, the serial transcript, a rendered
   screen, and a screenshot before rebooting. Use `xcraft vm logs` for host-side diagnostics. Retrieve guest files with
   [scripts/get-log.py](scripts/get-log.py), using SSH if configured or its checksum-verified serial transfer from the
   open diagnostic shell. See the runbook for commands and prerequisites.
6. After successful installation, stop the VM and boot the same disk without the ISO, retaining its UEFI variables.
   Verify the installed host actually boots before reporting installation success.

Report the observed installer state, collected artifact paths, any concrete failure cause, and the next unresolved
step. Keep new session-specific details in the dated handoff section of the reference rather than treating temporary
paths or unverified workarounds as permanent setup requirements.
