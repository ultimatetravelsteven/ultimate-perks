# Renders the email logo (transparent) and the email signature tile (mint) at 2x.
import base64, os
from playwright.sync_api import sync_playwright
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
b = lambda p: base64.b64encode(open(os.path.join(R, p), 'rb').read()).decode()
F = b('assets/fonts/work-sans-latin-900-normal.woff2'); F7 = b('assets/fonts/work-sans-latin-700-normal.woff2'); LOGO = b('assets/logo-white.png')
PERKS = '''<svg viewBox="-2 -2 474 122" style="height:100%;width:auto;display:block"><g font-family="Work Sans" font-weight="900" font-size="130" text-anchor="middle">
<text x="239" y="109" fill="#123B4A" stroke="#123B4A" stroke-width="16" stroke-linejoin="round">PERKS</text>
<text x="230" y="100" fill="#123B4A" stroke="#123B4A" stroke-width="16" stroke-linejoin="round">PERKS</text>
<text x="230" y="100" fill="#FFFFFF">PERKS</text></g></svg>'''
def page(w, h, bg, inner):
    return f'''<style>@font-face{{font-family:'Work Sans';font-weight:900;src:url(data:font/woff2;base64,{F})}}@font-face{{font-family:'Work Sans';font-weight:700;src:url(data:font/woff2;base64,{F7})}}
*{{margin:0;padding:0}}html,body{{background:transparent}}#c{{width:{w}px;height:{h}px;background:{bg};display:flex;align-items:center;justify-content:center;gap:14px;border-radius:{'18px' if bg!='transparent' else '0'};font-family:'Work Sans'}}
.pk{{height:{int(h*0.58)}px;width:{int(h*0.58*474/122)}px;flex:none}}.by{{display:flex;align-items:center;gap:7px;color:#fff;font-weight:700;font-size:{int(h*0.15)}px;padding-top:{int(h*0.2)}px}}.by img{{height:{int(h*0.16)}px}}</style>
<div id="c">{inner}</div>'''
lock = f'<div class="pk">{PERKS}</div><div class="by">by <img src="data:image/png;base64,{LOGO}"></div>'
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(device_scale_factor=2)
    pg.set_content(page(330, 84, '#4ECAC2', lock)); pg.wait_for_timeout(400)
    pg.locator('#c').screenshot(path=os.path.join(R, 'assets/social/email-signature-perks.png'), omit_background=True)
    pg.set_content(page(443, 88, 'transparent', f'<div class="pk" style="height:72px;width:280px">{PERKS}</div>')); pg.wait_for_timeout(400)
    pg.locator('#c').screenshot(path=os.path.join(R, 'assets/social/email-perks-logo.png'), omit_background=True)
    br.close()
print('ok')
