"""Pinned, opt-in personal skill synchronization. No skill payload is executed."""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib

if __package__:
    from .install import digest, is_linked, read_regular, resolve_home
else:
    from install import digest, is_linked, read_regular, resolve_home

LICENSE_ADDITIONS = {"LICENSE", "LICENSE.txt", "LICENSE.md", "NOTICE", "NOTICE.txt", "NOTICE.md",
                     "THIRD_PARTY_NOTICES", "THIRD_PARTY_NOTICES.txt", "THIRD_PARTY_NOTICES.md"}


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def ordinary_parents(path: Path):
    for parent in (path, *path.parents):
        if is_linked(parent):
            raise ValueError(f"Managed skill paths must not contain symlinks or junctions: {parent}")


def relative_name(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError("Skill files require portable relative paths")
    parts = PurePosixPath(value).parts
    if PurePosixPath(value).is_absolute() or any(p in {".", ".."} for p in parts) or "/".join(parts) != value:
        raise ValueError("Skill files require normalized relative paths without traversal")
    # Windows reserves these names even when a filename has an extension.
    for part in parts:
        if part.endswith((".", " ")) or any(ord(c) < 32 or c in '<>"|?*' for c in part):
            raise ValueError("Skill filename is not portable")
        if part.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}:
            raise ValueError("Skill filename uses a reserved Windows name")
    return value


