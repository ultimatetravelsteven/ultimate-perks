# One-page A4 Perks brand guidelines -> /home/claude/kit/guidelines
import base64, os
from playwright.sync_api import sync_playwright
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); K = '/home/claude/kit'
b = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
F = {w: b(os.path.join(R, f'assets/fonts/work-sans-latin-{w}-normal.woff2')) for w in ('500', '700', '900')}
WM = 'data:image/svg+xml;base64,' + b(f'{K}/logos/perks-wordmark.svg')
TILE = 'data:image/png;base64,' + b(f'{K}/logos/perks-lockup-mint-tile.png')
SQ = 'data:image/png;base64,' + b(f'{K}/logos/perks-lockup-stacked-mint-square.png')
LOCK = 'data:image/png;base64,' + b(f'{K}/logos/perks-lockup-by-ultimate.png')
cols = [('Mint', '#4ECAC2', 'Main Perks colour. Backgrounds, tiles, price pills.'),
        ('Teal', '#00ADBC', 'PERKS pills, buttons, links, active tabs.'),
        ('Navy', '#123B4A', 'Logo outline and shadow, headings on white.'),
        ('Coral', '#FF775E', 'ACTIVITIES pills, promo call-outs, BETA flag.'),
        ('Ink', '#0E1417', 'Body text on white only.'),
        ('White', '#FFFFFF', 'All text on mint, teal and coral.')]
