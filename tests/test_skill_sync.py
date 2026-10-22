import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.install import digest, documents_at, install_environment
from scripts.skill_sync import (apply_skills, canonical, desired_state, plan_skills,
                                probe_requirement, resolve_skills_home, skills_at,
                                skills_lock, tree_state)
from tests.test_install import SHA, fixture


def source_fixture(extra=b"original"):
    contents = {"SKILL.md": b"---\nname: example\n---\n# Example\n", "scripts/tool.py": extra}
    return {"manifest_sha256": digest(b"fixture"), "packages": {
        "example": {"entry": {"source": {"url": "https://example.invalid/skills", "revision": SHA, "license": "MIT"},
                              "requires": [], "depends_on": []}, "contents": contents}}}


def write_package(root, contents):
    for name, content in contents.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)


class SkillSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / "使用者 space" / ".codex"
        self.skills = self.root / "使用者 space" / ".agents" / "skills"
        self.source = source_fixture()

    def plan(self, source=None):
        return plan_skills(self.home, self.skills, source or self.source, SHA)

    def apply(self, source=None, expected=None):
        data = source or self.source
        state = self.plan(data)["skills_state_sha256"] if expected is None else expected
        with skills_lock(self.skills):
            return apply_skills(self.home, self.skills, data, SHA, state)

    def test_preview_check_no_install_writes_and_default_native_location(self):
        plan = self.plan()
        self.assertEqual(plan["skills"][0]["status"], "missing")
        self.assertEqual(plan["client_discovery"], "pending_client_verification")
        self.assertFalse(self.home.parent.exists())
        self.assertEqual(resolve_skills_home(None, self.home, ["example"], home=self.home.parent), self.skills)
        self.assertFalse(self.home.parent.exists())

    def test_existing_home_selected_and_two_locations_are_ambiguous(self):
        legacy = self.home / "skills"
        (legacy / "example").mkdir(parents=True)
        self.assertEqual(resolve_skills_home(None, self.home, ["example"], home=self.home.parent), legacy)
        (self.skills / "another").mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "both"):
            resolve_skills_home(None, self.home, ["example"], home=self.home.parent)
        self.assertEqual(resolve_skills_home(str(legacy), self.home, ["example"]), legacy)
        for value in ("relative", "", "C:relative"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                resolve_skills_home(value, self.home, ["example"])

    def test_two_devices_same_bytes_and_idempotent_receipt(self):
        first = self.apply()
        self.assertTrue(first["ready"])
        receipt = self.home / "agent-playbook/skills-receipt.json"
        old = receipt.read_bytes()
        second = self.apply()
        self.assertEqual(second["backups"], [])
        self.assertEqual(receipt.read_bytes(), old)
        other_home = self.root / "另一台" / ".codex"
        other_skills = self.root / "另一台" / ".agents/skills"
        planned = plan_skills(other_home, other_skills, self.source, SHA)
        with skills_lock(other_skills):
            apply_skills(other_home, other_skills, self.source, SHA, planned["skills_state_sha256"])
        self.assertEqual(tree_state(self.skills / "example"), tree_state(other_skills / "example"))

    def test_only_exact_unmanaged_package_is_adopted(self):
        write_package(self.skills / "example", self.source["packages"]["example"]["contents"])
        self.assertEqual(self.plan()["skills"][0]["status"], "adopt")
        self.assertFalse(self.plan()["ready"])
        self.apply()
        self.assertEqual(self.plan()["skills"][0]["status"], "matching")
        self.assertFalse((self.home / "agent-playbook/skill-backups").exists())

    def test_exact_reviewed_original_adoption_appends_only_license_and_backs_up(self):
        original = self.source["packages"]["example"]["contents"].copy()
        self.source["packages"]["example"]["entry"]["adoption_files"] = {n: digest(b) for n, b in original.items()}
        self.source["packages"]["example"]["contents"]["LICENSE"] = b"MIT License\n"
        write_package(self.skills / "example", original)
        self.assertEqual(self.plan()["skills"][0]["status"], "adopt_with_licenses")
        result = self.apply()
        self.assertTrue(result["verified"])
        self.assertEqual(tree_state(Path(result["backups"][0])), desired_state(original))
        self.assertEqual((self.skills / "example/LICENSE").read_bytes(), b"MIT License\n")
        for name, content in original.items():
            self.assertEqual((self.skills / "example" / name).read_bytes(), content)

    def test_receipt_commit_then_verification_failure_retains_consistent_new_files(self):
        self.apply()
        updated = source_fixture(b"new tool")
        reviewed = self.plan(updated)["skills_state_sha256"]
        original = plan_skills
        calls = 0
        def fail_post_commit(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError("post-commit read failed")
            return original(*args, **kwargs)
        with patch("scripts.skill_sync.plan_skills", side_effect=fail_post_commit):
            with self.assertRaisesRegex(OSError, "files and receipt committed"):
                self.apply(updated, expected=reviewed)
        self.assertEqual((self.skills / "example/scripts/tool.py").read_bytes(), b"new tool")
        self.assertEqual(self.plan(updated)["skills"][0]["status"], "matching")

    def test_unknown_same_name_and_extra_empty_directory_preserved(self):
        write_package(self.skills / "example", self.source["packages"]["example"]["contents"])
        (self.skills / "example/unknown-empty").mkdir()
        before = tree_state(self.skills / "example")
        self.assertEqual(self.plan()["skills"][0]["status"], "conflict")
        with self.assertRaisesRegex(ValueError, "conflicts"):
            self.apply()
        self.assertEqual(tree_state(self.skills / "example"), before)

    def test_conflict_preflight_prevents_core_write(self):
        write_package(self.skills / "example", {"SKILL.md": b"private local skill"})
        planned = self.plan()
        with self.assertRaisesRegex(ValueError, "conflicts"):
            install_environment(self.home, SHA, fixture(), apply=True, expected="missing",
                                skills_source=self.source, skills_home=self.skills,
                                expected_skills=planned["skills_state_sha256"])
        self.assertFalse((self.home / "AGENTS.md").exists())
        self.assertFalse((self.home / "agent-playbook").exists())

    def test_managed_local_edits_and_cas_stop_without_overwrite(self):
        self.apply()
        reviewed = self.plan()["skills_state_sha256"]
        target = self.skills / "example/SKILL.md"
        target.write_bytes(b"local changes")
        with self.assertRaisesRegex(ValueError, "changed"):
            self.apply(expected=reviewed)
        self.assertEqual(self.plan()["skills"][0]["status"], "conflict")
        with self.assertRaisesRegex(ValueError, "conflicts"):
            self.apply()
        self.assertEqual(target.read_bytes(), b"local changes")

    def test_managed_update_backups_and_manifest_removal_never_deletes(self):
        self.apply()
        old = tree_state(self.skills / "example")
        updated = source_fixture(b"new tool")
        self.assertEqual(self.plan(updated)["skills"][0]["status"], "update")
        result = self.apply(updated)
        backup = next(Path(p) for p in result["backups"] if Path(p).name == "example")
        self.assertEqual(tree_state(backup), old)
        empty = {"manifest_sha256": digest(b"empty"), "packages": {}}
        retained = self.apply(empty)
        self.assertEqual(retained["retained_from_previous_manifest"], ["example"])
        self.assertTrue((self.skills / "example/SKILL.md").exists())

    def test_backup_failure_keeps_skills_and_receipt_and_reports_core_partial(self):
        self.apply()
        old = tree_state(self.skills / "example")
        receipt = (self.home / "agent-playbook/skills-receipt.json").read_bytes()
        updated = source_fixture(b"new tool")
        with patch("scripts.skill_sync.shutil.copytree", side_effect=OSError("backup unavailable")):
            result = install_environment(self.home, SHA, fixture(), apply=True, expected="missing",
                                         skills_source=updated, skills_home=self.skills,
                                         expected_skills=self.plan(updated)["skills_state_sha256"])
        self.assertEqual(result["status"], "partial")
        self.assertIn("Core step completed", result["error"])
        self.assertEqual((self.home / "AGENTS.md").read_bytes(), fixture()["instructions/codex.md"])
        self.assertEqual(tree_state(self.skills / "example"), old)
        self.assertEqual((self.home / "agent-playbook/skills-receipt.json").read_bytes(), receipt)

    def test_failed_skill_replacement_rolls_back_and_retains_backup(self):
        self.apply()
        old = tree_state(self.skills / "example")
        receipt = (self.home / "agent-playbook/skills-receipt.json").read_bytes()
        original = Path.rename
        def fail_stage(path, target):
            if path.name == "example" and path.parent.name.startswith(".playbook-stage-"):
                raise OSError("replace failed")
            return original(path, target)
        with patch.object(Path, "rename", fail_stage):
            with self.assertRaisesRegex(OSError, "replace failed"):
                self.apply(source_fixture(b"new tool"))
        self.assertEqual(tree_state(self.skills / "example"), old)
        self.assertEqual((self.home / "agent-playbook/skills-receipt.json").read_bytes(), receipt)
        self.assertTrue(list((self.home / "agent-playbook/skill-backups").glob("*/example")))
        self.assertFalse(list(self.skills.glob(".playbook-stage-*")))

    def test_receipt_replace_failure_rolls_back_skill(self):
        self.apply()
        old = tree_state(self.skills / "example")
        with patch("scripts.skill_sync.os.replace", side_effect=OSError("receipt failed")):
            with self.assertRaisesRegex(OSError, "receipt failed"):
                self.apply(source_fixture(b"new tool"))
        self.assertEqual(tree_state(self.skills / "example"), old)

    def test_disabled_config_and_missing_runtime_are_separate_from_installation(self):
        self.home.mkdir(parents=True)
        path = (self.skills / "example").as_posix()
        (self.home / "config.toml").write_text(f'[[skills.config]]\npath = "{path}"\nenabled = false\n')
        self.source["packages"]["example"]["entry"]["requires"] = [{"command": "node", "min_version": "20"}]
        with patch("scripts.skill_sync.shutil.which", return_value=None):
            result = self.apply()
        self.assertTrue(result["verified"])
        self.assertFalse(result["ready"])
        self.assertTrue(result["skills"][0]["disabled"])
        self.assertEqual(result["skills"][0]["requires"][0]["status"], "missing")
        self.assertIn("enabled = false", (self.home / "config.toml").read_text())

    def test_explicit_only_skill_is_not_disabled_and_probe_only_runs_version(self):
        self.source["packages"]["example"]["contents"]["agents/openai.yaml"] = b"policy:\n  allow_implicit_invocation: false\n"
        self.assertFalse(self.apply()["skills"][0]["disabled"])
        with patch("scripts.skill_sync.shutil.which", return_value="/known/node"), patch("scripts.skill_sync.subprocess.run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, "v22.1.0\n", "")
            self.assertEqual(probe_requirement({"command": "node", "min_version": "20"})["status"], "available")
            self.assertEqual(run.call_args.args[0], ["/known/node", "--version"])

    def test_foreign_receipt_and_stale_lock_refuse(self):
        self.apply()
        other = self.root / "another-skills"
        with self.assertRaisesRegex(ValueError, "another skill home"):
            plan_skills(self.home, other, self.source, SHA)
        lock = self.skills.parent / ".agent-playbook-skills-install.lock"
        lock.write_text("inspect stale lock")
        with self.assertRaises(FileExistsError):
            self.apply()
        self.assertEqual(lock.read_text(), "inspect stale lock")

    @unittest.skipIf(os.name == "nt", "Unprivileged symlink creation is platform-dependent")
    def test_symlink_root_and_nested_entry_refuse_without_touching_outside(self):
        outside = self.root / "outside"
        outside.mkdir()
        self.skills.parent.mkdir(parents=True)
        self.skills.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            resolve_skills_home(str(self.skills), self.home, ["example"])
        self.assertEqual(list(outside.iterdir()), [])
        self.skills.unlink()
        write_package(self.skills / "example", {"SKILL.md": b"local"})
        (self.skills / "example/link").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "linked"):
            self.plan()

    @unittest.skipUnless(os.name == "nt", "Windows junction protection requires Windows")
    def test_windows_junction_skill_home_refuses(self):
        outside = self.root / "outside"
        outside.mkdir()
        self.skills.parent.mkdir(parents=True)
        subprocess.run(["cmd", "/c", "mklink", "/J", str(self.skills), str(outside)], check=True, capture_output=True)
        try:
            with self.assertRaises(ValueError):
                resolve_skills_home(str(self.skills), self.home, ["example"])
            self.assertEqual(list(outside.iterdir()), [])
        finally:
            self.skills.rmdir()


class SkillSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name).resolve()
        self.git("init")
        self.git("config", "core.autocrlf", "false")
        package = source_fixture()["packages"]["example"]
        self.entry = dict(package["entry"], name="example", path="skills/packages/example",
                          files={n: digest(b) for n, b in package["contents"].items()})
        write_package(self.repo / "skills/packages/example", package["contents"])
        write_package(self.repo, fixture())

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], stderr=subprocess.STDOUT)

    def commit(self):
        (self.repo / "skills/manifest.json").write_bytes(canonical({"schema_version": 1, "skills": [self.entry]}))
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "--allow-empty", "-m", "fixture")
        return self.git("rev-parse", "HEAD").decode().strip()

    def test_manifest_reads_fixed_git_bytes_and_excludes_packages_from_guides(self):
        commit = self.commit()
        loaded = skills_at(self.repo, commit)
        self.assertEqual(loaded["packages"]["example"]["contents"]["scripts/tool.py"], b"original")
        self.assertNotIn("skills/packages/example/SKILL.md", documents_at(self.repo, commit))
        (self.repo / "skills/packages/example/SKILL.md").write_bytes(b"dirty source ignored by object reader")
        self.assertNotEqual(loaded["packages"]["example"]["contents"]["SKILL.md"], b"dirty source ignored by object reader")

    def test_cli_readonly_check_apply_and_legacy_core_interface(self):
        source_root = Path(__file__).resolve().parents[1]
        write_package(self.repo, {f"scripts/{n}": (source_root / "scripts" / n).read_bytes() for n in ("install.py", "skill_sync.py")})
        pinned = self.commit()
        core_path = self.repo / "instructions/codex.md"
        core_path.write_bytes(core_path.read_bytes().replace(SHA.encode(), pinned.encode()))
        commit = self.commit()
        self.git("update-ref", "refs/remotes/origin/main", commit)
        home, skills = self.repo.parent / (self.repo.name + "-home"), self.repo.parent / (self.repo.name + "-skills")
        self.addCleanup(shutil.rmtree, home, True)
        self.addCleanup(shutil.rmtree, skills, True)
        command = [sys.executable, str(self.repo / "scripts/install.py"), "--commit", commit,
                   "--codex-home", str(home), "--skills-home", str(skills), "--with-skills"]
        checked = subprocess.run(command + ["--check"], capture_output=True, check=False)
        self.assertEqual(checked.returncode, 2, checked.stderr.decode())
        report = json.loads(checked.stdout)
        self.assertFalse(home.exists())
        self.assertFalse(skills.exists())
        self.assertEqual(report["core"]["snapshot_status"], "missing")
        applied = subprocess.run(command + ["--apply", "--expect-current-sha256", "missing",
                                            "--expect-skills-sha256", report["skills"]["skills_state_sha256"]], capture_output=True, check=False)
        self.assertEqual(applied.returncode, 0, applied.stderr.decode())
        self.assertEqual(subprocess.run(command + ["--check"], capture_output=True).returncode, 0)
        (self.repo / "skills/packages/example/SKILL.md").write_bytes(b"dirty working source")
        dirty = subprocess.run(command + ["--check"], capture_output=True)
        self.assertEqual(dirty.returncode, 1)
        self.assertIn(b"clean checkout", dirty.stderr)

    def test_hash_mismatch_undeclared_file_and_traversal_refuse(self):
        self.entry["files"]["SKILL.md"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            skills_at(self.repo, self.commit())
        self.entry["files"]["SKILL.md"] = digest((self.repo / "skills/packages/example/SKILL.md").read_bytes())
        (self.repo / "skills/packages/example/unknown.txt").write_bytes(b"undeclared")
        with self.assertRaisesRegex(ValueError, "undeclared"):
            skills_at(self.repo, self.commit())
        self.entry["files"]["../escape"] = digest(b"escape")
        with self.assertRaisesRegex(ValueError, "traversal"):
            skills_at(self.repo, self.commit())

    def test_license_adoption_rejects_changed_original_or_nonlicense_addition(self):
        self.entry["adoption_files"] = self.entry["files"].copy()
        path = self.repo / "skills/packages/example/LICENSE"
        path.write_bytes(b"MIT License\n")
        self.entry["files"]["LICENSE"] = digest(path.read_bytes())
        self.assertIn("adoption_files", skills_at(self.repo, self.commit())["packages"]["example"]["entry"])
        self.entry["adoption_files"]["SKILL.md"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "original file set unchanged"):
            skills_at(self.repo, self.commit())
        self.entry["adoption_files"] = {n: h for n, h in self.entry["files"].items() if n != "LICENSE"}
        path = self.repo / "skills/packages/example/new-tool.py"
        path.write_bytes(b"new program")
        self.entry["files"]["new-tool.py"] = digest(path.read_bytes())
        with self.assertRaisesRegex(ValueError, "only append"):
            skills_at(self.repo, self.commit())

    def test_case_colliding_directories_and_executable_sources_refuse(self):
        for rel in ("Assets/one.txt", "assets/two.txt"):
            target = self.repo / "skills/packages/example" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"data")
            self.entry["files"][rel] = digest(b"data")
        with self.assertRaisesRegex(ValueError, "collide"):
            skills_at(self.repo, self.commit())

    def test_executable_git_source_refuses_instead_of_silently_losing_mode(self):
        self.commit()
        self.git("update-index", "--chmod=+x", "skills/packages/example/scripts/tool.py")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "executable fixture")
        commit = self.git("rev-parse", "HEAD").decode().strip()
        with self.assertRaisesRegex(ValueError, "executable"):
            skills_at(self.repo, commit)

    def test_actual_vendor_manifest_hashes_and_exact_original_adoption_rules(self):
        repo = Path(__file__).resolve().parents[1]
        manifest = json.loads((repo / "skills/manifest.json").read_bytes())
        self.assertEqual(len(manifest["skills"]), 5)
        for entry in manifest["skills"]:
            directory = repo / entry["path"]
            actual = {p.relative_to(directory).as_posix(): digest(p.read_bytes()) for p in directory.rglob("*") if p.is_file()}
            self.assertEqual(entry["files"], actual)
            if "adoption_files" in entry:
                self.assertTrue(set(actual) - set(entry["adoption_files"]) <= {"LICENSE", "THIRD_PARTY_NOTICES"})
                self.assertTrue(all(actual[n] == h for n, h in entry["adoption_files"].items()))

    @unittest.skipIf(os.name == "nt", "Git symlink fixture needs native symlink support")
    def test_git_symlink_package_is_not_installed(self):
        (self.repo / "skills/packages/example/scripts/tool.py").unlink()
        (self.repo / "skills/packages/example/scripts/tool.py").symlink_to("../../outside")
        with self.assertRaisesRegex(ValueError, "linked"):
            skills_at(self.repo, self.commit())


if __name__ == "__main__":
    unittest.main()
