"""Phase 8: build the en/ko bilingual-merge tag mapping described in
tag-consolidation-plan.md section 6, and dump it for audit + reuse by
normalize_tags.py and tag_phase8_apply_yaml.py.

Regenerates the same 211-pair classification from data/tags.yaml + actual
frontmatter usage counts, applies the four documented rules, and writes:
  - script/tag_phase8_pairs.json   (full row data, for audit)
  - script/tag_phase8_mapping.json (flat old-tag -> new-tag, for normalize_tags.py)
"""
import glob
import io
import json
import re


def has_korean(s):
    return bool(re.search(r"[가-힣]", s))


def count_tags():
    counts = {}
    files = glob.glob("content/**/*index.md", recursive=True)
    for path in files:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        if not lines or lines[0].strip() != "---":
            continue
        fm_end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm_end = i
                break
        if fm_end is None:
            continue
        tags_start = None
        for i in range(1, fm_end):
            if re.match(r"^tags:\s*$", lines[i].rstrip()):
                tags_start = i + 1
                break
        if tags_start is None:
            continue
        i = tags_start
        while i < fm_end:
            m = re.match(r"^\s*-\s?(.*?)\s*$", lines[i].rstrip())
            if not m:
                break
            val = m.group(1).strip("\"'")
            counts[val] = counts.get(val, 0) + 1
            i += 1
    return counts


def parse_tags_yaml():
    pairs_by_cat = {}
    cat = None
    order = []
    with open("data/tags.yaml", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip() or line.strip().startswith("#"):
                continue
            m = re.match(r"^(\w+):\s*$", line)
            if m:
                cat = m.group(1)
                pairs_by_cat[cat] = []
                order.append(cat)
                continue
            m = re.match(r"^\s*-\s*(.+)$", line)
            if m and cat:
                pairs_by_cat[cat].append(m.group(1).strip())
    return order, pairs_by_cat


def main():
    counts = count_tags()
    order, pairs_by_cat = parse_tags_yaml()

    results = []
    for cat in order:
        tags = pairs_by_cat[cat]
        i = 0
        while i < len(tags):
            t = tags[i]
            if not has_korean(t) and i + 1 < len(tags) and has_korean(tags[i + 1]):
                results.append([cat, t, tags[i + 1], counts.get(t, 0), counts.get(tags[i + 1], 0)])
                i += 2
                continue
            i += 1

    # documented exclusions / manual corrections (see plan section 6)
    results = [r for r in results if not (r[1] == "Deep-Dive" and r[2] == "실습")]
    results = [r for r in results if not (r[1] == "Compression" and r[2] == "터미널")]
    results.append(["devops_and_tools", "Terminal", "터미널", counts.get("Terminal", 0), counts.get("터미널", 0)])

    proper_nouns = {"Python"}
    low_volume_humanities = {
        "Leadership", "Communication", "Interview", "Management", "Decision-Making", "Trust",
        "Business", "Society", "Ethics", "Politics", "Safety", "Accessibility", "Health", "Sports",
        "Identity", "Media", "Revolution",
    }

    rows = []
    for cat, en, ko, ec, kc in results:
        lo, hi = min(ec, kc), max(ec, kc)
        ratio = lo / hi if hi else 0
        if en in proper_nouns:
            verdict = "en_only"
        elif en in low_volume_humanities:
            verdict = "ko_only"
        elif lo < 10 or ratio < 0.15:
            verdict = "en_only" if ec >= kc else "ko_only"
        else:
            verdict = "bilingual"
        rows.append({"category": cat, "en": en, "ko": ko, "en_count": ec, "ko_count": kc, "verdict": verdict})

    with io.open("script/tag_phase8_pairs.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    mapping = {}
    for r in rows:
        en, ko, verdict = r["en"], r["ko"], r["verdict"]
        if verdict == "bilingual":
            merged = f"{en}({ko})"
            mapping[en] = merged
            mapping[ko] = merged
        elif verdict == "en_only":
            mapping[ko] = en
        elif verdict == "ko_only":
            mapping[en] = ko

    with io.open("script/tag_phase8_mapping.json", "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    from collections import Counter
    vc = Counter(r["verdict"] for r in rows)
    print("rows", len(rows), dict(vc))
    print("mapping entries", len(mapping))


if __name__ == "__main__":
    main()
