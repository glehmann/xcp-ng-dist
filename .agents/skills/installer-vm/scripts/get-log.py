"""Retrieve an installer file through its diagnostic shell or SSH."""

# ruff: noqa: INP001, T201

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import re
import shlex
import shutil
import subprocess
import time
import uuid
from pathlib import Path

from pydantic import BaseModel, Field

from xcraft.vm import Monitor, Session, type_text


class Header(BaseModel):
    """The expected size and checksum announced by the guest."""

    size: int = Field(ge=0)
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


def serial(  # noqa: PLR0913
    directory: Path, transcript: Path, output: Path, *, guest_path: str, device: str, timeout: float
) -> None:
    """Type a framed transfer command into an already-open diagnostic shell."""
    prefix = "XCRAFT_" + uuid.uuid4().hex
    code = (
        "import base64,hashlib;from pathlib import Path;"
        f"d=Path({guest_path!r}).read_bytes();"
        f"print('{prefix}:BEGIN:'+str(len(d))+':'+hashlib.sha256(d).hexdigest());"
        f"[print('{prefix}:'+str(i)+':'+base64.b64encode(d[i:i+768]).decode()) for i in range(0,len(d),768)];"
        f"print('{prefix}:END')"
    )
    command = f"python3 -c {shlex.quote(code)} > {shlex.quote(device)}"
    pattern = re.compile(re.escape(prefix.encode()) + rb":([^\r\n]*)\r*\n")
    chunks: dict[int, bytes] = {}
    header = None
    pending = b""
    with transcript.open("rb") as log:
        log.seek(0, os.SEEK_END)
        with Monitor(directory) as monitor:
            type_text(monitor, command + "\n")
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            pending += log.read()
            for match in list(pattern.finditer(pending)):
                record = match[1].decode("ascii")
                if record.startswith("BEGIN:"):
                    _, size, checksum = record.split(":")
                    header = Header(size=int(size), sha256=checksum)
                elif record == "END":
                    data = b""
                    for offset, chunk in sorted(chunks.items()):
                        if offset != len(data):
                            msg = f"missing serial data at offset {len(data)}"
                            raise RuntimeError(msg)
                        data += chunk
                    if header is None or len(data) != header.size or hashlib.sha256(data).hexdigest() != header.sha256:
                        msg = "serial transfer failed its size/checksum check; inspect the shell and retry"
                        raise RuntimeError(msg)
                    with output.open("xb") as target:
                        target.write(data)
                    return
                else:
                    offset, payload = record.split(":", 1)
                    chunks[int(offset)] = base64.b64decode(payload, validate=True)
            if matches := list(pattern.finditer(pending)):
                pending = pending[matches[-1].end() :]
            time.sleep(0.05)
    msg = "timed out retrieving the file; check the diagnostic shell screenshot and serial transcript"
    raise TimeoutError(msg)


def ssh(directory: Path, output: Path, guest_path: str, identity: Path | None, password_env: str | None) -> None:
    """Fetch one file over SSH, keeping credentials out of command arguments."""
    session = Session.model_validate_json((directory / "session.json").read_text())
    if not session.ssh_port:
        msg = "this session has SSH forwarding disabled"
        raise RuntimeError(msg)
    cmd = [
        "ssh", "-p", str(session.ssh_port), "-o", "ConnectTimeout=10", "-o", "StrictHostKeyChecking=accept-new",
        "-o", f"UserKnownHostsFile={directory / 'known_hosts'}",
    ]  # fmt: skip
    if identity:
        cmd += ["-i", str(identity)]
    env = dict(os.environ)
    if password_env:
        if not shutil.which("sshpass"):
            msg = "install sshpass to use --password-env"
            raise RuntimeError(msg)
        env["SSHPASS"] = env[password_env]
        cmd = ["sshpass", "-e", *cmd]
    else:
        cmd += ["-o", "BatchMode=yes"]
    cmd += ["root@127.0.0.1", f"cat -- {shlex.quote(guest_path)}"]
    with output.open("xb") as target:
        subprocess.run(cmd, stdout=target, env=env, check=True, timeout=120)


def main() -> None:
    """Select a transfer method and save the requested guest file locally."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vm-dir", type=Path, required=True)
    parser.add_argument(
        "--output", type=Path, required=True, help="New local file; existing files are not overwritten."
    )
    parser.add_argument("--guest-path", default="/tmp/install-log")  # noqa: S108  # existing guest log
    parser.add_argument("--transcript", type=Path, help="Serial transcript; defaults to <vm-dir>/serial.log.")
    parser.add_argument("--device", default="/dev/hvc0", help="Guest console device receiving the framed export.")
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("--ssh", action="store_true", help="Use SSH instead of typing into the open diagnostic shell.")
    parser.add_argument("--identity", type=Path)
    parser.add_argument("--password-env", help="Environment variable holding the SSH password; requires sshpass.")
    args = parser.parse_args()
    directory = args.vm_dir.absolute()
    if args.output.exists():
        parser.error(f"output already exists: {args.output}")
    if args.ssh:
        ssh(directory, args.output, args.guest_path, args.identity, args.password_env)
    else:
        serial(
            directory,
            args.transcript or directory / "serial.log",
            args.output,
            guest_path=args.guest_path,
            device=args.device,
            timeout=args.timeout,
        )
    print(args.output)


if __name__ == "__main__":
    main()
