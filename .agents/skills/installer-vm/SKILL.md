---
name: installer-vm
description: Test the XCP-ng installer in a disposable QEMU VM using answerfiles by default, drive its serial UI for interaction and display tests, retrieve diagnostic logs, and verify installed-host boot. Use when testing host-installer or installation ISO changes, resuming an installer VM session, or diagnosing installation failures.
---

# Installer VM

Read [the runbook](references/runbook.md) before controlling a VM for setup, answerfile execution, UI controls,
log retrieval, and installed-host checks.

Use answerfiles by default for functional installation tests. Reserve `pyte`-driven UI input for testing actual
user interaction, dialog behavior, or message display. Console rendering and screenshots can diagnose either mode.

## Workflow

1. Inspect the existing VM and its artifacts before starting another instance. Reuse its control endpoints when
   resuming a session.
2. For a new VM, use a disposable qcow2 disk and UEFI firmware with a writable, per-VM variables file. Attach serial
   capture before boot. Record the launch configuration and artifact paths so another session can attach.
3. Run the test with an answerfile unless UI behavior is the subject. For UI tests, render serial output with `pyte`
   and wait for stable expected screen contents with a timeout before sending input.
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
step. Keep session-specific details with local test artifacts; keep the runbook focused on reusable instructions.
