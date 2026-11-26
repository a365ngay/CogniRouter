"""Offline tests for the Skill Compass installer. Run: python -m unittest discover -s tests"""
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "installer"))
import compass  # noqa: E402


def run(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        compass.main(list(argv))
    return buf.getvalue()


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.home = Path(tempfile.mkdtemp(prefix="compass-test-"))
        for d in (".claude", ".codex", ".gemini", ".qwen", ".config/opencode"):
            (self.home / d).mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.home, ignore_errors=True)

    def install(self, *extra):
        return run("install", "--home", str(self.home), "--no-upstream", *extra)

    def test_skills_have_frontmatter(self):
        for d in (REPO / "skills").iterdir():
            meta = compass.parse_frontmatter(d / "SKILL.md")
            self.assertEqual(meta.get("name"), d.name, d)
            self.assertTrue(meta.get("description"), d)

    def test_install_all_detected_hosts(self):
        self.install()
        st = json.loads((self.home / ".skill-compass" / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(set(st["hosts"]), {"claude", "codex", "gemini", "qwen", "opencode"})
        for name, e in st["hosts"].items():
            text = Path(e["instructions"]).read_text(encoding="utf-8")
            self.assertIn(compass.MARK_START, text)
            self.assertNotIn("{{", text)
            self.assertTrue((Path(e["skills_dir"]) / "senior-tech-lead" / "SKILL.md").exists(), name)
        self.assertEqual(len(st["hosts"]["claude"]["agents"]), 5)
        self.assertTrue((self.home / ".skill-compass" / "SKILLS_INDEX.md").exists())

    def test_idempotent_and_preserves_user_text(self):
        claude_md = self.home / ".claude" / "CLAUDE.md"
        claude_md.write_text("# Mine\nkeep me\n", encoding="utf-8")
        self.install("--hosts", "claude")
        self.install("--hosts", "claude")
        text = claude_md.read_text(encoding="utf-8")
        self.assertEqual(text.count(compass.MARK_START), 1)
        self.assertTrue(text.startswith("# Mine\nkeep me"))

    def test_unmanaged_skill_is_not_overwritten(self):
        mine = self.home / ".claude" / "skills" / "senior-angular"
        mine.mkdir(parents=True)
        (mine / "SKILL.md").write_text("my own", encoding="utf-8")
        out = self.install("--hosts", "claude")
        self.assertIn("skip claude:senior-angular", out)
        self.assertEqual((mine / "SKILL.md").read_text(encoding="utf-8"), "my own")
        self.install("--hosts", "claude", "--force")
        self.assertNotEqual((mine / "SKILL.md").read_text(encoding="utf-8"), "my own")
        backups = list((self.home / ".skill-compass" / "backups").rglob("senior-angular/SKILL.md"))
        self.assertTrue(backups)

    def test_aliases(self):
        self.install("--hosts", "glm")
        st = json.loads((self.home / ".skill-compass" / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(list(st["hosts"]), ["claude"])

    def test_uninstall_restores(self):
        claude_md = self.home / ".claude" / "CLAUDE.md"
        claude_md.write_text("# Mine\n", encoding="utf-8")
        self.install()
        run("uninstall", "--home", str(self.home), "--purge")
        self.assertEqual(claude_md.read_text(encoding="utf-8").strip(), "# Mine")
        self.assertFalse(any((self.home / ".agents" / "skills").iterdir()))
        self.assertFalse((self.home / ".skill-compass").exists())

    def test_project_mode(self):
        proj = self.home / "repo"
        proj.mkdir()
        self.install("--project", str(proj))
        self.assertIn(compass.MARK_START, (proj / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertIn("@AGENTS.md", (proj / "CLAUDE.md").read_text(encoding="utf-8"))

    def test_export_has_no_local_paths(self):
        out = self.home / "prompt.md"
        run("export", "--home", str(self.home), "--out", str(out), "--with-skills", "senior-tech-lead")
        text = out.read_text(encoding="utf-8")
        self.assertNotIn(str(self.home).replace("\\", "/"), text)
        self.assertIn("senior-tech-lead", text)

    def test_dry_run_writes_nothing(self):
        run("install", "--home", str(self.home), "--no-upstream", "--dry-run")
        self.assertFalse((self.home / ".skill-compass").exists())
        self.assertFalse((self.home / ".claude" / "CLAUDE.md").exists())


if __name__ == "__main__":
    unittest.main()
