"""Zip each skill folder in agensi/ into dist/agensi/<skill>.zip for upload to Agensi.

Each zip holds one top-level folder named after the skill with SKILL.md at its root.
Standard library only.
"""
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "dist" / "agensi"
SKIP_NAMES = {".DS_Store", "Thumbs.db"}
SKIP_DIRS = {"__pycache__", ".git"}


def frontmatter_name(skill_md: Path) -> str:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{skill_md}: missing frontmatter")
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    raise ValueError(f"{skill_md}: no name in frontmatter")


def package(skill_dir: Path) -> Path:
    name = frontmatter_name(skill_dir / "SKILL.md")
    if name != skill_dir.name:
        raise ValueError(f"{skill_dir}: folder name must equal frontmatter name '{name}'")
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / f"{name}.zip"
    files = sorted(
        p for p in skill_dir.rglob("*")
        if p.is_file() and p.name not in SKIP_NAMES and not SKIP_DIRS.intersection(p.parts)
    )
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in files:
            zf.write(p, f"{name}/{p.relative_to(skill_dir).as_posix()}")
    print(f"{target.relative_to(HERE.parent)}  ({len(files)} files)")
    return target


def main() -> int:
    skills = [d for d in sorted(HERE.iterdir()) if (d / "SKILL.md").is_file()]
    if not skills:
        print("no skill folders found", file=sys.stderr)
        return 1
    for d in skills:
        package(d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
