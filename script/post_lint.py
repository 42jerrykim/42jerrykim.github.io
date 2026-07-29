"""Deterministic lint for a single blog post, feeding post-quality-loop's Score stage.

Why this exists
---------------
The quality rubric (.claude/skills/post-quality-loop/rubric.md) had the scoring
agent eyeball things that are mechanically decidable -- tag counts, description
length, prose ratio, broken links. Measured over 228 scored posts, that produced
a 99.1% pass rate with an 18% perfect-score rate, while 74 of those same passing
rows listed defects in their own notes. This script moves every decidable check
out of the model's judgement: it MEASURES and reports, the rubric maps the
measurements to anchor caps, and the critic applies them.

It deliberately reuses script/lint_frontmatter.py (which CI already runs on every
PR) plus find_broken_bold.py / fix_range_tilde.py, so CI and the scoring loop
share one implementation of each rule instead of drifting apart.

Usage:
  python script/post_lint.py <post-path>          # human-readable report
  python script/post_lint.py <post-path> --json   # machine-readable, for the critic
  python script/post_lint.py --scan               # posts missing from the scoreboard

Exit code is 1 when a critical (publication-blocking) finding is present.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import find_broken_bold  # noqa: E402  (sibling script, reused detection logic)
import fix_range_tilde  # noqa: E402
from lint_frontmatter import (  # noqa: E402
    DESC_MAX,
    DESC_MIN,
    TAGS_MIN,
    TITLE_MAX,
    _norm_tag,
    load_approved_tag_index,
)

REPO_ROOT = SCRIPT_DIR.parent
APPROVED_MIN = 10  # rules-that-must-be-followed §1: at least 10 verbatim approved tags
PROSE_MIN_RATIO = 0.40  # rubric §3: paragraphs must be >=40% of the body

BOM = "﻿"
FM_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
FENCE_LANG_RE = re.compile(r"^\s*(?:```|~~~)\s*([A-Za-z0-9_-]*)")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
BARE_URL_RE = re.compile(r"<(https?://[^>\s]+)>")
SHORTCODE_RE = re.compile(r"^\s*\{\{[<%]")

# Author-facing self-certification blocks that must never survive into the body
# (rules-that-must-be-followed §4 / rubric critical defect #3).
META_BLOCK_PATTERNS = [
    "게시 전 자가 점검",
    "평가 기준 재확인",
    "자가 점검 체크리스트",
    "작성자 메모",
    "게시 전 체크리스트",
]

MERMAID_RESERVED = ("end", "graph", "subgraph")
# Exactly the characters §5 enumerates: 대괄호 / 등호 / 비교 연산자 / 괄호.
# Deliberately NOT ':' or ',' -- Mermaid renders those unquoted, and flagging
# them produced false positives on existing, correctly-rendering diagrams.
MERMAID_NEEDS_QUOTE = set("()[]=<>")
# The repo standard for line breaks inside labels (§5); not a special char here.
MERMAID_BREAK_RE = re.compile(r"</br>|<br\s*/?>", re.IGNORECASE)
MERMAID_NODE_ID_RE = re.compile(r"[A-Za-z_][\w-]*")
# Longest delimiters first: ([...]) and [(...)] must win over [ and (, otherwise
# a stadium/cylinder node reads as an unquoted label starting with a bracket.
MERMAID_SHAPES = [
    ("[(", ")]"), ("([", "])"), ("[[", "]]"), ("((", "))"), ("{{", "}}"),
    ("[", "]"), ("(", ")"), ("{", "}"),
]
# Label syntax below only applies to flowcharts; sequence/class/state diagrams
# use ':' message text that is not a node label at all.
MERMAID_FLOW_TYPES = ("flowchart", "graph")
MERMAID_SKIP_LINE = (
    "subgraph", "end", "style", "classdef", "class", "click", "linkstyle",
    "direction", "%%", "flowchart", "graph",
)


def iter_mermaid_labels(line: str):
    """Yield (raw, inner_label) for every node definition on a flowchart line."""
    i, n = 0, len(line)
    while i < n:
        m = MERMAID_NODE_ID_RE.match(line, i)
        if not m:
            i += 1
            continue
        k = m.end()
        while k < n and line[k] == " ":
            k += 1
        shape = next(((o, c) for o, c in MERMAID_SHAPES if line.startswith(o, k)), None)
        if shape is None:
            i = m.end()
            continue
        opener, closer = shape
        body_at = k + len(opener)
        if line.startswith('"', body_at):
            # Quoted label: the closing delimiter is whatever follows the closing
            # quote. Scanning for the delimiter first would stop on a bracket
            # *inside* the quotes (e.g. A["x = [1,2,3]"]) and misread it as unquoted.
            quote_end = line.find('"', body_at + 1)
            if quote_end == -1:
                i = m.end()
                continue
            close_at = line.find(closer, quote_end + 1)
            inner = line[body_at: quote_end + 1]
        else:
            close_at = line.find(closer, body_at)
            inner = line[body_at: close_at] if close_at != -1 else ""
        if close_at == -1:
            i = m.end()
            continue
        yield line[m.start(): close_at + len(closer)], inner
        i = close_at + len(closer)

SEVERITY_ORDER = {"critical": 0, "defect": 1, "info": 2}


@dataclass
class Finding:
    severity: str  # critical | defect | info
    item: int  # rubric 항목 번호 (0 = 정보성, 항목 무관)
    code: str
    message: str
    line: int | None = None
    cap: int | None = None  # anchor ceiling this finding imposes on `item`

    def as_dict(self) -> dict:
        return {
            "severity": self.severity,
            "item": self.item,
            "code": self.code,
            "message": self.message,
            "line": self.line,
            "cap": self.cap,
        }


@dataclass
class Report:
    path: str
    findings: list[Finding] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)
    external_urls: list[str] = field(default_factory=list)

    def add(self, severity, item, code, message, line=None, cap=None):
        self.findings.append(Finding(severity, item, code, message, line, cap))

    @property
    def critical(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "critical"]

    def anchor_caps(self) -> dict[int, int]:
        """Tightest anchor ceiling per rubric item implied by the findings."""
        caps: dict[int, int] = {}
        for f in self.findings:
            if f.cap is None or f.item == 0:
                continue
            caps[f.item] = min(caps.get(f.item, 100), f.cap)
        return caps


# --------------------------------------------------------------------------
# frontmatter / body
# --------------------------------------------------------------------------


def read_text(path: Path) -> tuple[str, bool]:
    """Return (text-without-BOM, had_bom).

    The BOM matters: lint_frontmatter.py anchors its frontmatter regex at the
    start of the file, so a BOM makes CI silently skip the file entirely.
    20 files in content/ are in that state today.
    """
    raw = path.read_text(encoding="utf-8", errors="ignore")
    if raw.startswith(BOM):
        return raw[len(BOM):], True
    return raw, False


def split_frontmatter(text: str) -> tuple[str | None, str, int]:
    """Return (frontmatter_text|None, body, body_start_line)."""
    m = FM_RE.match(text)
    if not m:
        return None, text, 1
    return m.group(1), text[m.end():], text[: m.end()].count("\n") + 1


def classify_lines(body: str) -> tuple[list[tuple[int, str, str]], list[tuple[int, list[str]]]]:
    """Tag every body line with a block kind; also collect mermaid blocks.

    Returns (rows, mermaid_blocks) where rows are (lineno_in_body, kind, text)
    and mermaid_blocks are (start_lineno, lines).
    """
    rows: list[tuple[int, str, str]] = []
    mermaid_blocks: list[tuple[int, list[str]]] = []

    in_fence = False
    fence_lang = ""
    mermaid_start = 0
    mermaid_buf: list[str] = []

    for i, line in enumerate(body.splitlines(), start=1):
        if FENCE_RE.match(line):
            if not in_fence:
                in_fence = True
                fence_lang = (FENCE_LANG_RE.match(line).group(1) or "").lower()
                if fence_lang == "mermaid":
                    mermaid_start, mermaid_buf = i + 1, []
            else:
                if fence_lang == "mermaid":
                    mermaid_blocks.append((mermaid_start, mermaid_buf))
                in_fence, fence_lang = False, ""
            rows.append((i, "fence", line))
            continue

        if in_fence:
            if fence_lang == "mermaid":
                mermaid_buf.append(line)
            rows.append((i, "code", line))
            continue

        stripped = line.strip()
        if not stripped:
            kind = "blank"
        elif stripped.startswith("#"):
            kind = "heading"
        elif SHORTCODE_RE.match(line):
            kind = "shortcode"
        elif stripped.startswith("|"):
            kind = "table"
        elif LIST_RE.match(line):
            kind = "list"
        elif stripped.startswith(">"):
            kind = "quote"
        elif stripped.startswith("<"):
            kind = "html"
        else:
            kind = "prose"
        rows.append((i, kind, line))

    return rows, mermaid_blocks


# --------------------------------------------------------------------------
# URL index (validated at 99.7% against the 3,569 existing internal links)
# --------------------------------------------------------------------------


def _fm_dict(path: Path) -> dict:
    text, _ = read_text(path)
    fm_text, _, _ = split_frontmatter(text)
    if fm_text is None:
        return {}
    try:
        data = yaml.safe_load(fm_text)
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _page_slug(md: Path) -> str:
    fm = _fm_dict(md)
    if fm.get("slug"):
        return str(fm["slug"])
    return md.parent.name if md.name == "index.md" else md.stem


_url_index_cache: set[str] | None = None


def build_url_index(root: Path = REPO_ROOT) -> set[str]:
    """Every URL the content tree publishes, as /post/... paths.

    Collection chapter -> /post/<section-slug>/<page-slug>/
    Plain post         -> /post/<page-slug>/
    """
    global _url_index_cache
    if _url_index_cache is not None:
        return _url_index_cache

    urls: set[str] = set()
    for section_index in (root / "content" / "collection").glob("*/_index.md"):
        coll_dir = section_index.parent
        sec_slug = str(_fm_dict(section_index).get("slug") or coll_dir.name)
        urls.add(f"/post/{sec_slug}/")
        for md in coll_dir.rglob("*.md"):
            if md.name == "_index.md":
                continue
            urls.add(f"/post/{sec_slug}/{_page_slug(md)}/")
    for md in (root / "content" / "post").rglob("*.md"):
        if md.name == "_index.md":
            continue
        urls.add(f"/post/{_page_slug(md)}/")

    _url_index_cache = urls
    return urls


def normalize_internal(target: str) -> str:
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target.endswith("/"):
        target += "/"
    return target


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------


def check_frontmatter(report: Report, fm_text: str | None, post_path: Path) -> dict:
    if fm_text is None:
        report.add("critical", 7, "fm-missing", "frontmatter를 찾을 수 없음 (치명결함 5)", 1, 0)
        return {}
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        report.add("critical", 7, "fm-parse", f"frontmatter YAML 파싱 실패: {str(exc)[:120]} (치명결함 5)", 1, 0)
        return {}
    if not isinstance(fm, dict):
        report.add("critical", 7, "fm-parse", "frontmatter가 매핑이 아님 (치명결함 5)", 1, 0)
        return {}

    title = str(fm.get("title") or "")
    if not title:
        report.add("defect", 7, "title-missing", "title 없음", 1, 70)
    elif len(title) > TITLE_MAX:
        report.add("defect", 7, "title-long", f"title {len(title)}자 (>{TITLE_MAX}자, §1)", 1, 70)

    desc = str(fm.get("description") or "")
    if not desc:
        report.add("defect", 7, "desc-missing", "description 없음", 1, 70)
    elif not (DESC_MIN <= len(desc) <= DESC_MAX):
        report.add("defect", 7, "desc-len", f"description {len(desc)}자 (권장 {DESC_MIN}–{DESC_MAX}자)", 1, 85)

    if "draft" in fm:
        report.add("info", 0, "draft", f"draft: {fm['draft']} (의도 부합 여부는 채점자가 판정)")
    else:
        report.add("info", 0, "draft", "draft 필드 없음 = 게시 상태 (신규 초안이면 치명결함 5)")

    report.metrics.update(
        {
            "title_len": len(title),
            "description_len": len(desc),
            "collection_order": fm.get("collection_order"),
            "draft": fm.get("draft", "(없음)"),
        }
    )
    return fm


def check_tags(report: Report, fm: dict) -> None:
    tags = fm.get("tags") or []
    if not isinstance(tags, list):
        report.add("defect", 7, "tags-shape", "tags가 리스트가 아님", 1, 70)
        return
    tags = [str(t) for t in tags]

    approved = load_approved_tag_index(REPO_ROOT)
    exact, misspelled, unknown = [], [], []
    for t in tags:
        canonical = approved.get(_norm_tag(t))
        if canonical is None:
            unknown.append(t)
        elif canonical == t:
            exact.append(t)
        else:
            misspelled.append((t, canonical))

    report.metrics.update(
        {
            "tags_total": len(tags),
            "tags_approved_exact": len(exact),
            "tags_misspelled": len(misspelled),
            "tags_unknown": len(unknown),
        }
    )

    if len(tags) < TAGS_MIN:
        report.add("defect", 7, "tags-count", f"tags {len(tags)}개 (<{TAGS_MIN}개, §1)", 1, 70)
    if len(exact) < APPROVED_MIN:
        report.add(
            "defect", 7, "tags-approved",
            f"승인 태그 표기 그대로 {len(exact)}개 (<{APPROVED_MIN}개, §1)", 1, 70,
        )
    if misspelled:
        cap = 85 if len(misspelled) <= 3 else 70
        sample = ", ".join(f"'{t}'→'{c}'" for t, c in misspelled[:4])
        report.add(
            "defect", 7, "tags-spelling",
            f"승인 태그 표기 불일치 {len(misspelled)}개: {sample}", 1, cap,
        )
    if unknown:
        report.add(
            "info", 0, "tags-unknown",
            f"tags.yaml 미등재 태그 {len(unknown)}개: {', '.join(unknown[:6])}"
            f"{' …' if len(unknown) > 6 else ''} (고유 태그면 정상, 주제 무관이면 채점자가 감점)",
        )


def check_links(report: Report, fm: dict, offset: int, post_path: Path, rows) -> None:
    url_index = build_url_index()
    code_lines = {ln for ln, kind, _ in rows if kind in ("code", "fence")}

    external, internal_bad, asset_bad = [], 0, 0
    for ln, kind, line in rows:
        if ln in code_lines:
            continue
        targets = [m.group(1) for m in LINK_RE.finditer(line)]
        targets += [m.group(1) for m in BARE_URL_RE.finditer(line)]
        for target in targets:
            abs_line = ln + offset - 1
            if target.startswith(("http://", "https://")):
                external.append(target)
            elif target.startswith("/post/"):
                if normalize_internal(target) not in url_index:
                    internal_bad += 1
                    report.add(
                        "critical", 7, "link-internal",
                        f"내부 링크 대상 없음: {target} (치명결함 1)", abs_line, 0,
                    )
            elif target.startswith(("#", "mailto:", "/")):
                continue  # 앵커·메일·기타 절대경로는 대상 판정 보류
            else:
                asset = (post_path.parent / target).resolve()
                if not asset.exists():
                    asset_bad += 1
                    report.add(
                        "critical", 7, "asset-missing",
                        f"저장소에 없는 파일 참조: {target} (치명결함 1)", abs_line, 0,
                    )

    image = fm.get("image")
    if image and not str(image).startswith(("http", "/")):
        if not (post_path.parent / str(image)).exists():
            report.add("critical", 7, "image-missing", f"frontmatter image 파일 없음: {image} (치명결함 1)", 1, 0)

    report.external_urls = sorted(set(external))
    report.metrics.update(
        {
            "links_external": len(report.external_urls),
            "links_internal_broken": internal_bad,
            "assets_missing": asset_bad,
        }
    )


def check_prose_ratio(report: Report, rows) -> None:
    counted = {"prose", "code", "table", "list", "quote", "html"}
    totals = {k: 0 for k in counted}
    for _, kind, line in rows:
        if kind in counted:
            totals[kind] += len(line.strip())
    denominator = sum(totals.values())
    ratio = totals["prose"] / denominator if denominator else 0.0

    report.metrics["prose_ratio"] = round(ratio, 4)
    report.metrics["prose_breakdown"] = totals
    if denominator and ratio < PROSE_MIN_RATIO:
        report.add(
            "defect", 3, "prose-ratio",
            f"산문 비율 {ratio * 100:.1f}% (<{PROSE_MIN_RATIO * 100:.0f}%, rubric §3)", None, 70,
        )


def check_mermaid(report: Report, mermaid_blocks, offset: int) -> None:
    report.metrics["mermaid_blocks"] = len(mermaid_blocks)
    for start, lines in mermaid_blocks:
        diagram_type = ""
        for line in lines:
            if line.strip():
                diagram_type = line.strip().split()[0].lower()
                break
        is_flowchart = diagram_type.startswith(MERMAID_FLOW_TYPES)

        for j, line in enumerate(lines):
            abs_line = start + j + offset - 1
            stripped = line.strip()

            for word in MERMAID_RESERVED:
                if re.match(rf"^\s*{word}\s*[\[\(\{{]", line):
                    report.add(
                        "critical", 6, "mermaid-reserved",
                        f"예약어를 노드 ID로 사용: '{word}' (§5, 렌더 실패 가능)", abs_line, 0,
                    )

            if "\\n" in line:
                report.add(
                    "defect", 6, "mermaid-newline",
                    r"라벨에 \n 사용 — 이 저장소 표준은 </br> (§5)", abs_line, 70,
                )

            if not is_flowchart or stripped.lower().startswith(MERMAID_SKIP_LINE):
                continue
            for raw, inner in iter_mermaid_labels(line):
                label = MERMAID_BREAK_RE.sub("", inner).strip()
                if not label or (label.startswith('"') and label.endswith('"')):
                    continue
                if any(ch in MERMAID_NEEDS_QUOTE for ch in label):
                    report.add(
                        "defect", 6, "mermaid-quote",
                        f"특수문자 포함 라벨에 따옴표 없음: {raw[:48]} (§5)", abs_line, 70,
                    )


def check_meta_blocks(report: Report, rows, offset: int) -> None:
    for ln, kind, line in rows:
        if kind in ("code", "fence"):
            continue
        for pattern in META_BLOCK_PATTERNS:
            if pattern in line:
                report.add(
                    "critical", 4, "meta-block",
                    f"작성자용 메타블록 잔존: '{pattern}' (치명결함 3)", ln + offset - 1, 0,
                )


def check_prose_typography(report: Report, rows, offset: int) -> None:
    """§9 range tildes and §10 broken bold, using the existing scripts' logic."""
    tilde_hits, bold_hits = 0, 0
    for ln, kind, line in rows:
        if kind in ("code", "fence"):
            continue
        _, n = fix_range_tilde.process_line(line)
        if n:
            tilde_hits += n
            report.add(
                "defect", 7, "range-tilde",
                f"범위 표기 물결표 {n}개 — en dash(–)로 교체 (§9, 취소선 오파싱)", ln + offset - 1, 85,
            )
        _, hits = find_broken_bold.process_line(line)
        if hits:
            bold_hits += len(hits)
            report.add(
                "defect", 7, "broken-bold",
                f"렌더되지 않는 **강조** {len(hits)}개 — <strong> 사용 (§10): {hits[0][:48]}",
                ln + offset - 1, 85,
            )
    report.metrics.update({"range_tildes": tilde_hits, "broken_bold": bold_hits})


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------


