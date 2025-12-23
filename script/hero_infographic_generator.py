from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Card:
    title: str
    subtitle: str = ""
    bullets: list[str] | None = None
    accent: tuple[int, int, int] | None = None


@dataclass(frozen=True)
class Theme:
    bg0: tuple[int, int, int] = (10, 14, 24)
    bg1: tuple[int, int, int] = (12, 18, 34)
    card_bg: tuple[int, int, int] = (17, 24, 46)
    border: tuple[int, int, int] = (45, 55, 84)
    text: tuple[int, int, int] = (235, 240, 250)
    subtext: tuple[int, int, int] = (190, 200, 215)
    footer_bg: tuple[int, int, int] = (14, 20, 40)
    brand_bg: tuple[int, int, int] = (18, 28, 58)
    brand_text: tuple[int, int, int] = (225, 235, 250)
    footer_text: tuple[int, int, int] = (210, 220, 235)


@dataclass(frozen=True)
class Layout:
    margin: int = 96
    gap: int = 56
    header_y: int = 72
    cards_top: int = 290
    cards_h: int = 650
    footer_y: int = 972
    footer_h: int = 88
    card_radius: int = 28
    footer_radius: int = 22
    brand_radius: int = 16


def _find_project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _resolve_font_path(font_path: str | None) -> str | None:
    if not font_path:
        # repo 루트의 font.ttf를 기본값으로 사용
        cand = os.path.join(_find_project_root(), "font.ttf")
        return cand if os.path.isfile(cand) else None
    # 상대 경로면 CWD 기준
    return os.path.abspath(font_path)


