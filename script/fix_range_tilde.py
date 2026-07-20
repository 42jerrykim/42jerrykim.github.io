"""Replace prose range tildes (e.g. 1만~10만, 0.2~0.4) with en dash (–).

Skips fenced code blocks (``` / ~~~) and inline code spans (`...`), since
tildes there (shell paths, code) must not be touched. Only touches a tilde
that has a digit directly adjacent on at least one side (optionally with a
Korean syllable on the other side), which is the pattern that triggers the
strikethrough bug in lenient markdown readers (see rules-that-must-be-followed
skill, section 9).

Usage:
  python script/fix_range_tilde.py --dry-run <glob...>
  python script/fix_range_tilde.py <glob...>
"""
import re
import sys
import glob as globmod

RANGE_TILDE = re.compile(
    r'(?<=[0-9])~(?=[0-9])'
    r'|(?<=[0-9])~(?=[가-힣])'
    r'|(?<=[가-힣])~(?=[0-9])'
)

FENCE_RE = re.compile(r'^\s*(```|~~~)')
INLINE_CODE_RE = re.compile(r'`[^`\n]*`')


def process_line(line):
    if not RANGE_TILDE.search(line):
        return line, 0
    # protect inline code spans
    spans = []
    def protect(m):
        spans.append(m.group(0))
        return f'\x00{len(spans)-1}\x00'
    protected = INLINE_CODE_RE.sub(protect, line)
    count = len(RANGE_TILDE.findall(protected))
    replaced = RANGE_TILDE.sub('–', protected)
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
