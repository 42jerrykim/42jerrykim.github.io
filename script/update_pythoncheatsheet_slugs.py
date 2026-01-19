#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


STOPWORDS = {
    "python",
    "python3",
    "cheatsheet",
    "quick-reference",
    "quickreference",
    "standard-library",
    "best-practices",
    "pitfalls",
}


@dataclass(frozen=True)
class Frontmatter:
    title: str | None
    collection_order: int | None
    tags: list[str]


def detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def split_frontmatter(text: str) -> tuple[str | None, str]:
    # legacy stub (unused) kept intentionally empty
    return None, text


FRONTMATTER_BLOCK_RE = re.compile(r"(?s)\A---\s*\r?\n(.*?)\r?\n---\s*\r?\n")


def extract_frontmatter(text: str) -> tuple[str | None, str]:
    m = FRONTMATTER_BLOCK_RE.match(text)
    if not m:
        return None, text
    fm = m.group(1)
    body = text[m.end() :]
    return fm, body


def parse_frontmatter(fm: str) -> Frontmatter:
    title: str | None = None
    collection_order: int | None = None
    tags: list[str] = []

    lines = fm.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("title:"):
            m = re.match(r'^title:\s*"(.*)"\s*$', line)
            if m:
                title = m.group(1)
            else:
                title = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("collection_order:"):
            m = re.match(r"^collection_order:\s*(\d+)\s*$", line)
            if m:
                collection_order = int(m.group(1))
        elif line.startswith("tags:"):
            i += 1
            while i < len(lines):
                tline = lines[i]
                if re.match(r"^\S", tline):
                    i -= 1
                    break
                m = re.match(r"^\s*-\s*(.+?)\s*$", tline)
                if m:
                    tags.append(m.group(1).strip().strip('"'))
                i += 1
        i += 1

    return Frontmatter(title=title, collection_order=collection_order, tags=tags)


def slugify_ascii(s: str) -> str:
    s = s.strip().lower()
    s = s.replace("&", " and ")
    s = s.replace("’", "'")
    s = re.sub(r"[']", "", s)
    s = s.replace(".", " ")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s


def base_from_title(title: str) -> str:
    t = title.strip()
    t = re.sub(r"^\[[^\]]+\]\s*", "", t)  # [Python Cheatsheet]
    t = re.sub(r"^\d{1,3}\.\s*", "", t)  # 67.
    left = t.split(" - ", 1)[0].strip()
    return slugify_ascii(left)


def base_from_dir(dirname: str) -> str:
    name = re.sub(r"^\d{2}_", "", dirname)
    name = name.replace("_", " ")
    return slugify_ascii(name)


def pick_keywords(tags: list[str]) -> list[str]:
    out: list[str] = []
    for t in tags:
        t = t.strip()
        if not t:
            continue
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", t):
            continue
        k = slugify_ascii(t)
        if not k or k in STOPWORDS:
            continue
        if k not in out:
            out.append(k)
    return out


def build_slug(fm: Frontmatter, dirname: str, used: set[str]) -> str:
    base = base_from_title(fm.title) if fm.title else ""

    # If base too short, enrich with directory hint
    if not base or len(base) < 10:
        dbase = base_from_dir(dirname)
        if dbase and dbase not in base:
            base = "-".join([p for p in [base, dbase] if p]).strip("-")

    if not base:
        base = base_from_dir(dirname) or slugify_ascii(dirname)

    base_tokens = set(base.split("-"))

    extras: list[str] = []
    for k in pick_keywords(fm.tags):
        if not k:
            continue
        if k == base:
            continue
        k_tokens = set(k.split("-"))
        # skip keywords already covered by the base tokens (prevents duplicates like control-flow-control-flow)
        if k_tokens.issubset(base_tokens):
            continue
        extras.append(k)

    cur = base
    for k in extras:
        cur_tokens = set(cur.split("-"))
        k_tokens = set(k.split("-"))
        if k_tokens.issubset(cur_tokens):
            continue
        cand = f"{cur}-{k}"
        if len(cand) <= 70:
            cur = cand

    # ensure uniqueness
    slug = cur[:70].rstrip("-")
    if slug in used:
        suffix = str(fm.collection_order) if fm.collection_order is not None else "2"
        base2 = slug
        if len(base2) + 1 + len(suffix) > 70:
            base2 = base2[: max(1, 70 - (1 + len(suffix)))].rstrip("-")
        slug = f"{base2}-{suffix}"
        n = 2
        while slug in used:
            inc = str(n)
            base3 = base2
            if len(base3) + 1 + len(inc) > 70:
                base3 = base3[: max(1, 70 - (1 + len(inc)))].rstrip("-")
            slug = f"{base3}-{inc}"
            n += 1

    used.add(slug)
    return slug


def upsert_slug(fm_text: str, slug: str) -> str:
    lines = fm_text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("slug:"):
            lines[i] = f'slug: "{slug}"'
            return "\n".join(lines)

    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("title:"):
            insert_at = i + 1
            break
        if line.startswith("image:") or line.startswith("featured_image:"):
            insert_at = i + 1

    lines.insert(insert_at, f'slug: "{slug}"')
    return "\n".join(lines)


SIBLING_LINK_RE = re.compile(r"\]\((?:\.\./)?(\d{2}_[A-Za-z0-9_]+?)/\)")


def rewrite_links(body: str) -> tuple[str, int]:
    def repl(m: re.Match) -> str:
        d = m.group(1)
        return f']({{{{< relref "collection/pythoncheatsheet/{d}/index.md" >}}}})'

    return SIBLING_LINK_RE.subn(repl, body)


def process_leaf(path: Path, used: set[str], dry_run: bool) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    nl = detect_newline(text)

    fm, body = extract_frontmatter(text)
    if fm is None:
        return False, f"SKIP(no frontmatter): {path}"

    info = parse_frontmatter(fm)
    slug = build_slug(info, path.parent.name, used)
    new_fm = upsert_slug(fm, slug)
    new_body, n_links = rewrite_links(body)
    new_text = f"---\n{new_fm}\n---\n{new_body}"
    new_text = new_text.replace("\n", nl)

    changed = new_text != text
    if changed and not dry_run:
        path.write_text(new_text, encoding="utf-8")

    return changed, f"{'CHANGED' if changed else 'OK'} slug={slug} links={n_links} {path}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="content/collection/pythoncheatsheet")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.exists():
        raise SystemExit(f"root not found: {root}")

    used: set[str] = set()
    touched = 0
    changed = 0

    for p in sorted(root.glob("*/index.md")):
        touched += 1
        c, msg = process_leaf(p, used, args.dry_run)
        if c:
            changed += 1
        print(msg)

    print(f"Touched: {touched}, Changed: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

