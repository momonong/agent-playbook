"""Install a pinned playbook using native paths; preview by default, stdlib only."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib


def digest(data: bytes | None) -> str:
    return "missing" if data is None else hashlib.sha256(data).hexdigest()


def resolve_home(explicit=None, *, environ=None, home=None) -> Path:
    env = os.environ if environ is None else environ
    value = explicit if explicit is not None else env.get("CODEX_HOME")
    if value is None:
        return ((Path.home() if home is None else Path(home)) / ".codex").resolve()
    if not value or any(c in str(value) for c in "\r\n\x00`"):
        raise ValueError("Codex home must be a nonempty native absolute path without control/backtick characters")
    path = Path(value).expanduser()
    if os.name != "nt" and (PureWindowsPath(value).drive or "\\" in str(value)):
        raise ValueError("Windows paths cannot be used in this environment; resolve the path on the executing host")
    if not path.is_absolute():
        raise ValueError("Codex home must be absolute; relative and drive-relative paths are ambiguous")
    return path.resolve()


def is_linked(path: Path) -> bool:
    if path.is_symlink():
        return True
    if os.name == "nt":
        try:
            # Python 3.11 lacks Path.is_junction; fail closed for all reparse points.
            return bool(path.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
        except FileNotFoundError:
            return False
    return False


def read_regular(path: Path) -> bytes | None:
    if is_linked(path):
        raise ValueError(f"Refusing linked managed file: {path.name}")
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError(f"Expected a regular file: {path.name}")
    return path.read_bytes()


def check_sources(home: Path):
    override = home / "AGENTS.override.md"
    if override.exists() or override.is_symlink():
        raise ValueError("AGENTS.override.md exists; inspect precedence before installing")
    raw = read_regular(home / "config.toml")
    config = tomllib.loads(raw.decode("utf-8")) if raw is not None else {}
    def check(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in {"instructions", "developer_instructions", "model_instructions_file", "experimental_instructions_file"} and value:
                    raise ValueError(f"Alternative instruction configuration requires review: {key}")
                check(value)
        elif isinstance(node, list):
            for value in node:
                check(value)
    check(config)


def guide_commit(core: bytes) -> str:
    text = core.decode("utf-8")
    matches = re.findall(r"^<!-- agent-playbook guides-commit: ([0-9a-f]{40}) -->$", text, re.MULTILINE)
    if len(matches) != 1 or "{{PLAYBOOK_" in text:
        raise ValueError("Core must be directly copyable with one pinned guides-commit and no placeholders")
    return matches[0]


def documents_at(repo: Path, commit: str):
    def git(*args):
        return subprocess.check_output(["git", "-C", str(repo), *args])
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Use the complete 40-character commit SHA")
    payload = {}
    for record in git("ls-tree", "-rz", commit).split(b"\0"):
        if not record:
            continue
        meta, raw_name = record.split(b"\t", 1)
        name = raw_name.decode("utf-8")
        if not name.endswith(".md"):
            continue
        if meta.split()[0] != b"100644" or ".." in Path(name).parts or Path(name).is_absolute() or "\\" in name:
            raise ValueError("Snapshot requires ordinary Markdown files and portable relative paths")
        payload[name] = git("show", f"{commit}:{name}")
    return payload


def payload_at(repo: Path, commit: str):
    head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"]).decode().strip()
    dirty = subprocess.check_output(["git", "-C", str(repo), "status", "--porcelain"]).strip()
    if head != commit or dirty:
        raise ValueError("Source must be a clean checkout at the requested commit")
    return documents_at(repo, commit)


def install(home: Path, commit: str, payload: dict[str, bytes], *, apply=False, expected=None, guide_payload=None):
    check_sources(home)
    target = home / "AGENTS.md"
    old = read_regular(target)
    old_hash = digest(old)
    if expected is not None and expected != old_hash:
        raise ValueError("AGENTS.md changed since preview; inspect and preview again")
    if apply and expected is None:
        raise ValueError("Apply requires --expect-current-sha256 from a reviewed preview")
    core_bytes = payload["instructions/codex.md"]
    pinned = guide_commit(core_bytes)
    if guide_payload is None:
        if pinned != commit:
            raise ValueError("Pinned guides require their own committed document payload")
        guide_payload = payload
    snapshot = home / "agent-playbook" / "versions" / pinned
    for parent in (snapshot, *snapshot.parents):
        if is_linked(parent):
            raise ValueError("Managed snapshot parents must not be symlinks or junctions")
    for guide in ("collaboration", "engineering", "model-selection", "service-integration"):
        if f"guides/{guide}.md" not in guide_payload:
            raise ValueError(f"Missing guide: {guide}")
    payload = dict(guide_payload, SOURCE_COMMIT=(pinned + "\n").encode())
    def verify_snapshot():
        actual = {p.relative_to(snapshot).as_posix() for p in snapshot.rglob("*") if p.is_file()}
        if actual != set(payload) or any(is_linked(p) for p in snapshot.rglob("*")):
            raise ValueError("Existing immutable snapshot has a different file set or linked entries")
        if any(read_regular(snapshot / name) != content for name, content in payload.items()):
            raise ValueError("Existing immutable snapshot differs from source")
    if snapshot.exists():
        verify_snapshot()
    report = dict(source_commit=commit, guides_commit=pinned, snapshot=str(snapshot), target=str(target),
                  current_sha256=old_hash, installed_sha256=digest(core_bytes),
                  installed_bytes=len(core_bytes), mode="apply" if apply else "preview")
    if not apply:
        return report
    home.mkdir(parents=True, exist_ok=True)
    lock = home / ".agent-playbook-install.lock"
    # Cooperative installer lock. A stale lock must be inspected, never silently removed.
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(str(os.getpid()))
    try:
        check_sources(home)
        if read_regular(target) != old:
            raise ValueError("AGENTS.md changed while preparing installation")
        if not snapshot.exists():
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            stage = Path(tempfile.mkdtemp(prefix=".install-", dir=snapshot.parent))
            try:
                for name, content in payload.items():
                    path = stage / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(content)
                stage.rename(snapshot)
            finally:
                if stage.exists():
                    shutil.rmtree(stage)
        verify_snapshot()
        if old == core_bytes:
            report["unchanged"] = True
            return report
        mode = stat.S_IMODE(target.stat().st_mode) if old is not None else 0o600
        if old is not None:
            backup_dir = home / "backups"
            if is_linked(backup_dir):
                raise ValueError("Backup directory must not be linked")
            backup_dir.mkdir(exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            backup = backup_dir / f"AGENTS-{stamp}-{old_hash[:12]}.md"
            with backup.open("xb") as stream:
                stream.write(old)
            os.chmod(backup, mode)
            if backup.read_bytes() != old:
                raise ValueError("Backup verification failed")
            report["backup"] = str(backup)
        fd, temporary = tempfile.mkstemp(prefix=".AGENTS-", dir=home)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(core_bytes)
                stream.flush()
                os.fsync(stream.fileno())
            os.chmod(temporary, mode)
            check_sources(home)
            if read_regular(target) != old:
                raise ValueError("AGENTS.md changed before replacement")
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        if target.read_bytes() != core_bytes:
            raise ValueError("Installed file verification failed")
        report["verified"] = True
        return report
    finally:
        lock.unlink()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--codex-home")
    parser.add_argument("--expect-current-sha256")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    try:
        payload = payload_at(repo, args.commit)
        pinned = guide_commit(payload["instructions/codex.md"])
        guides = documents_at(repo, pinned)
        if args.apply:
            subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", args.commit, "origin/main"], check=True)
        print(json.dumps(install(resolve_home(args.codex_home), args.commit, payload,
                                 apply=args.apply, expected=args.expect_current_sha256, guide_payload=guides), ensure_ascii=False, indent=2))
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Installation stopped: {exc}\n")


if __name__ == "__main__":
    main()
