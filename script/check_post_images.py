"""Check that newly added posts declare a representative image that exists in the bundle.

Hard-fails only on newly ADDED non-draft post bundles (content/post, content/collection),
since a large share of legacy posts (e.g. Movies posters) predates this rule.
Modified legacy files are reported as warnings only.

Usage: python script/check_post_images.py <base-ref>
Fix: python script/wordcloud_generator.py "<bundle dir>" then add `image: "wordcloud.png"` to the frontmatter.
"""
import re
import subprocess
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
IMAGE_RE = re.compile(r"^\s*image:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)
DRAFT_RE = re.compile(r"^\s*draft:\s*(\w+)", re.MULTILINE)
ZERO_SHA = "0" * 40


def changed_files(base_ref: str):
    if not base_ref or base_ref == ZERO_SHA:
        base_ref = "HEAD^"
    diff = subprocess.run(
        ["git", "diff", "--name-status", base_ref, "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout
    added, modified = [], []
    for line in diff.splitlines():
        parts = line.split("\t")
        if len(parts) < 2 or parts[0].startswith("D"):
            continue
        path = parts[-1]
        if not re.match(r"content/(post|collection)/.+/index\.md$", path):
            continue
        (added if parts[0].startswith("A") else modified).append(path)
    return added, modified


def problem(path_str: str):
    path = Path(path_str)
    m = FRONTMATTER_RE.match(path.read_text(encoding="utf-8", errors="ignore"))
    if not m:
        return None
    fm = m.group(1)
    draft = DRAFT_RE.search(fm)
    if draft and draft.group(1).lower() == "true":
        return None  # drafts are not published
    image = IMAGE_RE.search(fm)
    if not image:
        return "frontmatter에 image 필드 없음 (대표 이미지 필수)"
    name = image.group(1)
    if name.startswith(("http", "/")):
        return None
    if not (path.parent / name).exists():
        return f"image 파일 없음: {name}"
    return None


def main():
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "HEAD^"
    added, modified = changed_files(base_ref)
    failed = False
    for p in added:
        msg = problem(p)
        if msg:
            failed = True
            print(f"::error file={p}::{msg} — python script/wordcloud_generator.py <번들 경로> 후 image: \"wordcloud.png\" 추가")
    for p in modified:
        msg = problem(p)
        if msg:
            print(f"::warning file={p}::{msg} (기존 글 수정 — 경고만)")
    if failed:
        sys.exit(1)
    print(f"대표 이미지 검사 통과 (added={len(added)}, modified={len(modified)}).")


if __name__ == "__main__":
    main()
