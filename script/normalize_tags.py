"""Normalize casing/format variants of frontmatter tags to their approved canonical
form (data/tags.yaml), per tag-consolidation-plan.md Phase 1.

Only rewrites tag list items that exactly match a key in TAG_MAPPING. Leaves every
other line (title, description, unrelated tags, quoting style) untouched. After
mapping, removes duplicate tag lines that result from the merge, keeping the first
occurrence's position.

Usage:
    python script/normalize_tags.py --mapping <mapping.json> [--apply]

Without --apply, prints a dry-run summary (files that would change, tag counts).
"""
import argparse
import glob
import json
import re

TAG_LINE_RE = re.compile(r"^([ ]*)-[ ]?(.*?)[ \t]*\r?$")
TAGS_KEY_RE = re.compile(r"^tags:\s*\r?$")


def strip_quotes(v: str):
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        return v[1:-1]
    return v


def process_file(path: str, mapping: dict):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    # locate frontmatter (--- ... ---)
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

    # collect contiguous list items
    block_end = tags_start
    indent = None
    items = []  # (line_index, raw_line, value)
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
        items.append([block_end, lines[block_end], value])
        block_end += 1

    if not items:
        return None

    changed = False
    seen = set()
    new_lines_for_block = []
    for idx, raw, value in items:
        mapped = mapping.get(value, value)
        if mapped != value:
            changed = True
        if mapped in seen:
            changed = True
            continue  # drop duplicate
        seen.add(mapped)
        if mapped != value:
            new_line = f"{indent}- {mapped}\n"
        else:
            new_line = raw
        new_lines_for_block.append(new_line)

    if not changed:
        return None

    new_lines = lines[:tags_start] + new_lines_for_block + lines[block_end:]
    return new_lines, len(items), len(new_lines_for_block)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mapping", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    with open(args.mapping, encoding="utf-8") as f:
        mapping = json.load(f)

    files = glob.glob("content/**/index.md", recursive=True)
    changed_files = 0
    total_before = 0
    total_after = 0

    for path in files:
        result = process_file(path, mapping)
        if result is None:
            continue
        new_lines, before_count, after_count = result
        changed_files += 1
        total_before += before_count
        total_after += after_count
        if args.apply:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.writelines(new_lines)

    mode = "APPLIED" if args.apply else "DRY-RUN"
    print(f"[{mode}] files changed: {changed_files}")
    print(f"tag lines before: {total_before}, after: {total_after} (removed {total_before - total_after} duplicate lines)")


if __name__ == "__main__":
    main()