def skills_at(repo: Path, commit: str) -> dict:
    """Read the manifest and every package byte from the requested Git object."""
    def git(*args):
        return subprocess.check_output(["git", "-C", str(repo), *args])
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Use the complete 40-character commit SHA")
    records = {}
    for record in git("ls-tree", "-rz", commit, "--", "skills").split(b"\0"):
        if record:
            meta, name = record.split(b"\t", 1)
            records[name.decode("utf-8")] = meta.split()[0]
    if records.get("skills/manifest.json") != b"100644":
        raise ValueError("Missing ordinary skills/manifest.json at requested commit")
    manifest_bytes = git("show", f"{commit}:skills/manifest.json")
    manifest = json.loads(manifest_bytes)
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("skills"), list):
        raise ValueError("Unsupported skill manifest schema")
    packages, seen, declared = {}, set(), set()
    for entry in manifest["skills"]:
        if not isinstance(entry, dict):
            raise ValueError("Each skill manifest entry must be an object")
        name = entry.get("name", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name in seen:
            raise ValueError("Skill names must be unique lowercase portable directory names")
        seen.add(name)
        prefix = f"skills/packages/{name}"
        if entry.get("path") != prefix:
            raise ValueError("Skill path must be skills/packages/<name>")
        source = entry.get("source", {})
        if not isinstance(source, dict) or any(not isinstance(source.get(key), str) or not source[key].strip() for key in ("url", "revision", "license")):
            raise ValueError("Each skill requires source url, fixed revision and license provenance")
        if source.get("kind") == "locally-adapted":
            if not re.fullmatch(r"sha256:[0-9a-f]{64}", source["revision"]) or not re.fullmatch(r"[0-9a-f]{40}", source.get("upstream_revision", "")):
                raise ValueError("Adapted skills require a fixed local tree digest and complete upstream commit")
        elif not re.fullmatch(r"[0-9a-f]{40}", source["revision"]):
            raise ValueError("Skill source revision must be a complete pinned commit SHA")
        files = entry.get("files")
        if not isinstance(files, dict) or "SKILL.md" not in files:
            raise ValueError("Each skill must declare its complete file set including SKILL.md")
        contents, case_names, portable_entries = {}, set(), {}
        for rel, expected in files.items():
            relative_name(rel)
            if rel.casefold() in case_names or not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
                raise ValueError("Skill files require unique portable names and SHA-256 digests")
            case_names.add(rel.casefold())
            for part in (PurePosixPath(rel), *PurePosixPath(rel).parents):
                if str(part) == ".":
                    continue
                key = str(part).casefold()
                if key in portable_entries and portable_entries[key] != str(part):
                    raise ValueError("Skill file and directory names collide on case-insensitive platforms")
                portable_entries[key] = str(part)
            full = prefix + "/" + rel
            if records.get(full) != b"100644":
                raise ValueError(f"Missing, executable or linked skill source (ordinary 100644 files required): {full}")
            content = git("show", f"{commit}:{full}")
            if digest(content) != expected:
                raise ValueError(f"Skill manifest hash mismatch: {full}")
            contents[rel] = content
            declared.add(full)
        adoption = entry.get("adoption_files")
        if adoption is not None:
            if not isinstance(adoption, dict) or "SKILL.md" not in adoption or any(files.get(n) != h for n, h in adoption.items()):
                raise ValueError("adoption_files must pin an exact original file set unchanged in desired files")
            additions = set(files) - set(adoption)
            if not additions or not additions <= LICENSE_ADDITIONS:
                raise ValueError("Adoption may only append named top-level license/notice files")
            for license_name in additions:
                text = contents[license_name].decode("utf-8")
                if not text.strip() or any(ord(c) < 32 and c not in "\n\r\t" for c in text):
                    raise ValueError("Adoption license additions must be ordinary UTF-8 text")
        requires = entry.get("requires", [])
        if not isinstance(requires, list):
            raise ValueError("Skill requires must be a list")
        for requirement in requires:
            if not isinstance(requirement, dict) or requirement.get("command") not in {"node", "python", "uv", "git"} or not re.fullmatch(r"[0-9]+(?:\.[0-9]+){0,2}", requirement.get("min_version", "")):
                raise ValueError("Skill requirements allow only fixed tool --version probes")
        if not isinstance(entry.get("depends_on", []), list) or any(not isinstance(n, str) for n in entry.get("depends_on", [])):
            raise ValueError("Skill depends_on must list manifest skill names")
        packages[name] = {"entry": entry, "contents": contents}
    if {n for n in records if n.startswith("skills/packages/")} != declared:
        raise ValueError("Skill package tree contains undeclared files")
    for name, package in packages.items():
        if any(n not in packages or n == name for n in package["entry"].get("depends_on", [])):
            raise ValueError("Skill dependency must identify another manifest skill")
    return {"manifest_sha256": digest(manifest_bytes), "packages": packages}


def resolve_skills_home(explicit, codex_home: Path, names, *, home=None) -> Path:
    if explicit is not None:
        # Validate without resolving links away before the managed-path check.
        resolve_home(explicit)
        result = Path(explicit).expanduser().absolute()
        ordinary_parents(result)
        return result
    native_home = Path.home() if home is None else Path(home)
    candidates = list(dict.fromkeys([native_home / ".agents" / "skills", codex_home / "skills"]))
    existing = []
    for path in candidates:
        ordinary_parents(path)
        if path.exists() and not path.is_dir():
            raise ValueError(f"Skill home is not a directory: {path}")
        if path.exists() and any(p.name != ".system" and not p.name.startswith(".") for p in path.iterdir()):
            existing.append(path)
    if len(existing) > 1:
        raise ValueError("Personal skills exist in both .agents/skills and Codex home/skills; select --skills-home explicitly")
    result = existing[0] if existing else candidates[0]
    ordinary_parents(result)
    return result


def tree_state(path: Path) -> dict | None:
    ordinary_parents(path)
    if not path.exists():
        return None
    if not path.is_dir():
        raise ValueError(f"Expected skill directory: {path}")
    result = {}
    for child in sorted(path.rglob("*")):
        if is_linked(child):
            raise ValueError(f"Refusing linked skill entry: {child}")
        rel = child.relative_to(path).as_posix()
        if child.is_dir():
            result[rel + "/"] = "directory"
        elif child.is_file():
            result[rel] = digest(child.read_bytes())
        else:
            raise ValueError(f"Refusing special skill entry: {child}")
    return result


def desired_state(contents: dict) -> dict:
    result = {name: digest(content) for name, content in contents.items()}
    for name in contents:
        for parent in PurePosixPath(name).parents:
            if str(parent) != ".":
                result[str(parent) + "/"] = "directory"
    return result


def adoption_state(files: dict) -> dict:
    result = dict(files)
    for name in files:
        for parent in PurePosixPath(name).parents:
            if str(parent) != ".":
                result[str(parent) + "/"] = "directory"
    return result


def read_receipt(codex_home: Path, skills_home: Path):
    path = codex_home / "agent-playbook" / "skills-receipt.json"
    ordinary_parents(path)
    raw = read_regular(path)
    if raw is None:
        return path, raw, {"schema_version": 1, "skills_home": str(skills_home), "skills": {}}
    receipt = json.loads(raw)
    if receipt.get("schema_version") != 1 or receipt.get("skills_home") != str(skills_home) or not isinstance(receipt.get("skills"), dict):
        raise ValueError("Skill receipt belongs to another skill home or unsupported schema; inspect without overwriting")
    for name, entry in receipt["skills"].items():
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or not isinstance(entry, dict) or not isinstance(entry.get("tree"), dict):
            raise ValueError("Malformed managed skill receipt")
    return path, raw, receipt


def disabled_skills(codex_home: Path, skills_home: Path, names) -> set:
    raw = read_regular(codex_home / "config.toml")
    config = tomllib.loads(raw.decode("utf-8")) if raw is not None else {}
    disabled = set()
    settings = config.get("skills", {}).get("config", [])
    if not isinstance(settings, list):
        raise ValueError("Unsupported skills.config configuration; inspect client enable settings")
    for setting in settings:
        if isinstance(setting, dict) and setting.get("enabled") is False:
            value = setting.get("path")
            if isinstance(value, str):
                candidate = Path(value).expanduser()
                for name in names:
                    if candidate in {skills_home / name, skills_home / name / "SKILL.md"}:
                        disabled.add(name)
    return disabled


def probe_requirement(requirement: dict) -> dict:
    command = requirement["command"]
    executable = sys.executable if command == "python" else shutil.which(command)
    report = dict(requirement, status="missing")
    if executable is None:
        return report
    try:
        completed = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=10, check=True)
        match = re.search(r"(?<![0-9])([0-9]+(?:\.[0-9]+){1,2})", completed.stdout + completed.stderr)
        if not match:
            return dict(report, status="unknown")
        version = match.group(1)
        def numeric(value):
            return tuple((list(map(int, value.split("."))) + [0, 0])[:3])
        return dict(report, status="available" if numeric(version) >= numeric(requirement["min_version"]) else "too_old", version=version)
    except (OSError, subprocess.SubprocessError):
        return dict(report, status="unknown")


