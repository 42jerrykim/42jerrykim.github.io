"""Phase 9: pair bare acronym/abbreviation tags with their spelled-out full
name, "ABBR(Full Name)", mirroring the Phase 8 "English(한글)" treatment.

Scope, decided by inspecting data/tags.yaml (post Phase 8) plus actual
frontmatter usage counts:
  - Abbreviations that already got a Korean pairing in Phase 8 (BOJ(백준),
    DP(동적계획법), OOP(객체지향), AI(인공지능), OS(운영체제)) are left as-is --
    the Korean gloss already serves the same clarifying purpose, and
    overriding a just-made Phase 8 call without being asked isn't warranted.
  - A handful of abbreviations turned out to duplicate an already-approved
    spelled-out tag for the identical concept (fragmentation, same kind of
    issue Phase 1/2 fixed for casing): Dynamic-Programming/DP,
    Binary-Indexed-Tree+Fenwick-Tree/BIT, Disjoint-Set/DSU, Sci-Fi/SF. These
    are merged into one canonical "ABBR(Full Name)" tag instead of just
    appending a gloss to both sides.
  - SOLID and PATH are skipped: SOLID has no single contiguous "full name"
    (it's five separate principles' initials) and PATH isn't an acronym of
    anything -- expanding either would be inventing information, not
    reporting it.
"""
import io
import json

# straightforward: bare acronym -> "ABBR(Full Name)"
RENAME = {
    "SQL": "SQL(Structured Query Language)",
    "AWS": "AWS(Amazon Web Services)",
    "GCP": "GCP(Google Cloud Platform)",
    "ICPC": "ICPC(International Collegiate Programming Contest)",
    "USACO": "USACO(USA Computing Olympiad)",
    "BFS": "BFS(Breadth-First Search)",
    "DFS": "DFS(Depth-First Search)",
    "LCA": "LCA(Lowest Common Ancestor)",
    "FFT": "FFT(Fast Fourier Transform)",
    "MST": "MST(Minimum Spanning Tree)",
    "UML": "UML(Unified Modeling Language)",
    "CQRS": "CQRS(Command Query Responsibility Segregation)",
    "GoF": "GoF(Gang of Four)",
    "CI-CD": "CI-CD(Continuous Integration/Continuous Deployment)",
    "IDE": "IDE(Integrated Development Environment)",
    "API": "API(Application Programming Interface)",
    "REST": "REST(Representational State Transfer)",
    "HTTP": "HTTP(HyperText Transfer Protocol)",
    "JSON": "JSON(JavaScript Object Notation)",
    "XML": "XML(eXtensible Markup Language)",
    "YAML": "YAML(YAML Ain't Markup Language)",
    "CDN": "CDN(Content Delivery Network)",
    "SEO": "SEO(Search Engine Optimization)",
    "NLP": "NLP(Natural Language Processing)",
    "LLM": "LLM(Large Language Model)",
    "GPT": "GPT(Generative Pre-trained Transformer)",
    "CPU": "CPU(Central Processing Unit)",
    "IO": "IO(Input/Output)",
    "RAII": "RAII(Resource Acquisition Is Initialization)",
    "SSH": "SSH(Secure Shell)",
    "PWD": "PWD(Print Working Directory)",
    "ELF": "ELF(Executable and Linkable Format)",
    "TOEFL": "TOEFL(Test of English as a Foreign Language)",
    "IELTS": "IELTS(International English Language Testing System)",
    "GRE": "GRE(Graduate Record Examination)",
    "MCU": "MCU(Marvel Cinematic Universe)",
    "TDD": "TDD(Test-Driven Development)",
    "RDP": "RDP(Remote Desktop Protocol)",
    "CSS": "CSS(Cascading Style Sheets)",
    "HTML": "HTML(HyperText Markup Language)",
}

# duplicate-concept merges: multiple approved tags for the same idea collapse
# into one "ABBR(Full Name)" tag
MERGE = {
    "Dynamic-Programming": "DP(동적계획법)",
    "Binary-Indexed-Tree": "BIT(Binary Indexed Tree)",
    "Fenwick-Tree": "BIT(Binary Indexed Tree)",
    "BIT": "BIT(Binary Indexed Tree)",
    "Disjoint-Set": "DSU(Disjoint Set Union)",
    "DSU": "DSU(Disjoint Set Union)",
    "SF": "Sci-Fi(Science Fiction)",
    "Sci-Fi": "Sci-Fi(Science Fiction)",
}

MAPPING = {**RENAME, **MERGE}


def main():
    with io.open("script/tag_phase9_mapping.json", "w", encoding="utf-8") as f:
        json.dump(MAPPING, f, ensure_ascii=False, indent=2)
    print("mapping entries", len(MAPPING))


if __name__ == "__main__":
    main()
