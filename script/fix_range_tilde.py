"""Replace prose range tildes (e.g. 1만~10만, 0.2~0.4, 초급~중급, A~Z, D0~D31)
with en dash (–).

Skips fenced code blocks (``` / ~~~) and inline code spans (`...`), since
tildes there (shell paths, code) must not be touched. Touches a tilde that
has a "word-like" Unicode character (Unicode category L* letter or N*
number -- covers digits, Latin letters, Korean syllables, Greek/micro signs,
etc.) directly adjacent on BOTH sides. This is the GFM tilde-strikethrough
delimiter pattern that goldmark (this site's Hugo markdown renderer) actually
parses as `<del>`, confirmed by inspecting the live rendered HTML (see
rules-that-must-be-followed skill, section 9). An earlier version of this
script only checked digit/Korean adjacency and missed Latin-letter cases
like "S~E", "A~Z", "D0~D31", "1µs~1시간" -- verified still
broken in production HTML after the first pass, hence the Unicode-category
generalization here.

Usage:
  python script/fix_range_tilde.py --dry-run <glob...>
  python script/fix_range_tilde.py <glob...>
"""
import re
import sys
import glob as globmod
import unicodedata

FENCE_RE = re.compile(r'^\s*(```|~~~)')
INLINE_CODE_RE = re.compile(r'`[^`\n]*`')
TILDE_RE = re.compile(r'~')


def is_wordlike(ch):
    return unicodedata.category(ch)[0] in ('L', 'N')


def process_line(line):
    if '~' not in line:
        return line, 0
    # protect inline code spans
    spans = []

    def protect(m):
        spans.append(m.group(0))
        return f'\x00{len(spans) - 1}\x00'

    protected = INLINE_CODE_RE.sub(protect, line)

    out_chars = list(protected)
    count = 0
    for m in TILDE_RE.finditer(protected):
        i = m.start()
        before = protected[i - 1] if i > 0 else ''
        after = protected[i + 1] if i + 1 < len(protected) else ''
        if before and after and is_wordlike(before) and is_wordlike(after):
            out_chars[i] = '–'
            count += 1
    replaced = ''.join(out_chars)

    def restore(m):
        return spans[int(m.group(1))]

    restored = re.sub(r'\x00(\d+)\x00', restore, replaced)
    return restored, count


def process_file(path, dry_run):
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()

    in_fence = False
    total = 0
    out = []
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        new_line, count = process_line(line)
        total += count
        out.append(new_line)

    if total and not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(out)
    return total


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
        n = process_file(path, dry_run)
        if n:
            grand_total += n
            touched_files += 1
            print(f'{"[dry] " if dry_run else ""}{path}: {n} replacement(s)')

    print(f'\n{touched_files} files, {grand_total} replacements total')


if __name__ == '__main__':
    main()
