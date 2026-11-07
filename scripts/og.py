#!/usr/bin/env python3
"""
OG 미리보기 그림(1200×630) 4개 언어 — 앱 아이콘을 출시순으로 한 줄. 앱이 늘면 다시 돌린다: python3 scripts/og.py
아이콘은 assets/apps/<id>.webp(384px). 순서는 index.html APPS 의 sort 순이 아니라 아래 ORDER(한 줄에 9개까지, 넘으면 두 줄).
글꼴은 macOS 의 Apple SD Gothic Neo(한·영·일·중 전부 들어 있다).
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), '..')
ORDER = ['buruda', 'wemera', 'tobeokmap', 'timeteller', 'morado-ildeung', 'todaycolor', 'nom', 'petitmap', 'dondon', 'tuck', 'meong']
TEXT = {
    'ko': ('mubi labs', '나부터 쓰고 싶은 앱을 만들고 있습니다.'),
    'en': ('mubi labs', 'Apps I want to use myself.'),
    'ja': ('mubi labs', 'まず自分が使いたいアプリを作っています。'),
    'zh': ('mubi labs', '先做我自己想用的 App。'),
}
FONT = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
BG, INK, SUB, FOOT = (247, 248, 250), (14, 17, 22), (76, 80, 83), (134, 138, 141)
W, H, M = 1200, 630, 80

def rounded(im, r):
    mask = Image.new('L', im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.size[0] - 1, im.size[1] - 1), r, fill=255)
    out = im.convert('RGBA'); out.putalpha(mask); return out

def make(lang):
    title, lede = TEXT[lang]
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((M, 100), title, font=ImageFont.truetype(FONT, 62, index=6), fill=INK)
    d.text((M, 180), lede, font=ImageFont.truetype(FONT, 26, index=2), fill=SUB)
    n = len(ORDER); per_row = min(n, 9); rows = (n + per_row - 1) // per_row
    gap = 18; size = min(130, (W - 2 * M - gap * (per_row - 1)) // per_row)
    total = per_row * size + gap * (per_row - 1); x0 = (W - total) // 2
    y0 = 300 if rows == 1 else 250
    for i, app in enumerate(ORDER):
        r, c = divmod(i, per_row)
        ic = Image.open(os.path.join(ROOT, 'assets/apps', app + '.webp')).convert('RGB').resize((size, size), Image.LANCZOS)
        ic = rounded(ic, int(size * 0.225))
        x = x0 + c * (size + gap); y = y0 + r * (size + gap)
        sh = Image.new('RGBA', (size + 8, size + 8), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((4, 6, size + 3, size + 7), int(size * 0.225), fill=(0, 0, 0, 22))
        im.paste(sh, (x - 4, y - 2), sh); im.paste(ic, (x, y), ic)
    d.text((M, 540), 'younghwakim.github.io · Threads @mubi.labs', font=ImageFont.truetype(FONT, 22, index=0), fill=FOOT)
    out = os.path.join(ROOT, 'assets', 'og.jpg' if lang == 'ko' else f'og-{lang}.jpg')
    im.save(out, 'JPEG', quality=90); print(out)

for lang in TEXT: make(lang)
