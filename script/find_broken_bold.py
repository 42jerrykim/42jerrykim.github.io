"""Find (and optionally fix) **bold** spans that CommonMark will NOT render as <strong>.

Root cause: per the CommonMark emphasis "right-flanking" rule, a closing
`**` immediately preceded by Unicode punctuation and immediately followed by
a non-whitespace, non-punctuation character (e.g. a Korean particle glued
directly onto a term ending in ')', '"', etc. with no space) is not a valid
closing delimiter. goldmark (this site's renderer) follows the spec exactly,
so the `**` are left as literal asterisks instead of becoming <strong>
(confirmed against this site's actual built HTML -- see
rules-that-must-be-followed skill).

The fix is mechanical and always safe: rewrap the exact matched span as
`<strong>...</strong>` raw HTML (this site's goldmark config has
`unsafe = true`, so raw HTML passes through). This bypasses CommonMark's
delimiter-flanking parsing entirely and renders identically to a working
`**...**` span. Spans that already render fine are left untouched.

Usage:
  python script/find_broken_bold.py --dry-run <glob...>
  python script/find_broken_bold.py <glob...>
"""
import re
import sys
import glob as globmod
import unicodedata

FENCE_RE = re.compile(r'^\s*(```|~~~)')
INLINE_CODE_RE = re.compile(r'`[^`\n]*`')
BOLD_RE = re.compile(r'\*\*([^*\n]+?)\*\*')


def is_punct(ch):
    return unicodedata.category(ch).startswith('P')


def is_broken(content, after):
    if not content:
        return False
    before = content[-1]
    return bool(is_punct(before) and after and not after.isspace() and not is_punct(after))


def process_line(line):
    protected = INLINE_CODE_RE.sub(lambda m: 'X' * len(m.group(0)), line)
    matches = list(BOLD_RE.finditer(protected))
    if not matches:
        return line, []

    hits = []
    edits = []  # (start, end, replacement)
    for m in matches:
        content = m.group(1)
        end = m.end()
        after = protected[end] if end < len(protected) else ''
        if is_broken(content, after):
            s = max(0, m.start() - 12)
            hits.append(line[s:m.end() + 12].strip())
            original_content = line[m.start() + 2:m.end() - 2]
            edits.append((m.start(), m.end(), f'<strong>{original_content}</strong>'))

    if not edits:
        return line, []

    out = line
    for start, end, repl in reversed(edits):
        out = out[:start] + repl + out[end:]
    return out, hits


def process_file(path, dry_run):
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    in_fence = False
    hits = []
    out_lines = []
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue
        new_line, line_hits = process_line(line)
        hits.extend(line_hits)
        out_lines.append(new_line)

    if hits and not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(out_lines)
    return hits


def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    patterns = [a for a in args if a != '--dry-run']
    files = set()
    for p in patterns:
        files.update(globmod.glob(p, recursive=True))

    grand_total = 0
    touched_files = 0
    for path in sorted(files):
        hits = process_file(path, dry_run)
        if hits:
            grand_total += len(hits)
            touched_files += 1
            print(f'{"[dry] " if dry_run else ""}{path}: {len(hits)}')

    print(f'\n{touched_files} files, {grand_total} broken bold span(s) total')


if __name__ == '__main__':
    main()