def plan_skills(codex_home: Path, skills_home: Path, source: dict, commit: str) -> dict:
    ordinary_parents(skills_home)
    receipt_path, raw, receipt = read_receipt(codex_home, skills_home)
    disabled = disabled_skills(codex_home, skills_home, source["packages"])
    statuses, states, requirements = [], {}, {}
    for name, package in source["packages"].items():
        actual = tree_state(skills_home / name)
        desired = desired_state(package["contents"])
        old = receipt["skills"].get(name)
        if actual is None:
            status = "missing"
        elif actual == desired:
            status = "matching" if old else "adopt"
        elif old and actual == old["tree"]:
            status = "update"
        elif not old and package["entry"].get("adoption_files") and actual == adoption_state(package["entry"]["adoption_files"]):
            status = "adopt_with_licenses"
        else:
            status = "conflict"
        states[name] = actual
        needed = []
        for requirement in package["entry"].get("requires", []):
            key = (requirement["command"], requirement["min_version"])
            if key not in requirements:
                requirements[key] = probe_requirement(requirement)
            needed.append(requirements[key])
        statuses.append({"name": name, "status": status, "managed": old is not None,
                         "disabled": name in disabled, "requires": needed,
                         "depends_on": package["entry"].get("depends_on", [])})
    retired = sorted(set(receipt["skills"]) - set(source["packages"]))
    unmanaged = []
    if skills_home.exists():
        unmanaged = sorted(p.name for p in skills_home.iterdir() if p.name not in source["packages"] and not p.name.startswith("."))
    ready = all(s["status"] == "matching" and not s["disabled"] and all(r["status"] == "available" for r in s["requires"]) for s in statuses)
    state_hash = digest(canonical({"home": str(skills_home), "trees": states, "receipt": digest(raw), "disabled": sorted(disabled)}))
    return {"skills_home": str(skills_home), "skills_state_sha256": state_hash,
            "manifest_sha256": source["manifest_sha256"], "skills": statuses,
            "unmanaged": unmanaged, "retained_from_previous_manifest": retired,
            "ready": ready, "client_discovery": "pending_client_verification"}


@contextmanager
def skills_lock(skills_home: Path):
    ordinary_parents(skills_home)
    skills_home.parent.mkdir(parents=True, exist_ok=True)
    lock = skills_home.parent / ".agent-playbook-skills-install.lock"
    ordinary_parents(lock)
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(str(os.getpid()))
    try:
        yield
    finally:
        lock.unlink()


def require_applicable(plan, expected):
    if expected is None or expected != plan["skills_state_sha256"]:
        raise ValueError("Skill target changed or missing --expect-skills-sha256; inspect and preview again")
    if any(s["status"] == "conflict" for s in plan["skills"]):
        raise ValueError("Skill conflicts require review; existing files were preserved")


