"""Phase 8: rewrite data/tags.yaml so each en/ko pair becomes a single
approved tag per the verdicts in script/tag_phase8_pairs.json:
  - bilingual: two lines "En" + "Ko" -> one line "En(Ko)"
  - en_only:   two lines "En" + "Ko" -> keep "En", drop "Ko"
  - ko_only:   two lines "En" + "Ko" -> drop "En", keep "Ko"
The one non-adjacent pair (Terminal/터미널) is handled as a special case since
it can't be resolved by simple adjacent-line replacement.
"""
import io
import json
import re

with io.open("script/tag_phase8_pairs.json", encoding="utf-8") as f:
    rows = json.load(f)

# adjacent pairs: keyed by (category, en) -> (ko, verdict)
adjacent = {}
special = None
for r in rows:
    if r["en"] == "Terminal" and r["ko"] == "터미널":
        special = r
        continue
    adjacent[(r["category"], r["en"])] = (r["ko"], r["verdict"])

with io.open("data/tags.yaml", encoding="utf-8") as f:
    lines = f.readlines()

out = []
cat = None
i = 0
n = len(lines)
while i < n:
    line = lines[i]
    stripped = line.rstrip("\n")
    m = re.match(r"^(\w+):\s*$", stripped)
    if m and not stripped.strip().startswith("#"):
        cat = m.group(1)
        out.append(line)
        i += 1
        continue
    m = re.match(r"^(\s*-\s*)(.+)$", stripped)
    if m:
        indent, value = m.group(1), m.group(2).strip()
        key = (cat, value)
        if key in adjacent:
            ko, verdict = adjacent[key]
            # confirm the very next line is indeed the ko partner
            next_stripped = lines[i + 1].rstrip("\n") if i + 1 < n else ""
            nm = re.match(r"^\s*-\s*(.+)$", next_stripped)
            assert nm and nm.group(1).strip() == ko, f"expected {ko!r} after {value!r} in {cat}, got {next_stripped!r}"
            if verdict == "bilingual":
                out.append(f"{indent}{value}({ko})\n")
            elif verdict == "en_only":
                out.append(f"{indent}{value}\n")
            elif verdict == "ko_only":
                out.append(f"{indent}{ko}\n")
            i += 2
            continue
        if special and cat == "devops_and_tools" and value == "Terminal":
            out.append(f"{indent}Terminal(터미널)\n")
            i += 1
            continue
        if special and cat == "devops_and_tools" and value == "터미널":
            # dropped: merged into the Terminal(터미널) line above
            i += 1
            continue
        out.append(line)
        i += 1
        continue
    out.append(line)
    i += 1

with io.open("data/tags.yaml", "w", encoding="utf-8", newline="\n") as f:
    f.writelines(out)

print("wrote data/tags.yaml:", len(out), "lines (was", n, ")")
