"""Remove self-referential 'headword + meaning/usage/examples/...' compound tags
from content/collection/Vocabulary posts (see tag-consolidation-plan.md, Vocabulary
long-tail cleanup). These tags embed that post's own headword plus a fixed suffix
(e.g. "track meaning", "track 의미") and can never recur on another post by
construction -- they add tag-list length without any connecting value.

For posts that would drop below the 25-tag minimum after removal, backfills with
unused approved tags (data/tags.yaml, english_vocabulary category) to stay >=25.

Usage:
    python script/clean_vocabulary_noise_tags.py [--apply]
"""
import argparse
import glob
import re

import yaml

NOISE_SUFFIXES = ["meaning", "usage", "examples", "noun", "verb", "adjective", "adverb"]
NOISE_SUFFIXES_KO = ["의미", "용법", "예문"]

TAG_LINE_RE = re.compile(r"^([ ]*)-[ ]?(.*?)[ \t]*\r?$")
TAGS_KEY_RE = re.compile(r"^tags:\s*\r?$")

TAGS_MIN = 25


def strip_quotes(v: str):
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        return v[1:-1]
    return v


def is_noise(tag: str) -> bool:
    if " " not in tag:
        return False
    prefix, _, last = tag.rpartition(" ")
    if not prefix:
        return False
    if last.lower() in NOISE_SUFFIXES:
        return True
    if last in NOISE_SUFFIXES_KO:
        return True
    return False


POS_SPECIFIC_TAGS = {"영어동사", "영어명사", "영어형용사", "영어부사"}


def load_backfill_pool(repo_root):
    with open(repo_root + "/data/tags.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    pool = [t for t in data.get("english_vocabulary", []) if t not in POS_SPECIFIC_TAGS]
    return pool


def process_file(path, backfill_pool):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    if not lines or lines[0].strip() != "---":
        return None
    fm_end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm_end = i
            break
    if fm_end is None:
        return None

    tags_start = None
    for i in range(1, fm_end):
        if TAGS_KEY_RE.match(lines[i]):
            tags_start = i + 1
            break
    if tags_start is None:
        return None

    block_end = tags_start
    indent = None
    items = []
    while block_end < fm_end:
        m = TAG_LINE_RE.match(lines[block_end])
        if not m:
            break
        this_indent = m.group(1)
        if indent is None:
            indent = this_indent
        elif this_indent != indent:
            break
        value = strip_quotes(m.group(2))
        items.append(value)
        block_end += 1

    if not items:
        return None

    kept = [t for t in items if not is_noise(t)]
    removed_count = len(items) - len(kept)
    if removed_count == 0:
        return None

    existing = set(kept)
    if len(kept) < TAGS_MIN:
        for candidate in backfill_pool:
            if len(kept) >= TAGS_MIN:
                break
            if candidate not in existing:
                kept.append(candidate)
                existing.add(candidate)

    new_lines_for_block = [f"{indent}- {t}\n" for t in kept]
    new_lines = lines[:tags_start] + new_lines_for_block + lines[block_end:]
    return new_lines, len(items), len(kept), removed_count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    backfill_pool = load_backfill_pool(".")
    files = glob.glob("content/collection/Vocabulary/**/*index.md", recursive=True)

    changed_files = 0
    total_removed = 0
    below_50_fixed = 0

    for path in files:
        result = process_file(path, backfill_pool)
        if result is None:
            continue
        new_lines, before_count, after_count, removed_count = result
        changed_files += 1
        total_removed += removed_count
        if before_count - removed_count < TAGS_MIN <= after_count:
            below_50_fixed += 1
        if args.apply:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.writelines(new_lines)

    mode = "APPLIED" if args.apply else "DRY-RUN"
    print(f"[{mode}] files changed: {changed_files}")
    print(f"noise tags removed: {total_removed}")
    print(f"posts backfilled to stay >=50: {below_50_fixed}")


if __name__ == "__main__":
    main()
