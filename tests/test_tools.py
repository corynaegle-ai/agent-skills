"""Behavioral tests for installation safety and complete pre-commit review capture."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load("installer", ROOT / "scripts/install-skills.py")
review = load("review", ROOT / "skills/engineering/code-review/scripts/review-snapshot.py")


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skill-install-test-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.destination = self.directory / "agent" / "skills"
        self.skills = installer.catalog()

    def install(self, *destinations, dry_run=False, names=None):
        with contextlib.redirect_stdout(io.StringIO()):
            installer.install(names or ["diagnosing-bugs"], self.skills,
                              destinations or [self.destination], dry_run)

    def test_install_and_repeat_preserve_source_and_link(self):
        self.install()
        link = self.destination / "diagnosing-bugs"
        before = link.lstat()
        self.assertEqual(link.resolve(), self.skills["diagnosing-bugs"])
        self.install()
        self.assertEqual(link.lstat().st_ino, before.st_ino)

    def test_dry_run_creates_no_directories(self):
        self.install(dry_run=True)
        self.assertFalse(self.destination.parent.exists())

    def test_existing_directory_is_preserved_and_entire_plan_aborts(self):
        target = self.destination / "diagnosing-bugs"
        target.mkdir(parents=True)
        marker = target / "custom.md"
        marker.write_text("user-owned")
        other = self.directory / "other-agent"
        with self.assertRaises(ValueError):
            self.install(other, self.destination)
        self.assertEqual(marker.read_text(), "user-owned")
        self.assertFalse(other.exists())

    def test_existing_regular_file_is_preserved(self):
        self.destination.mkdir(parents=True)
        target = self.destination / "diagnosing-bugs"
        target.write_text("custom skill")
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(target.read_text(), "custom skill")

    def test_unrelated_and_broken_symlinks_are_preserved(self):
        self.destination.mkdir(parents=True)
        target = self.destination / "diagnosing-bugs"
        for source in (self.directory, self.directory / "missing"):
            target.symlink_to(source)
            with self.assertRaises(ValueError):
                self.install()
            self.assertEqual(os.readlink(target), str(source))
            target.unlink()

    def test_symlinked_destination_is_rejected(self):
        destination = self.directory / "redirect"
        destination.symlink_to(self.directory)
        with self.assertRaises(ValueError):
            self.install(destination)
        self.assertFalse((self.directory / "diagnosing-bugs").exists())

    def test_destination_inside_source_repo_is_rejected(self):
        with self.assertRaises(ValueError):
            self.install(ROOT / "skills" / "never-create")
        self.assertFalse((ROOT / "skills" / "never-create").exists())

    def test_dependency_closure_for_architecture_and_implementation(self):
        deps = json.loads((ROOT / "skills.json").read_text())["dependencies"]
        names = installer.select_skills(self.skills, ["improve-codebase-architecture"], deps)
        self.assertEqual(set(names), {"improve-codebase-architecture", "grilling", "domain-modeling", "codebase-design"})
        names = installer.select_skills(self.skills, ["implement-spec"], deps)
        self.assertEqual(set(names), {"implement-spec", "tdd", "code-review", "codebase-design", "pr"})

    def test_recommended_and_full_selection_exclude_experiments(self):
        config = json.loads((ROOT / "skills.json").read_text())
        names = installer.select_skills(self.skills, config["recommended"], config["dependencies"])
        self.assertEqual(len(names), 6)
        self.assertEqual(len(self.skills), 27)
        self.assertNotIn("loop-me", self.skills)
        self.assertNotIn("setup-pre-commit", self.skills)

    def test_invalid_skill_and_dependency_cycle_fail(self):
        for name, deps in (("../outside", {}), ("retro", {"retro": ["retro"]})):
            with self.assertRaises(ValueError):
                installer.select_skills(self.skills, [name], deps)

    def test_cli_custom_destination_works_from_another_directory(self):
        result = subprocess.run(["bash", str(ROOT / "scripts/link-skills.sh"),
                                 "--skill", "pr", "--destination", str(self.destination)],
                                cwd=self.directory, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.destination / "pr" / "SKILL.md").is_file())


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skill-review-test-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.repo = self.directory / "project"
        self.repo.mkdir()
        self.git("init", "-q")
        (self.repo / "tracked.txt").write_text("baseline\n")
        (self.repo / ".gitignore").write_text(".env\n")
        self.git("add", ".")
        self.commit("baseline")
        self.base = self.git("rev-parse", "HEAD").strip()

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, stderr=subprocess.DEVNULL, text=True)

    def commit(self, message):
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", message)

    def snapshot(self, **kwargs):
        return review.snapshot(cwd=self.repo, output=self.directory / "snapshot", **kwargs)

    def test_precommit_capture_includes_staged_unstaged_and_untracked(self):
        (self.repo / "tracked.txt").write_text("staged content\n")
        self.git("add", "tracked.txt")
        (self.repo / "tracked.txt").write_text("unstaged content\n")
        (self.repo / "new file.txt").write_bytes(b"new content without newline")
        (self.repo / ".env").write_text("ignored fixture")
        index_before = (self.repo / ".git/index").read_bytes()
        before = self.git("status", "--porcelain")
        output = self.snapshot()
        self.assertIn("staged content", (output / "staged.patch").read_text())
        self.assertIn("unstaged content", (output / "unstaged.patch").read_text())
        self.assertIn("unstaged content", (output / "combined.patch").read_text())
        metadata = json.loads((output / "summary.json").read_text())
        self.assertEqual([x["path"] for x in metadata["untracked"]], ["new file.txt"])
        self.assertEqual((output / metadata["untracked"][0]["artifact"]).read_bytes(), b"new content without newline")
        self.assertEqual(index_before, (self.repo / ".git/index").read_bytes())
        self.assertEqual(before, self.git("status", "--porcelain"))

    def test_branch_scope_excludes_dirty_work_and_uses_merge_base(self):
        self.git("checkout", "-qb", "feature")
        (self.repo / "tracked.txt").write_text("committed change\n")
        self.git("add", "."); self.commit("feature")
        (self.repo / "tracked.txt").write_text("dirty change\n")
        (self.repo / "untracked.txt").write_text("not in branch")
        output = self.snapshot(base=self.base, scope="branch")
        patch = (output / "committed.patch").read_text()
        self.assertIn("committed change", patch)
        self.assertNotIn("dirty change", patch)
        self.assertFalse((output / "staged.patch").exists())
        self.assertEqual(json.loads((output / "summary.json").read_text())["merge_base"], self.base)

    def test_staged_change_reversed_in_worktree_remains_visible(self):
        (self.repo / "tracked.txt").write_text("staged only\n")
        self.git("add", "tracked.txt")
        (self.repo / "tracked.txt").write_text("baseline\n")
        output = self.snapshot()
        self.assertEqual((output / "combined.patch").read_bytes(), b"")
        self.assertIn("staged only", (output / "staged.patch").read_text())
        self.assertIn("staged only", (output / "unstaged.patch").read_text())

    def test_scope_paths_preserve_unrelated_work(self):
        (self.repo / "tracked.txt").write_text("unrelated edit\n")
        (self.repo / "owned.txt").write_text("owned edit\n")
        output = self.snapshot(paths=["owned.txt"])
        metadata = json.loads((output / "summary.json").read_text())
        self.assertEqual([x["path"] for x in metadata["untracked"]], ["owned.txt"])
        self.assertEqual((output / "combined.patch").read_bytes(), b"")

    def test_untracked_symlink_does_not_disclose_target_contents(self):
        outside = self.directory / "private.txt"
        outside.write_text("outside sentinel")
        (self.repo / "link").symlink_to(outside)
        output = self.snapshot()
        entry = json.loads((output / "summary.json").read_text())["untracked"][0]
        self.assertEqual(entry["kind"], "symlink")
        self.assertEqual((output / entry["artifact"]).read_text(), str(outside))

    def test_empty_scope_is_observably_empty(self):
        output = self.snapshot()
        self.assertEqual((output / "combined.patch").read_bytes(), b"")
        self.assertEqual(json.loads((output / "summary.json").read_text())["untracked"], [])

    def test_snapshot_rejects_invalid_base_and_repo_output(self):
        with self.assertRaises(ValueError):
            self.snapshot(base="missing-ref")
        with self.assertRaises(ValueError):
            review.snapshot(cwd=self.repo, output=self.repo / "snapshot")
        self.assertFalse((self.repo / "snapshot").exists())

    def test_changed_checkout_rejects_capture_without_output(self):
        real = review.capture
        count = 0

        def mutate(*args):
            nonlocal count
            captured = real(*args)
            count += 1
            if count == 1:
                (self.repo / "tracked.txt").write_text("concurrent writer\n")
            return captured

        with mock.patch.object(review, "capture", side_effect=mutate):
            with self.assertRaises(ValueError):
                self.snapshot()
        self.assertFalse((self.directory / "snapshot").exists())

    def test_snapshot_contents_are_private_on_unix(self):
        output = self.snapshot()
        self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o700)
        for entry in output.iterdir():
            if entry.is_file():
                self.assertEqual(stat.S_IMODE(entry.stat().st_mode), 0o600)

    def test_diverged_target_uses_common_ancestor(self):
        self.git("checkout", "-qb", "feature")
        (self.repo / "tracked.txt").write_text("feature content\n")
        self.git("add", ".")
        self.commit("feature")
        self.git("checkout", "-qb", "target", self.base)
        (self.repo / "target-only.txt").write_text("target content\n")
        self.git("add", ".")
        self.commit("target moves independently")
        self.git("checkout", "-q", "feature")
        output = self.snapshot(base="target", scope="branch")
        self.assertIn("feature content", (output / "committed.patch").read_text())
        self.assertNotIn("target-only", (output / "committed.patch").read_text())
        self.assertEqual(json.loads((output / "summary.json").read_text())["merge_base"], self.base)

    def test_binary_and_deleted_files_are_reviewable(self):
        (self.repo / "tracked.txt").unlink()
        binary = b"\x00\xff\x01binary content"
        (self.repo / "new.bin").write_bytes(binary)
        output = self.snapshot()
        self.assertIn("deleted file mode", (output / "combined.patch").read_text())
        entry = json.loads((output / "summary.json").read_text())["untracked"][0]
        self.assertEqual((output / entry["artifact"]).read_bytes(), binary)

    def test_stat_refresh_does_not_rewrite_the_index(self):
        tracked = self.repo / "tracked.txt"
        original = tracked.stat()
        os.utime(tracked, ns=(original.st_atime_ns, original.st_mtime_ns + 2_000_000_000))
        before = (self.repo / ".git/index").read_bytes()
        self.snapshot()
        self.assertEqual((self.repo / ".git/index").read_bytes(), before)

    def test_existing_output_is_preserved(self):
        output = self.directory / "snapshot"
        output.mkdir()
        (output / "keep.txt").write_text("existing output")
        with self.assertRaises(FileExistsError):
            self.snapshot()
        self.assertEqual((output / "keep.txt").read_text(), "existing output")


if __name__ == "__main__":
    unittest.main()
