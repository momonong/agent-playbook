import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts.install import digest, install, payload_at, resolve_home

SHA = 'a' * 40


def fixture():
    data = {'instructions/codex.md': b'{{PLAYBOOK_COMMIT}}\n`{{PLAYBOOK_SNAPSHOT}}`\n'}
    data.update({f'guides/{g}.md': g.encode() for g in ('collaboration', 'engineering', 'model-selection', 'service-integration')})
    return data


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / '使用者 space' / '.codex'
        self.data = fixture()

    def apply(self, expected='missing'):
        return install(self.home, SHA, self.data, apply=True, expected=expected)

    def test_native_home_and_explicit_precedence(self):
        user = Path(self.temp.name)
        explicit = user / '指定 空間'
        env = user / 'env'
        self.assertEqual(resolve_home(environ={}, home=user), user / '.codex')
        self.assertEqual(resolve_home(environ={'CODEX_HOME': str(env)}), env.resolve())
        self.assertEqual(resolve_home(str(explicit), environ={'CODEX_HOME': str(env)}), explicit.resolve())

    def test_invalid_paths_do_not_fall_back(self):
        for value in ('', 'relative', 'C:relative', 'bad\npath', '`bad`'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                resolve_home(value)
        if os.name != 'nt':
            with self.assertRaises(ValueError):
                resolve_home(r'C:\Users\Someone\.codex')

    def test_preview_does_not_write(self):
        report = install(self.home, SHA, self.data)
        self.assertEqual(report['current_sha256'], 'missing')
        self.assertFalse(self.home.exists())

    def test_first_install_and_idempotence(self):
        report = self.apply()
        self.assertTrue(report['verified'])
        current = (self.home / 'AGENTS.md').read_bytes()
        self.assertIn(self.home.as_posix().encode('utf-8'), current)
        self.assertNotIn(b'{{PLAYBOOK_', current)
        self.assertTrue(self.apply(digest(current))['unchanged'])
        self.assertFalse((self.home / 'backups').exists())

    def test_update_preserves_exact_backup(self):
        self.home.mkdir(parents=True)
        old = '舊指示\r\n'.encode()
        (self.home / 'AGENTS.md').write_bytes(old)
        report = self.apply(digest(old))
        self.assertEqual(Path(report['backup']).read_bytes(), old)
        self.assertEqual(digest((self.home / 'AGENTS.md').read_bytes()), report['rendered_sha256'])

    def test_changed_target_and_missing_expected_rejected(self):
        self.home.mkdir(parents=True)
        target = self.home / 'AGENTS.md'
        target.write_bytes(b'concurrent edit')
        for expected in ('missing', digest(b'old'), None):
            with self.subTest(expected=expected), self.assertRaises(ValueError):
                self.apply(expected)
        self.assertEqual(target.read_bytes(), b'concurrent edit')
        self.assertFalse((self.home / 'agent-playbook').exists())

    def test_override_and_nested_configuration_rejected(self):
        self.home.mkdir(parents=True)
        override = self.home / 'AGENTS.override.md'
        override.write_text('override')
        with self.assertRaises(ValueError):
            self.apply()
        override.unlink()
        (self.home / 'config.toml').write_text('[profiles.work]\nmodel_instructions_file="custom.md"\n')
        with self.assertRaises(ValueError):
            self.apply()
        self.assertFalse((self.home / 'AGENTS.md').exists())

    def test_corrupt_snapshot_rejected_even_when_target_unchanged(self):
        self.apply()
        target = self.home / 'AGENTS.md'
        current = target.read_bytes()
        (self.home / 'agent-playbook' / 'versions' / SHA / 'guides/engineering.md').write_bytes(b'corrupt')
        with self.assertRaises(ValueError):
            self.apply(digest(current))
        self.assertEqual(target.read_bytes(), current)

    def test_failed_atomic_replace_keeps_old_file_and_backup(self):
        self.home.mkdir(parents=True)
        target = self.home / 'AGENTS.md'
        target.write_bytes(b'old')
        with patch('scripts.install.os.replace', side_effect=OSError('simulated failure')):
            with self.assertRaises(OSError):
                self.apply(digest(b'old'))
        self.assertEqual(target.read_bytes(), b'old')
        self.assertEqual(next((self.home / 'backups').iterdir()).read_bytes(), b'old')
        self.assertFalse((self.home / '.agent-playbook-install.lock').exists())
        self.assertFalse(list(self.home.glob('.AGENTS-*')))

    def test_cooperative_lock_blocks_second_installer(self):
        self.home.mkdir(parents=True)
        lock = self.home / '.agent-playbook-install.lock'
        lock.write_text('another installer')
        with self.assertRaises(FileExistsError):
            self.apply()
        self.assertEqual(lock.read_text(), 'another installer')
        self.assertFalse((self.home / 'AGENTS.md').exists())

    def test_git_reads_committed_bytes_and_rejects_dirty_source(self):
        repo = Path(self.temp.name) / 'repo 空白'
        repo.mkdir()
        def git(*args):
            return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.STDOUT)
        git('init')
        git('config', 'core.autocrlf', 'false')
        for name, data in self.data.items():
            path = repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        (repo / 'scripts').mkdir()
        (repo / 'scripts/install.py').write_bytes((Path(__file__).resolve().parents[1] / 'scripts/install.py').read_bytes())
        (repo / 'extra.py').write_text('# excluded from document snapshot\n')
        git('add', '.')
        git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-m', 'fixture')
        commit = git('rev-parse', 'HEAD').decode().strip()
        self.assertEqual(payload_at(repo, commit), self.data)
        git('update-ref', 'refs/remotes/origin/main', commit)
        import json
        import sys
        command = [sys.executable, str(repo / 'scripts/install.py'), '--commit', commit,
                   '--codex-home', str(self.home)]
        preview = json.loads(subprocess.check_output(command, cwd=self.temp.name))
        self.assertEqual(preview['current_sha256'], 'missing')
        self.assertFalse(self.home.exists())
        applied = json.loads(subprocess.check_output(command + ['--apply', '--expect-current-sha256', 'missing'], cwd=self.temp.name))
        self.assertTrue(applied['verified'])
        self.assertEqual(applied['source_commit'], commit)
        (repo / 'extra.py').write_text('# changed\n')
        with self.assertRaises(ValueError):
            payload_at(repo, commit)


if __name__ == '__main__':
    unittest.main()
