#!/usr/bin/env python3
"""Dependency-free structural validation for the Agent Skills repository."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"!?[[][^]]*[]][(]([^)]+)[)]")
EXPECTED_SKILLS = {"implicit-state-machines", "vibe-refactor-protocol"}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)} must begin with YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) != 3:
        fail(f"{path.relative_to(ROOT)} has unclosed YAML frontmatter")
    fields: dict[str, str] = {}
    for line in parts[1].splitlines():
        stripped = line.strip()
        if not stripped or line[:1].isspace() or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            fail(f"invalid frontmatter line in {path.relative_to(ROOT)}: {line}")
        key, value = stripped.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields, parts[2]


def check_links(path: Path, body: str) -> None:
    for raw in LINK_RE.findall(body):
        target = raw.strip().split(" ", 1)[0].split("#", 1)[0]
        if not target or target.startswith(("https://", "http://", "mailto:")):
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"link escapes repository in {path.relative_to(ROOT)}: {raw}")
        if not resolved.exists():
            fail(f"broken local link in {path.relative_to(ROOT)}: {raw}")


def main() -> int:
    if not SKILLS_DIR.is_dir():
        fail("skills/ directory is missing")
    found = {
        p.name for p in SKILLS_DIR.iterdir()
        if p.is_dir() and (p / "SKILL.md").is_file()
    }
    if found != EXPECTED_SKILLS:
        fail(f"expected skills {sorted(EXPECTED_SKILLS)}, found {sorted(found)}")

    for skill_name in sorted(found):
        skill_file = SKILLS_DIR / skill_name / "SKILL.md"
        fields, body = parse_frontmatter(skill_file)
        if not {"name", "description"}.issubset(fields):
            fail(f"{skill_file.relative_to(ROOT)} needs name and description")
        if fields["name"] != skill_name or not NAME_RE.fullmatch(fields["name"]):
            fail(f"invalid skill name/folder match in {skill_file.relative_to(ROOT)}")
        if not fields["description"] or len(fields["description"]) > 1024:
            fail(f"description missing or exceeds 1024 characters in {skill_name}")
        check_links(skill_file, body)
        print(f"PASS: {skill_name}")

    for path in [
        ROOT / "README.md",
        *sorted((ROOT / "docs").glob("*.md")),
        ROOT / "CONTRIBUTING.md",
        ROOT / "PUBLISHING.md",
    ]:
        if path.is_file():
            check_links(path, path.read_text(encoding="utf-8"))

    required = [
        ROOT / "LICENSE",
        ROOT / "README.md",
        ROOT / ".github/workflows/validate.yml",
        ROOT / "skills/implicit-state-machines/references/detection-signals.md",
        ROOT / "skills/vibe-refactor-protocol/SKILL.md",
        ROOT / "prompts/vibe-refactor-protocol.md",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    if missing:
        fail("required files missing: " + ", ".join(missing))

    print("PASS: local Markdown links and required repository files")
    print("PASS: repository validation complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