def apply_skills(codex_home: Path, skills_home: Path, source: dict, commit: str, expected: str) -> dict:
    """Caller holds the skill lock. Core installation is a separate atomic step."""
    plan = plan_skills(codex_home, skills_home, source, commit)
    require_applicable(plan, expected)
    receipt_path, receipt_raw, receipt = read_receipt(codex_home, skills_home)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup_dir = codex_home / "agent-playbook" / "skill-backups" / stamp
    ordinary_parents(backup_dir)
    # Complete and verify every backup before replacing any managed skill.
    backups = []
    for item in plan["skills"]:
        if item["status"] in {"update", "adopt_with_licenses"}:
            name = item["name"]
            backup = backup_dir / name
            backup.parent.mkdir(parents=True, exist_ok=True)
            before = tree_state(skills_home / name)
            shutil.copytree(skills_home / name, backup)
            if tree_state(backup) != before:
                raise ValueError("Skill backup verification failed")
            backups.append(str(backup))
    skills_home.mkdir(parents=True, exist_ok=True)
    stage_root = Path(tempfile.mkdtemp(prefix=".playbook-stage-", dir=skills_home))
    changed, rollback_errors = [], []
    receipt_temp, receipt_committed = None, False
    try:
        for item in plan["skills"]:
            name = item["name"]
            if item["status"] not in {"missing", "update", "adopt_with_licenses"}:
                continue
            staged = stage_root / name
            staged.mkdir()
            for rel, content in source["packages"][name]["contents"].items():
                path = staged / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            if tree_state(staged) != desired_state(source["packages"][name]["contents"]):
                raise ValueError("Staged skill verification failed")
        # Last cooperative CAS before the first replacement, after staging/backups.
        require_applicable(plan_skills(codex_home, skills_home, source, commit), expected)
        for item in plan["skills"]:
            name = item["name"]
            if item["status"] not in {"missing", "update", "adopt_with_licenses"}:
                continue
            target = skills_home / name
            old_path = stage_root / (name + ".rollback")
            if item["status"] in {"update", "adopt_with_licenses"}:
                target.rename(old_path)
            changed.append((target, old_path))
            (stage_root / name).rename(target)
            if tree_state(target) != desired_state(source["packages"][name]["contents"]):
                raise ValueError("Installed skill verification failed")
        updated = dict(receipt["skills"])
        for name, package in source["packages"].items():
            updated[name] = {"tree": desired_state(package["contents"]), "source_commit": commit,
                             "source": package["entry"]["source"]}
        new_receipt = canonical({"schema_version": 1, "skills_home": str(skills_home),
                                 "source_commit": commit, "manifest_sha256": source["manifest_sha256"], "skills": updated}) + b"\n"
        if new_receipt != receipt_raw:
            receipt_path.parent.mkdir(parents=True, exist_ok=True)
            if receipt_raw is not None:
                backup_dir.mkdir(parents=True, exist_ok=True)
                receipt_backup = backup_dir / "skills-receipt.json"
                receipt_backup.write_bytes(receipt_raw)
                if receipt_backup.read_bytes() != receipt_raw:
                    raise ValueError("Skill receipt backup verification failed")
                backups.append(str(receipt_backup))
            fd, temporary = tempfile.mkstemp(prefix=".skills-receipt-", dir=receipt_path.parent)
            receipt_temp = Path(temporary)
            with os.fdopen(fd, "wb") as stream:
                stream.write(new_receipt)
                stream.flush()
                os.fsync(stream.fileno())
            if read_regular(receipt_path) != receipt_raw:
                raise ValueError("Skill receipt changed before replacement")
            os.replace(receipt_temp, receipt_path)
            receipt_temp = None
        receipt_committed = True
        result = plan_skills(codex_home, skills_home, source, commit)
        result.update(verified=True, backups=backups)
        return result
    except (OSError, ValueError) as exc:
        if receipt_committed:
            raise OSError(f"Skill files and receipt committed; post-install verification failed: {exc}") from exc
        for target, old_path in reversed(changed):
            try:
                if target.exists():
                    shutil.rmtree(target)
                if old_path.exists():
                    old_path.rename(target)
            except OSError as rollback_error:
                rollback_errors.append(str(rollback_error))
        if rollback_errors:
            # Keep rollback trees for recovery; never delete the only surviving old bytes.
            raise OSError(f"Skill installation failed; partial skill rollback, recovery directory {stage_root}: {rollback_errors}") from exc
        raise
    finally:
        if receipt_temp is not None and receipt_temp.exists():
            receipt_temp.unlink()
        if not rollback_errors and stage_root.exists():
            shutil.rmtree(stage_root)