sw = ''.join(f'<div class="sw"><div class="chip" style="background:{h};{"border:1.5px solid #D9E3E5" if h=="#FFFFFF" else ""}"></div><b>{n}</b><span class="hex">{h}</span><span>{d}</span></div>' for n, h, d in cols)
html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:W;font-weight:500;src:url(data:font/woff2;base64,{F['500']})}}
@font-face{{font-family:W;font-weight:700;src:url(data:font/woff2;base64,{F['700']})}}
@font-face{{font-family:W;font-weight:900;src:url(data:font/woff2;base64,{F['900']})}}
/* // CSS NAME: brand-sheet // */
@page{{size:A4;margin:0}}*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:W;color:#0E1417;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:210mm;height:297mm;padding:9mm 12mm 8mm;display:flex;flex-direction:column;gap:3.6mm;overflow:hidden}}
.hero{{background:#4ECAC2;border-radius:6mm;padding:6mm 8mm;color:#fff;display:flex;align-items:center;justify-content:space-between}}
.hero h1{{font-weight:900;font-size:21pt;line-height:1;text-transform:uppercase;text-shadow:.5mm .5mm 0 #123B4A}}
.hero p{{font-weight:700;font-size:10pt;margin-top:2mm;white-space:nowrap}}
.hero img{{height:22mm}}
h2{{font-weight:900;font-size:12pt;text-transform:uppercase;color:#123B4A;margin-bottom:2mm}}
.row{{display:grid;grid-template-columns:1fr 1fr;gap:6mm}}
p,li{{font-weight:500;font-size:9.2pt;line-height:1.42;color:#33393B}}
ul{{padding-left:4.5mm}}b{{font-weight:700;color:#123B4A}}
.logos{{display:grid;grid-template-columns:1.6fr 1fr 1fr;gap:4mm;align-items:stretch}}
.lg{{border-radius:4mm;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2mm;padding:3.6mm 3mm;font-size:8.6pt;font-weight:700;text-align:center}}
.lg img{{max-width:100%;max-height:22mm}}
.sws{{display:grid;grid-template-columns:repeat(6,1fr);gap:3mm}}
.sw{{display:flex;flex-direction:column;gap:1mm;font-size:8.4pt;line-height:1.35;color:#33393B}}
.sw .chip{{height:11mm;border-radius:3mm;margin-bottom:1mm}}.sw b{{font-size:9.6pt}}.sw .hex{{font-weight:700;color:#123B4A}}
.pills{{display:flex;gap:2.5mm;flex-wrap:wrap;margin-top:2mm}}
.pill{{color:#fff;font-weight:900;font-size:8.6pt;text-transform:uppercase;border-radius:10mm;padding:1.6mm 3.6mm}}
.type .big{{font-weight:900;font-size:17pt;text-transform:uppercase;color:#123B4A;line-height:1}}
.type .mid{{font-weight:700;font-size:12pt;color:#123B4A;margin-top:1.5mm}}
.dont{{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}}
.dn{{border:1.5px solid #FFD4CB;border-radius:3mm;padding:2.4mm;font-size:8.6pt;font-weight:700;color:#123B4A;text-align:center;display:flex;flex-direction:column;gap:2mm;align-items:center;justify-content:space-between}}
.dn .demo{{height:11mm;display:flex;align-items:center;justify-content:center;width:100%;border-radius:2mm}}
.foot{{margin-top:auto;border-top:1.5px solid #E2EAEC;padding-top:3mm;font-size:8.6pt;font-weight:700;color:#123B4A;display:flex;justify-content:space-between}}
</style></head><body><div class="pg">
<div class="hero"><div><h1>Perks brand guidelines</h1><p>Traveller Perks by ULTIMATE &middot; The East Coast traveller club</p></div><img src="{LOCK}" style="height:15mm"></div>

<div><h2>Logo</h2>
<div class="logos">
  <div class="lg" style="background:#4ECAC2;color:#fff"><img src="{LOCK}">Main lockup. Use on mint, teal or a dark photo.</div>
  <div class="lg" style="background:#F2F6F7;color:#123B4A"><img src="{TILE}" style="border-radius:2mm">On white: use the mint tile.</div>
  <div class="lg" style="background:#F2F6F7;color:#123B4A"><img src="{SQ}" style="max-height:24mm;border-radius:2mm">Square: app icon, social avatar, email signature.</div>
</div>
<p style="margin-top:2.6mm">PERKS is white letters with a navy outline and a navy drop shadow, always with "by ULTIMATE" in white beside or under it. Use the supplied files only. Leave clear space around it at least the height of the letter P's bowl.</p></div>

<div><h2>Do not</h2><div class="dont">
  <div class="dn"><div class="demo" style="background:#4ECAC2"><img src="{WM}" style="height:8mm;transform:scale(1.45,.62)"></div>Stretch or squash it</div>
  <div class="dn"><div class="demo" style="background:#FFFFFF;border:1px dashed #CFD8DA"><img src="{WM}" style="height:8mm;opacity:.95"></div>Put the white logo on white</div>
  <div class="dn"><div class="demo" style="background:#4ECAC2;overflow:hidden;justify-content:flex-start"><img src="{WM}" style="height:11mm;margin-left:-6mm"></div>Crop any letter</div>
  <div class="dn"><div class="demo" style="background:#4ECAC2;font-weight:700;font-size:13pt;color:#fff">Perks</div>Retype it in a font</div>
</div></div>

<div><h2>Colours</h2><div class="sws">{sw}</div>
<div class="pills"><span class="pill" style="background:#00ADBC">12 Perks</span><span class="pill" style="background:#FF775E">12 Activities</span><span class="pill" style="background:#4ECAC2">$79 / week</span><span class="pill" style="background:#FF775E">List free with code 'ULTIMATE'</span></div>
<p style="margin-top:2.4mm"><b>The one rule:</b> text on mint, teal or coral is always white. Never black or ink text on orange or coral.</p></div>

<div class="row">
  <div class="type"><h2>Type</h2><div class="big">Work Sans Black</div><div class="mid">Work Sans Bold and Medium</div>
  <ul style="margin-top:2.4mm"><li>Headings: Work Sans 900, uppercase, tight line spacing.</li><li>Body and buttons: Work Sans 500 and 700, sentence case.</li><li>No small, thin uppercase labels above headings.</li></ul></div>
  <div><h2>Words</h2><ul>
  <li>Say <b>Group Tour</b> and <b>Group Leader</b>, always capitalised.</li>
  <li>Venue copy speaks to all East Coast <b>Backpackers and Working Holiday Makers</b>, not only ULTIMATE customers.</li>
  <li>Write the promo code with quotes: <b>'ULTIMATE'</b>.</li>
  <li>Contact is email only: <b>E:</b> perks@ultimate.travel, <b>W:</b> perks.ultimate.travel. No phone numbers.</li>
  <li>No emojis, anywhere.</li></ul></div>
</div>

<div class="row">
  <div><h2>Photos</h2><ul><li>Real venues, real travellers, real food and drinks.</li><li>Self-host every image. Never hotlink from another site.</li><li>Offer cards use one fixed image shape, so every card is the same size.</li></ul></div>
  <div><h2>Where the files are</h2><ul><li>Brand kit zip: logos, animated logo, icons, social images, fonts, business card, signature.</li><li>Email signature: perks.ultimate.travel/signature</li><li>Source: GitHub ultimatetravelsteven/ultimate-perks, assets folder.</li></ul></div>
</div>

<div class="foot"><span>Traveller Perks by ULTIMATE</span><span>Brand guidelines v1.0 &middot; November 2026</span></div>
</div></body></html>'''
open(f'{K}/guidelines/brand-sheet.html', 'w').write(html)
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(); pg.set_content(html); pg.wait_for_timeout(600)
    pg.pdf(path=f'{K}/guidelines/Perks-Brand-Guidelines-v1.0.pdf', prefer_css_page_size=True, print_background=True); br.close()
print('ok')
