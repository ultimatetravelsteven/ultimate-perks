# ULTIMATE Perks business card: 90 x 55 mm, 3 mm bleed (96 x 61 mm pages), front + back.
import base64, os, qrcode
R = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(R, '..', '..', 'assets')
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
LOGO = b64(os.path.join(A, 'logo-white.png'))
F = {w: b64(os.path.join(A, 'fonts', f'work-sans-latin-{w}-normal.woff2')) for w in ('500', '700', '900')}

def qr_svg(url, color='#123B4A'):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0); q.add_data(url); q.make(fit=True)
    m = q.get_matrix(); n = len(m)
    rects = ''.join(f'<rect x="{x}" y="{y}" width="1.02" height="1.02"/>' for y, row in enumerate(m) for x, v in enumerate(row) if v)
    return f'<svg viewBox="0 0 {n} {n}" shape-rendering="crispEdges"><g fill="{color}">{rects}</g></svg>'

SEE = qr_svg('https://perks.ultimate.travel', '#FFFFFF')
LIST = qr_svg('https://perks.ultimate.travel/venues/#join', '#FFFFFF')

PERKS = '''<svg class="pk" viewBox="0 0 460 112" role="img" aria-label="PERKS"><g font-family="Work Sans" font-weight="900" font-size="130" text-anchor="middle">
<text x="239" y="109" fill="#123B4A" stroke="#123B4A" stroke-width="16" stroke-linejoin="round">PERKS</text>
<text x="230" y="100" fill="#123B4A" stroke="#123B4A" stroke-width="16" stroke-linejoin="round">PERKS</text>
<text x="230" y="100" fill="#FFFFFF">PERKS</text></g></svg>'''

html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'Work Sans';font-weight:500;src:url(data:font/woff2;base64,{F['500']}) format('woff2')}}
@font-face{{font-family:'Work Sans';font-weight:700;src:url(data:font/woff2;base64,{F['700']}) format('woff2')}}
@font-face{{font-family:'Work Sans';font-weight:900;src:url(data:font/woff2;base64,{F['900']}) format('woff2')}}
/* // CSS NAME: card-page // */
@page{{size:96mm 61mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{font-family:'Work Sans',Arial,sans-serif;color:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:96mm;height:61mm;position:relative;overflow:hidden;page-break-after:always}}
.safe{{position:absolute;left:7mm;top:7mm;right:7mm;bottom:7mm}}
/* // CSS NAME: card-front // */
.front{{background:#4ECAC2}}
.front .lock{{display:flex;align-items:flex-end;gap:2.2mm}}
.front .pk{{width:46mm;height:auto;display:block}}
.front .by{{display:flex;align-items:center;gap:1.2mm;font-weight:700;font-size:7pt;padding-bottom:1.6mm;white-space:nowrap}}
.front .by img{{height:2.6mm;width:auto;display:block}}
.front .tag{{margin-top:3.2mm;white-space:nowrap;font-weight:900;font-size:10.5pt;line-height:1.05;text-transform:uppercase;text-shadow:.35mm .35mm 0 #123B4A}}
.front .sub{{margin-top:1.8mm;font-weight:700;font-size:7.6pt;line-height:1.3;white-space:nowrap}}
.front .stops{{margin-top:1.4mm;font-weight:700;font-size:5.6pt;line-height:1.45;white-space:nowrap;color:#fff}}
.front .name{{position:absolute;left:0;right:30mm;bottom:10.5mm;border-bottom:.35mm solid #fff;height:6mm}}
.front .contact{{position:absolute;left:0;bottom:0;font-weight:700;font-size:8pt;line-height:1.45}}
.front .dots{{position:absolute;right:-3mm;bottom:-3mm;width:30mm;height:30mm;border-radius:50%;background:#00ADBC}}
.front .dots b{{position:absolute;left:8.5mm;top:9mm;font-weight:900;font-size:13pt;line-height:.95;text-transform:uppercase;text-align:left}}
/* // CSS NAME: card-back // */
.back{{background:#fff}}
.back .panel{{position:absolute;left:6.5mm;top:6.5mm;right:6.5mm;bottom:6.5mm;background:#00ADBC;border-radius:3.2mm}}
.back .safe{{left:10mm;top:10mm;right:10mm;bottom:10mm}}
.back .grid{{position:absolute;inset:0;display:grid;grid-template-columns:31mm 1fr;gap:3mm;align-items:center}}
.back h2{{font-weight:900;font-size:9.6pt;line-height:1.02;text-transform:uppercase;text-shadow:.35mm .35mm 0 #123B4A}}
.back .pill{{display:inline-block;margin-top:2.6mm;background:#FF775E;color:#fff;font-weight:900;font-size:6.6pt;line-height:1.15;border-radius:2.4mm;padding:1.6mm 2.2mm;text-transform:uppercase}}
.back .url{{margin-top:2.2mm;font-weight:700;font-size:6.8pt}}
.back .qrs{{display:flex;gap:2.2mm;justify-content:flex-end}}
.back .tile{{background:transparent;padding:0;width:19.4mm;text-align:center}}
.back .tile svg{{width:17mm;height:17mm;display:block;margin:0 auto}}
.back .tile b{{display:block;margin-top:1.6mm;color:#fff;font-weight:900;font-size:6.2pt;line-height:1.05;text-transform:uppercase}}
</style></head><body>
<div class="pg front"><div class="safe">
  <div class="lock">{PERKS}<span class="by">by <img src="data:image/png;base64,{LOGO}" alt="ULTIMATE"></span></div>
  <div class="tag">The East Coast traveller club</div>
  <div class="sub">Deals for Backpackers and Working Holiday Makers</div>
  <div class="stops">Melbourne &middot; Sydney &middot; Byron Bay &middot; Surfers Paradise &middot; Brisbane &middot; Noosa<br>Rainbow Beach &middot; K'gari &middot; Whitsundays &middot; Magnetic Island &middot; Mission Beach &middot; Cairns</div>
  <div class="name"></div>
  <div class="contact">E: perks@ultimate.travel<br>W: perks.ultimate.travel</div>
</div></div>
<div class="pg back"><div class="panel"></div><div class="safe"><div class="grid">
  <div><h2>Get your venue in front of East Coast travellers</h2><span class="pill">List free with<br>code 'ULTIMATE'</span><div class="url">W: perks.ultimate.travel</div></div>
  <div class="qrs"><div class="tile">{SEE}<b>See perks</b></div><div class="tile">{LIST}<b>List your venue</b></div></div>
</div></div></div>
</body></html>'''
open(os.path.join(R, 'card.html'), 'w').write(html)

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto('file://' + os.path.join(R, 'card.html')); pg.wait_for_timeout(500)
    pg.pdf(path=os.path.join(R, 'ULTIMATE-Perks-Business-Card-print.pdf'), prefer_css_page_size=True, print_background=True)
    b.close()
print('built')