def lint_post(post_path: Path) -> Report:
    report = Report(path=str(post_path.relative_to(REPO_ROOT)).replace("\\", "/"))

    text, had_bom = read_text(post_path)
    if had_bom:
        report.add(
            "defect", 7, "bom",
            "파일 선두 UTF-8 BOM — lint_frontmatter.py(CI)가 이 파일을 통째로 건너뜀", 1, 85,
        )

    fm_text, body, offset = split_frontmatter(text)
    rows, mermaid_blocks = classify_lines(body)

    fm = check_frontmatter(report, fm_text, post_path)
    if fm:
        check_tags(report, fm)
    check_links(report, fm, offset, post_path, rows)
    check_prose_ratio(report, rows)
    check_mermaid(report, mermaid_blocks, offset)
    check_meta_blocks(report, rows, offset)
    check_prose_typography(report, rows, offset)

    report.metrics["body_lines"] = len(rows)
    return report


def render_human(report: Report) -> str:
    out = [f"# post_lint: {report.path}", ""]

    m = report.metrics
    out.append("## 측정값")
    out.append(f"- title {m.get('title_len', 0)}자 / description {m.get('description_len', 0)}자")
    out.append(
        f"- tags {m.get('tags_total', 0)}개 (승인 표기 일치 {m.get('tags_approved_exact', 0)}, "
        f"표기 불일치 {m.get('tags_misspelled', 0)}, 미등재 {m.get('tags_unknown', 0)})"
    )
    out.append(f"- 산문 비율 {m.get('prose_ratio', 0) * 100:.1f}%  (본문 {m.get('body_lines', 0)}줄)")
    out.append(
        f"- 링크: 외부 {m.get('links_external', 0)} / 내부 깨짐 {m.get('links_internal_broken', 0)} "
        f"/ 누락 파일 {m.get('assets_missing', 0)}"
    )
    out.append(f"- Mermaid 블록 {m.get('mermaid_blocks', 0)}개, draft: {m.get('draft')}")
    out.append("")

    caps = report.anchor_caps()
    if caps:
        out.append("## 앵커 상한 (rubric 1.1 매핑)")
        for item in sorted(caps):
            out.append(f"- 항목 {item}: 최대 {caps[item]}")
        out.append("")

    if report.findings:
        out.append("## 결함")
        for f in sorted(report.findings, key=lambda x: (SEVERITY_ORDER[x.severity], x.item, x.line or 0)):
            loc = f"L{f.line}" if f.line else "-"
            tag = {"critical": "치명", "defect": "결함", "info": "정보"}[f.severity]
            item = f"항목{f.item}" if f.item else "정보"
            out.append(f"- [{tag}][{item}] {loc}: {f.message}")
    else:
        out.append("## 결함\n- 없음")

    if report.external_urls:
        out.append("")
        out.append(f"## 외부 링크 {len(report.external_urls)}개 (채점자가 WebFetch로 검증)")
        for u in report.external_urls:
            out.append(f"- {u}")

    return "\n".join(out)


