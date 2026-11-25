"""Rebuild the profile header PNGs with Pillow and the bundled licensed font.

Run: python -m pip install Pillow; python scripts/render_header.py
The 1600 × 240 artboards display at 800 × 120 (2× pixel density).
GitHub selects a solid light/dark variant using the README's picture element.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / 'assets/fonts/DMSerifDisplay-Regular.ttf'
TEXT = 'Chemistry meets machine learning.'
SIZE = (1600, 240)


def main():
    font = ImageFont.truetype(str(FONT), 80)
    for mode, background, ink, accent in (
        ('light', '#FFFFFF', '#141414', '#136F64'),
        ('dark', '#0D1117', '#FFFFFF', '#C2F3D9'),
    ):
        # Work at 2× the delivery resolution for smooth, crisp serif contours.
        scale = 2
        image = Image.new('RGB', tuple(n * scale for n in SIZE), background)
        draw = ImageDraw.Draw(image)
        render_font = ImageFont.truetype(str(FONT), font.size * scale)
        bounds = draw.textbbox((0, 0), TEXT, font=render_font)
        x = 48 * scale
        y = (SIZE[1] * scale - (bounds[3] - bounds[1])) // 2 - bounds[1]
        assert x + bounds[2] < SIZE[0] * scale - 48 * scale
        draw.text((x, y), TEXT, font=render_font, fill=ink)
        draw.rectangle((x, 194 * scale, x + 64 * scale, 197 * scale), fill=accent)
        image = image.resize(SIZE, Image.Resampling.LANCZOS)
        image.save(ROOT / f'assets/header-{mode}.png', optimize=True)


if __name__ == '__main__':
    main()
