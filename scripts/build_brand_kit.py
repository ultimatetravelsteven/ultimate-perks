# Builds the Perks brand kit logo files into /home/claude/kit/logos
import base64, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from playwright.sync_api import sync_playwright
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); OUT = '/home/claude/kit/logos'; os.makedirs(OUT, exist_ok=True)
font = TTFont(os.path.join(R, 'assets/fonts/work-sans-latin-900-normal.woff2')); gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font['head'].unitsPerEm
import uharfbuzz as hb, io
_buf = io.BytesIO(); font.flavor = None; font.save(_buf); HBF = hb.Font(hb.Face(_buf.getvalue()))
def text_path(txt, size, x, y):
    sc = size / upm; b = hb.Buffer(); b.add_str(txt); b.guess_segment_properties(); hb.shape(HBF, b, {'kern': True})
    order = font.getGlyphOrder(); adv = sum(p.x_advance for p in b.glyph_positions) * sc; cx = x - adv / 2
    out = []
    for info, pos in zip(b.glyph_infos, b.glyph_positions):
        g = order[info.codepoint]; pen = SVGPathPen(gs); gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, cx + pos.x_offset * sc, y))); cx += pos.x_advance * sc; out.append(pen.getCommands())
    return out
d = text_path('PERKS', 130, 230, 100)
d2 = text_path('PERKS', 130, 239, 109)
NAVY, MINT = '#123B4A', '#4ECAC2'
from svgpathtools import parse_path
xs=[];ys=[]
for x in d+d2:
    a,b_,c,e = parse_path(x).bbox(); xs+=[a,b_]; ys+=[c,e]
VB = (min(xs)-10, min(ys)-10, max(xs)-min(xs)+20, max(ys)-min(ys)+20)
wordmark = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB[0]:.1f} {VB[1]:.1f} {VB[2]:.1f} {VB[3]:.1f}" width="{VB[2]:.0f}" height="{VB[3]:.0f}">
<title>PERKS</title>
<g fill="{NAVY}" stroke="{NAVY}" stroke-width="16" stroke-linejoin="round">{''.join(f'<path d="{x}"/>' for x in d2)}</g>
<g fill="{NAVY}" stroke="{NAVY}" stroke-width="16" stroke-linejoin="round">{''.join(f'<path d="{x}"/>' for x in d)}</g>
<g fill="#FFFFFF">{''.join(f'<path d="{x}"/>' for x in d)}</g>
</svg>'''
open(os.path.join(OUT, 'perks-wordmark.svg'), 'w').write(wordmark)
LOGO = base64.b64encode(open(os.path.join(R, 'assets/logo-white.png'), 'rb').read()).decode()
F7 = base64.b64encode(open(os.path.join(R, 'assets/fonts/work-sans-latin-700-normal.woff2'), 'rb').read()).decode()
WM = 'data:image/svg+xml;base64,' + base64.b64encode(wordmark.encode()).decode()
def lock(w, h, bg, radius, stacked=False, pad=0):
    wmh = h * (0.46 if stacked else 0.62)
    k = 0.62 if stacked else 1
    by = f'<div class="by" style="font-size:{h*.11*k:.0f}px;gap:{h*.05*k:.0f}px"><span>by</span><img src="data:image/png;base64,{LOGO}" style="height:{h*.12*k:.0f}px"></div>'
    return f'''<style>@font-face{{font-family:W;font-weight:700;src:url(data:font/woff2;base64,{F7})}}*{{margin:0}}html,body{{background:transparent}}
#c{{width:{w}px;height:{h}px;background:{bg};border-radius:{radius}px;display:flex;flex-direction:{'column' if stacked else 'row'};align-items:center;justify-content:center;gap:{h*(0.06 if stacked else 0.09):.0f}px;font-family:W;color:#fff;box-sizing:border-box;padding:{pad}px}}
.by{{display:flex;align-items:center;font-weight:700;{'' if stacked else f'padding-top:{h*.2:.0f}px'}}}</style>
<div id="c"><img src="{WM}" style="{f'width:{w*0.8:.0f}px' if stacked else f'height:{wmh:.0f}px'}">{by}</div>'''
jobs = [
 ('perks-wordmark-white.png', f'<style>*{{margin:0}}html,body{{background:transparent}}</style><div id="c" style="width:{VB[2]*5:.0f}px;height:{VB[3]*5:.0f}px"><img src="{WM}" style="width:100%;height:100%"></div>'),
 ('perks-lockup-by-ultimate.png', lock(1800, 420, 'transparent', 0)),
 ('perks-lockup-mint-tile.png', lock(1800, 460, MINT, 60)),
 ('perks-lockup-stacked-mint-square.png', lock(1080, 1080, MINT, 0, stacked=True)),
 ('perks-lockup-stacked-mint-circle.png', lock(1080, 1080, MINT, 540, stacked=True)),
 ('_email-signature-square.png', lock(480, 480, MINT, 56, stacked=True)),
]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for name, html in jobs:
        pg.set_content(html); pg.wait_for_timeout(300)
        pg.locator('#c').screenshot(path=os.path.join(OUT, name), omit_background=True)
    b.close()
print('ok')
