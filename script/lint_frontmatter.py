"""Lint Hugo content frontmatter for the rules in .claude/skills/rules-that-must-be-followed.

Hard-fails only on newly ADDED content files, for the two unambiguous
numeric rules (title length, tag count). Everything else (description
length tolerance, changes to pre-existing files) is warning-only, since
a large share of historical content predates these rules and a hard gate
there would block unrelated edits.

Usage: python script/lint_frontmatter.py <base-ref>
"""
import re
import subprocess
import sys
from pathlib import Path

import yaml

TITLE_MAX = 70
DESC_MIN = 120
DESC_MAX = 170
TAGS_MIN = 25

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
TITLE_RE = re.compile(r'^title:\s*"?(.*?)"?\s*$', re.MULTILINE)
DESC_RE = re.compile(r'^description:\s*"?(.*?)"?\s*$', re.MULTILINE)
TAG_ITEM_RE = re.compile(r"^\s*-\s*(.+?)\s*$")


def _norm_tag(t: str) -> str:
    return t.lower().replace("-", "").replace("_", "").replace(" ", "")


def load_approved_tag_index(repo_root: Path):
    """Map normalized(tag) -> approved canonical spelling, from data/tags.yaml."""
    tags_yaml = repo_root / "data" / "tags.yaml"
    if not tags_yaml.exists():
        return {}
    data = yaml.safe_load(tags_yaml.read_text(encoding="utf-8")) or {}
    index = {}
    for category, tags in data.items():
        if not isinstance(tags, list):
            continue
        for t in tags:
            index.setdefault(_norm_tag(str(t)), str(t))
    return index


def extract_tag_lines(frontmatter: str):
    m = re.search(r"^tags:\s*\n((?:^\s*-.*\n?)+)", frontmatter, re.MULTILINE)
    if not m:
        return []
    tags = []
    for line in m.group(1).splitlines():
        tm = TAG_ITEM_RE.match(line)
        if tm:
            tags.append(tm.group(1).strip("'\""))
    return tags


def get_changed_files(base_ref: str):
    diff = subprocess.run(
        ["git", "diff", "--name-status", base_ref, "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    added, modified = [], []
    for line in diff.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status, path = parts[0], parts[-1]
        if not (path.startswith("content/") and path.endswith(".md")):
            continue
        (added if status.startswith("A") else modified).append(path)
    return added, modified


def check(path_str: str, approved_index: dict):
    text = Path(path_str).read_text(encoding="utf-8", errors="ignore")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None  # not a frontmatter page (e.g. _index.md section-only), skip
    fm = m.group(1)

    errors, warnings = [], []

    title_m = TITLE_RE.search(fm)
    title = title_m.group(1) if title_m else ""
    if len(title) > TITLE_MAX:
        errors.append(f"title {len(title)}자 (>{TITLE_MAX}자, rules-that-must-be-followed §1)")

    desc_m = DESC_RE.search(fm)
    desc = desc_m.group(1) if desc_m else ""
    if desc and not (DESC_MIN <= len(desc) <= DESC_MAX):
        warnings.append(f"description {len(desc)}자 (권장 {DESC_MIN}~{DESC_MAX}자)")

    tags = extract_tag_lines(fm)
    if "tags:" in fm and len(tags) < TAGS_MIN:
        errors.append(f"tags {len(tags)}개 (<{TAGS_MIN}개, rules-that-must-be-followed §1)")

    for t in tags:
        canonical = approved_index.get(_norm_tag(t))
        if canonical and canonical != t:
            errors.append(
                f"태그 표기 불일치: '{t}' 대신 승인 태그 '{canonical}' 사용 "
                f"(data/tags.yaml, tag-consolidation-plan.md Phase 1/2)"
            )

    return errors, warnings


def main():
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    added, modified = get_changed_files(base_ref)
    approved_index = load_approved_tag_index(Path.cwd())

    hard_fail = False

    for path in added:
        result = check(path, approved_index)
        if result is None:
            continue
        errors, warnings = result
        for e in errors:
            hard_fail = True
            print(f"::error file={path}::{e}")
        for w in warnings:
            print(f"::warning file={path}::{w}")

    for path in modified:
        result = check(path, approved_index)
        if result is None:
            continue
        errors, warnings = result
        for msg in errors + warnings:
            print(f"::warning file={path}::{msg} (기존 글 수정 — 경고만, 신규 글만 강제)")

    if hard_fail:
        print("\n신규 콘텐츠 파일의 frontmatter가 필수 규칙(title<=70자, tags>=25개)을 위반했습니다.")
        sys.exit(1)

    print(f"frontmatter 린트 통과 (added={len(added)}, modified={len(modified)}).")


if __name__ == "__main__":
    main()