def scoreboard_paths(scoreboard: Path) -> set[str]:
    if not scoreboard.exists():
        return set()
    paths = set()
    for line in scoreboard.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| content/"):
            continue
        paths.add(line.split("|")[1].strip())
    return paths


def scan(scoreboard: Path) -> list[str]:
    """Published posts that the scoreboard has not registered yet."""
    known = scoreboard_paths(scoreboard)
    missing = []
    for base in ("post", "collection"):
        for md in (REPO_ROOT / "content" / base).rglob("*.md"):
            if md.name == "_index.md":
                continue
            fm = _fm_dict(md)
            if fm.get("draft") is True:
                continue  # 초안은 신규 초안 모드에서 다룬다
            rel = str(md.relative_to(REPO_ROOT)).replace("\\", "/")
            if rel not in known:
                missing.append(rel)
    return sorted(missing)


def main() -> int:
    parser = argparse.ArgumentParser(description="post-quality-loop 결정론적 린트")
    parser.add_argument("post", nargs="?", help="채점할 글 경로")
    parser.add_argument("--json", action="store_true", help="JSON 출력")
    parser.add_argument("--scan", action="store_true", help="스코어보드 미등록 게시글 목록")
    parser.add_argument(
        "--scoreboard",
        default=str(REPO_ROOT / ".claude" / "quality" / "scoreboard.md"),
        help="스코어보드 경로",
    )
    args = parser.parse_args()

    if args.scan:
        missing = scan(Path(args.scoreboard))
        if args.json:
            print(json.dumps({"missing": missing, "count": len(missing)}, ensure_ascii=False, indent=2))
        else:
            print(f"스코어보드 미등록 게시글 {len(missing)}개")
            for p in missing:
                print(p)
        return 0

    if not args.post:
        parser.error("글 경로 또는 --scan 이 필요합니다")

    post_path = Path(args.post)
    if not post_path.is_absolute():
        post_path = (REPO_ROOT / post_path).resolve()
    if not post_path.exists():
        print(f"파일 없음: {post_path}", file=sys.stderr)
        return 2

    report = lint_post(post_path)
    if args.json:
        print(
            json.dumps(
                {
                    "path": report.path,
                    "metrics": report.metrics,
                    "anchor_caps": report.anchor_caps(),
                    "findings": [f.as_dict() for f in report.findings],
                    "external_urls": report.external_urls,
                    "critical_count": len(report.critical),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(render_human(report))

    return 1 if report.critical else 0


if __name__ == "__main__":
    sys.exit(main())
