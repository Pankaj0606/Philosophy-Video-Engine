"""
Typography & Card Design Engine:
Renders Netflix-grade Title Sequences, Chapter Intros,
and Sanskrit/Philosophical Quote Cards with Devanagari and Golden Accents.
"""

import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "fonts"))
os.makedirs(FONTS_DIR, exist_ok=True)

ENGLISH_FONT_PATH = os.path.join(FONTS_DIR, "Cinzel-Bold.ttf")
SANSKRIT_FONT_PATH = os.path.join(FONTS_DIR, "NotoSerifDevanagari-Bold.ttf")
BODY_FONT_PATH = os.path.join(FONTS_DIR, "Cinzel-Regular.ttf")


def ensure_fonts():
    """Downloads authoritative typography fonts if not already cached locally."""
    font_urls = {
        ENGLISH_FONT_PATH: "https://raw.githubusercontent.com/google/fonts/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
        SANSKRIT_FONT_PATH: "https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifdevanagari/NotoSerifDevanagari%5Bwght%5D.ttf",
        BODY_FONT_PATH: "https://raw.githubusercontent.com/google/fonts/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
    }
    for path, url in font_urls.items():
        if not os.path.exists(path) or os.path.getsize(path) < 1000:
            try:
                urllib.request.urlretrieve(url, path)
            except Exception:
                pass


ensure_fonts()


def get_font(path: str, size: int):
    """Loads custom font or falls back safely to Mac system serif fonts."""
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        # Fallbacks for macOS
        for sys_font in ["/System/Library/Fonts/Supplemental/Times New Roman.ttf", "/System/Library/Fonts/Kohinoor.ttc"]:
            if os.path.exists(sys_font):
                return ImageFont.truetype(sys_font, size)
        return ImageFont.load_default()


def create_chapter_card(chapter_roman: str, chapter_title: str, output_path: str):
    """Generates an atmospheric Chapter Title sequence image."""
    w, h = 1920, 1080
    img = Image.new("RGBA", (w, h), (10, 12, 16, 255))
    draw = ImageDraw.Draw(img)

    # 1. Subtle Golden Ornamental Border
    margin = 80
    border_color = (197, 160, 89, 140)  # Classical gold
    draw.rectangle([margin, margin, w - margin, h - margin], outline=border_color, width=2)
    draw.rectangle([margin + 12, margin + 12, w - margin - 12, h - margin - 12], outline=(197, 160, 89, 50), width=1)

    # 2. Chapter Subtitle (e.g., "— CHAPTER I —")
    font_sub = get_font(ENGLISH_FONT_PATH, 32)
    sub_text = f"— {chapter_roman.upper()} —"
    sub_bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text(((w - sub_w) / 2, 430), sub_text, font=font_sub, fill=(197, 160, 89, 230))

    # 3. Main Title
    font_title = get_font(ENGLISH_FONT_PATH, 68)
    title_text = chapter_title.upper()
    t_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    t_w = t_bbox[2] - t_bbox[0]

    # Draw subtle text glow
    for ox, oy in [(-2, -2), (2, 2), (-2, 2), (2, -2)]:
        draw.text(((w - t_w) / 2 + ox, 500 + oy), title_text, font=font_title, fill=(0, 0, 0, 200))
    draw.text(((w - t_w) / 2, 500), title_text, font=font_title, fill=(245, 245, 240, 255))

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.convert("RGB").save(output_path, quality=95)


def create_quote_card(sanskrit_verse: str, english_trans: str, attribution: str, output_path: str):
    """
    Renders an ancient philosophy quote card with:
    - Primary verse in authentic Sanskrit (Devanagari)
    - Golden quotation markers
    - English translation & Attribution
    """
    w, h = 1920, 1080
    img = Image.new("RGBA", (w, h), (8, 9, 12, 255))
    draw = ImageDraw.Draw(img)

    # Decorative background tint
    draw.rectangle([120, 120, w - 120, h - 120], outline=(180, 140, 75, 100), width=2)

    # Decorative Quotation Mark "“"
    font_quote_mark = get_font(ENGLISH_FONT_PATH, 160)
    draw.text((w / 2 - 40, 210), "“", font=font_quote_mark, fill=(180, 140, 75, 80))

    # Sanskrit Verse (Devanagari)
    font_sanskrit = get_font(SANSKRIT_FONT_PATH, 48)
    s_bbox = draw.textbbox((0, 0), sanskrit_verse, font=font_sanskrit)
    s_w = s_bbox[2] - s_bbox[0]
    draw.text(((w - s_w) / 2, 400), sanskrit_verse, font=font_sanskrit, fill=(245, 225, 170, 255))

    # Ornamental Divider
    draw.line([(w / 2 - 120, 510), (w / 2 + 120, 510)], fill=(180, 140, 75, 160), width=2)
    draw.rectangle([(w / 2 - 5, 507), (w / 2 + 5, 513)], fill=(197, 160, 89, 255))

    # English Translation (Multi-line)
    font_trans = get_font(BODY_FONT_PATH, 34)
    trans_text = f'"{english_trans}"'
    t_bbox = draw.textbbox((0, 0), trans_text, font=font_trans)
    t_w = t_bbox[2] - t_bbox[0]
    draw.text(((w - t_w) / 2, 570), trans_text, font=font_trans, fill=(230, 230, 235, 230))

    # Attribution / Source
    font_attr = get_font(ENGLISH_FONT_PATH, 24)
    attr_text = f"— {attribution.upper()} —"
    a_bbox = draw.textbbox((0, 0), attr_text, font=font_attr)
    a_w = a_bbox[2] - a_bbox[0]
    draw.text(((w - a_w) / 2, 690), attr_text, font=font_attr, fill=(180, 140, 75, 210))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.convert("RGB").save(output_path, quality=95)