def _load_font(font_path: str | None, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if font_path:
        try:
            return ImageFont.truetype(font_path, size=size)
        except Exception:
            pass
    return ImageFont.load_default()


def _text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    """
    공백 기반 래핑이 기본이지만, 한 단어(또는 CJK처럼 공백이 적은 문자열)가 너무 길면
    문자 단위로 강제 분할해 오버플로우를 방지한다.
    """
    if not text:
        return []
    if _text_width(draw, text, font) <= max_width:
        return [text]

    words = text.split(" ")
    lines: list[str] = []
    cur = ""

    def flush() -> None:
        nonlocal cur
        if cur:
            lines.append(cur)
            cur = ""

    for w in words:
        if not w:
            continue
        cand = (cur + " " + w).strip()
        if _text_width(draw, cand, font) <= max_width:
            cur = cand
            continue

        # cand가 안 들어가면: cur를 확정하고 w를 처리
        flush()

        # w 자체가 너무 길면 문자 단위로 쪼갬
        if _text_width(draw, w, font) > max_width:
            chunk = ""
            for ch in w:
                cand2 = chunk + ch
                if _text_width(draw, cand2, font) <= max_width:
                    chunk = cand2
                else:
                    if chunk:
                        lines.append(chunk)
                    chunk = ch
            if chunk:
                cur = chunk
        else:
            cur = w

    flush()
    return lines


def _draw_gradient_bg(img: Image.Image, theme: Theme) -> None:
    W, H = img.size
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / max(1, H - 1)
        r = int(theme.bg0[0] * (1 - t) + theme.bg1[0] * t)
        g = int(theme.bg0[1] * (1 - t) + theme.bg1[1] * t)
        b = int(theme.bg0[2] * (1 - t) + theme.bg1[2] * t)
        draw.line((0, y, W, y), fill=(r, g, b))


def _draw_card(
    img: Image.Image,
    box: tuple[int, int, int, int],
    card: Card,
    *,
    theme: Theme,
    font_path: str | None,
    bullet_prefix: str,
) -> None:
    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box

    radius = 28
    draw.rounded_rectangle(box, radius=radius, fill=theme.card_bg, outline=theme.border, width=2)

    accent = card.accent
    if accent is not None:
        bar_w = 10
        draw.rounded_rectangle((x0, y0, x0 + bar_w, y1), radius=radius, fill=accent)
    else:
        bar_w = 0

    f_title = _load_font(font_path, 46)
    f_sub = _load_font(font_path, 28)
    f_bul = _load_font(font_path, 30)

    pad = 36
    tx = x0 + pad + bar_w
    ty = y0 + pad
    max_w = (x1 - tx) - pad

    # title
    if card.title:
        draw.text((tx, ty), card.title, font=f_title, fill=theme.text)
        ty += 62

    # subtitle
    if card.subtitle:
        for line in _wrap(draw, card.subtitle, f_sub, max_w):
            draw.text((tx, ty), line, font=f_sub, fill=theme.subtext)
            ty += 38
        ty += 12

    # bullets
    bullets = card.bullets or []
    prefix_w = _text_width(draw, bullet_prefix, f_bul)
    indent = max(22, prefix_w)
    for b in bullets:
        lines = _wrap(draw, b, f_bul, max_w - indent)
        if not lines:
            continue
        draw.text((tx, ty), bullet_prefix + lines[0], font=f_bul, fill=theme.text)
        ty += 42
        for cont in lines[1:]:
            draw.text((tx + indent, ty), cont, font=f_bul, fill=theme.text)
            ty += 42
        ty += 6


def _layout_boxes(W: int, layout: Layout, num_cards: int, cols: int) -> list[tuple[int, int, int, int]]:
    """
    N개 카드를 cols 열로 배치한다(현재는 1~3개 정도를 상정).
    rows는 자동 계산.
    """
    cols = max(1, min(cols, max(1, num_cards)))
    rows = (num_cards + cols - 1) // cols

    # 현재 템플릿은 1행 기준으로 디자인되어 있어서, rows>1이면 높이를 나눠쓴다.
    # (여러 상황에서도 깨지지 않게 최소한의 분할 로직 제공)
    card_total_h = layout.cards_h
    row_gap = 28
    card_h = (card_total_h - row_gap * (rows - 1)) // rows

    boxes: list[tuple[int, int, int, int]] = []
    card_w = (W - 2 * layout.margin - layout.gap * (cols - 1)) // cols

    idx = 0
    for r in range(rows):
        y0 = layout.cards_top + r * (card_h + row_gap)
        y1 = y0 + card_h
        for c in range(cols):
            if idx >= num_cards:
                break
            x0 = layout.margin + c * (card_w + layout.gap)
            x1 = x0 + card_w
            boxes.append((x0, y0, x1, y1))
            idx += 1
    return boxes


def generate(
    output_path: str,
    *,
    width: int,
    height: int,
    header_lines: list[str],
    header_subtitle: str | None,
    cards: list[Card],
    footer_text: str | None,
    brand: str | None,
    theme: Theme | None = None,
    layout: Layout | None = None,
    font_path: str | None = None,
    cols: int = 2,
    bullet_prefix: str = "- ",
) -> None:
    theme = theme or Theme()
    layout = layout or Layout()
    font_path = _resolve_font_path(font_path)

    img = Image.new("RGB", (width, height), theme.bg0)
    _draw_gradient_bg(img, theme)
    draw = ImageDraw.Draw(img)

    # header
    f_h1 = _load_font(font_path, 58)
    f_h2 = _load_font(font_path, 30)
    header_x = layout.margin
    y = layout.header_y
    for line in header_lines:
        draw.text((header_x, y), line, font=f_h1, fill=theme.text)
        y += 70
    if header_subtitle:
        draw.text((header_x, y + 10), header_subtitle, font=f_h2, fill=theme.subtext)

    # cards
    boxes = _layout_boxes(width, layout, len(cards), cols=cols)
    for card, box in zip(cards, boxes, strict=False):
        _draw_card(img, box, card, theme=theme, font_path=font_path, bullet_prefix=bullet_prefix)

    # footer
    if footer_text or brand:
        footer_x0, footer_x1 = layout.margin, width - layout.margin
        draw.rounded_rectangle(
            (footer_x0, layout.footer_y, footer_x1, layout.footer_y + layout.footer_h),
            radius=layout.footer_radius,
            fill=theme.footer_bg,
            outline=theme.border,
            width=2,
        )
        footer_font = _load_font(font_path, 26)

        brand_x0 = None
        if brand:
            pad_x, pad_y = 22, 12
            brand_w = _text_width(draw, brand, footer_font)
            brand_box_w = brand_w + pad_x * 2
            brand_box_h = (draw.textbbox((0, 0), brand, font=footer_font)[3]) + pad_y * 2
            bx1 = footer_x1 - 24
            bx0 = bx1 - brand_box_w
            by0 = layout.footer_y + (layout.footer_h - brand_box_h) // 2
            by1 = by0 + brand_box_h
            draw.rounded_rectangle((bx0, by0, bx1, by1), radius=layout.brand_radius, fill=theme.brand_bg)
            draw.text((bx0 + pad_x, by0 + pad_y), brand, font=footer_font, fill=theme.brand_text)
            brand_x0 = bx0

        if footer_text:
            left_pad = 24
            right_limit = (brand_x0 - 24) if brand_x0 is not None else (footer_x1 - 24)
            max_w = right_limit - (footer_x0 + left_pad)
            lines = _wrap(draw, footer_text, footer_font, max_w)
            if len(lines) > 2:
                lines = lines[:2]
            line_h = 34
            total_h = line_h * len(lines)
            ty = layout.footer_y + (layout.footer_h - total_h) // 2
            tx = footer_x0 + left_pad
            for ln in lines:
                draw.text((tx, ty), ln, font=footer_font, fill=theme.footer_text)
                ty += line_h

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    img.save(output_path, format="PNG", optimize=True)


def _default_spec() -> dict[str, Any]:
    # 기존과 동일한 결과를 내는 기본 스펙(호환성 유지)
    return {
        "canvas": {"width": 1920, "height": 1080},
        "header": {
            "lines": ["Privacy is marketing.", "Anonymity is architecture."],
            "subtitle": "프라이버시(약속) vs 익명성(구조) — 설계가 강제집행 가능성을 바꾼다",
        },
        "cards": [
            {
                "title": "Privacy theater (약속/정책)",
                "subtitle": "데이터를 ‘가지고’ 있으면서 잘 지키겠다고 말한다",
                "accent": [255, 120, 85],
                "bullets": [
                    "이메일/전화/ID 요구 → 식별 벡터 누적",
                    "비밀번호 재설정/지원 프로세스 → 소유권 확인을 위해 신원을 저장",
                    "IP/행동 로그/지문 → 운영 데이터가 사용자 모델로 변질",
                    "요청(영장/내부자/침해) 시 ‘제공 가능’ 영역이 생김",
                ],
            },
            {
                "title": "Anonymity by design (아키텍처)",
                "subtitle": "운영자조차 연결할 데이터가 없도록 만든다",
                "accent": [75, 205, 160],
                "bullets": [
                    "무작위 자격증명 기반(예: account number/credential)",
                    "신원·IP·사용패턴 비보유(또는 비연결) 원칙",
                    "계정 복구 불가 같은 UX 비용을 ‘의도된 기능’으로 수용",
                    "요청(영장)에도 ‘줄 데이터가 없음’이 구조로 보장됨",
                ],
            },
        ],
        "footer": {
            "text": "Trade-offs: 관측가능성(로그/메트릭) · 남용 대응 · 결제/환불 · 고객지원 — 익명성은 기능이 아니라 위협모델이다",
            "brand": "42jerrykim.github.io",
        },
        "layout": {"cols": 2},
        "typography": {"bullet_prefix": "- "},
    }


def _parse_rgb(value: Any) -> tuple[int, int, int] | None:
    if value is None:
        return None
    if isinstance(value, (list, tuple)) and len(value) == 3:
        return (int(value[0]), int(value[1]), int(value[2]))
    raise ValueError(f"Invalid RGB: {value}")


def _cards_from_spec(cards_spec: list[dict[str, Any]]) -> list[Card]:
    out: list[Card] = []
    for c in cards_spec:
        out.append(
            Card(
                title=str(c.get("title", "")),
                subtitle=str(c.get("subtitle", "")),
                bullets=[str(x) for x in (c.get("bullets") or [])],
                accent=_parse_rgb(c.get("accent")),
            )
        )
    return out


def _load_spec(path: str | None) -> dict[str, Any]:
    if not path:
        return _default_spec()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate reusable hero/infographic images from a JSON spec.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("output", help="Output PNG path")
    parser.add_argument("--spec", help="Path to JSON spec (optional)")
    parser.add_argument("--font", help="Font path (ttf/otf). Defaults to repo root font.ttf if present.")
    parser.add_argument("--width", type=int, help="Override canvas width")
    parser.add_argument("--height", type=int, help="Override canvas height")
    parser.add_argument("--cols", type=int, help="Override number of columns for card layout")
    parser.add_argument("--brand", help="Override brand text in footer (set empty to disable)")
    parser.add_argument("--footer", help="Override footer text (set empty to disable)")
    parser.add_argument("--bullet-prefix", dest="bullet_prefix", help="Bullet prefix string")
    args = parser.parse_args()

    spec = _load_spec(args.spec)

    canvas = spec.get("canvas", {})
    width = int(args.width or canvas.get("width", 1920))
    height = int(args.height or canvas.get("height", 1080))

    header = spec.get("header", {})
    header_lines = [str(x) for x in (header.get("lines") or [])]
    header_subtitle = header.get("subtitle")

    cards = _cards_from_spec(spec.get("cards") or [])
    if not cards:
        raise SystemExit("spec.cards must contain at least one card")

    footer = spec.get("footer", {})
    footer_text = footer.get("text")
    brand = footer.get("brand")

    if args.footer is not None:
        footer_text = args.footer or None
    if args.brand is not None:
        brand = args.brand or None

    layout_spec = spec.get("layout", {})
    cols = int(args.cols or layout_spec.get("cols", 2))
    typography_spec = spec.get("typography", {})
    bullet_prefix = str(args.bullet_prefix or typography_spec.get("bullet_prefix", "- "))

    generate(
        args.output,
        width=width,
        height=height,
        header_lines=header_lines,
        header_subtitle=str(header_subtitle) if header_subtitle else None,
        cards=cards,
        footer_text=str(footer_text) if footer_text else None,
        brand=str(brand) if brand else None,
        font_path=args.font,
        cols=cols,
        bullet_prefix=bullet_prefix,
    )
    print(f"Wrote: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


