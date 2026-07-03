"""Phase 9: rewrite data/tags.yaml -- rename bare abbreviation tags to
"ABBR(Full Name)" and drop lines for tags merged into another abbreviation's
canonical form (see script/tag_phase9_build_mapping.py for the mapping and
the reasoning for each rename/merge).
"""
import io
import json
import re

with io.open("script/tag_phase9_mapping.json", encoding="utf-8") as f:
    mapping = json.load(f)

# tags that get renamed in place (old value appears once, becomes new value)
RENAME_ONLY = {k: v for k, v in mapping.items() if k in {
    "SQL", "AWS", "GCP", "ICPC", "USACO", "BFS", "DFS", "LCA", "FFT", "MST",
    "UML", "CQRS", "GoF", "CI-CD", "IDE", "API", "REST", "HTTP", "JSON",
    "XML", "YAML", "CDN", "SEO", "NLP", "LLM", "GPT", "CPU", "IO", "RAII",
    "SSH", "PWD", "ELF", "TOEFL", "IELTS", "GRE", "MCU", "TDD", "RDP",
    "CSS", "HTML",
}}

# tags that get renamed to the merge target; duplicates of the same target
# collapse to a single line, kept at the position of the first occurrence
MERGE_TARGETS = {
    "Dynamic-Programming": "DP(동적계획법)",
    "Binary-Indexed-Tree": "BIT(Binary Indexed Tree)",
    "Fenwick-Tree": "BIT(Binary Indexed Tree)",
    "BIT": "BIT(Binary Indexed Tree)",
    "Disjoint-Set": "DSU(Disjoint Set Union)",
    "DSU": "DSU(Disjoint Set Union)",
    "SF": "Sci-Fi(Science Fiction)",
    "Sci-Fi": "Sci-Fi(Science Fiction)",
}

with io.open("data/tags.yaml", encoding="utf-8") as f:
    lines = f.readlines()

out = []
emitted_targets = set()
for line in lines:
    stripped = line.rstrip("\n")
    m = re.match(r"^(\s*-\s*)(.+)$", stripped)
    if not m:
        out.append(line)
        continue
    indent, value = m.group(1), m.group(2).strip()
    if value in RENAME_ONLY:
        out.append(f"{indent}{RENAME_ONLY[value]}\n")
        continue
    if value in MERGE_TARGETS:
        target = MERGE_TARGETS[value]
        if target in emitted_targets:
            continue  # drop: already emitted at the first occurrence
        emitted_targets.add(target)
        out.append(f"{indent}{target}\n")
        continue
    out.append(line)

with io.open("data/tags.yaml", "w", encoding="utf-8", newline="\n") as f:
    f.writelines(out)

print("wrote data/tags.yaml:", len(out), "lines (was", len(lines), ")")
