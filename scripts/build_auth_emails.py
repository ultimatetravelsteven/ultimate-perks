# Builds the branded Supabase Auth email templates into emails/auth/.
# Paste each file into Supabase > Authentication > Emails > Templates.
import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'emails', 'auth')
LOGO = 'https://perks.ultimate.travel/assets/social/email-perks-logo.png'
F = "'Work Sans',Arial,Helvetica,sans-serif"
FD = "'Work Sans','Arial Black',Arial,sans-serif"

def shell(title, inner, btn, note):
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title></head>
<body style="margin:0;padding:0;background:#F4F8F8">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F4F8F8"><tr><td align="center" style="padding:32px 16px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#FFFFFF;border-radius:20px;overflow:hidden">
<tr><td align="center" style="background:#4ECAC2;padding:28px 24px 22px"><img src="{LOGO}" width="240" alt="PERKS by ULTIMATE" style="display:block;width:240px;max-width:100%;height:auto;border:0"></td></tr>
<tr><td style="padding:36px 36px 8px;font-family:{F};color:#123B4A">{inner}</td></tr>
<tr><td align="center" style="padding:0 36px 28px"><a href="{{{{ .ConfirmationURL }}}}" style="display:inline-block;background:#00ADBC;color:#FFFFFF;font-family:{FD};font-weight:900;font-size:16px;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;padding:16px 32px;border-radius:14px">{btn}</a></td></tr>
<tr><td style="padding:0 36px 32px;font-family:{F};font-size:15px;line-height:1.6;color:#43484A">{note}</td></tr>
<tr><td style="background:#123B4A;padding:20px 36px;font-family:{F};font-size:13px;line-height:1.5;color:#CFE9E6">Traveller Perks by ULTIMATE &middot; <a href="https://perks.ultimate.travel" style="color:#FFFFFF;text-decoration:underline">perks.ultimate.travel</a><br>Questions? Write to <a href="mailto:info@ultimate.travel" style="color:#FFFFFF;text-decoration:underline">info@ultimate.travel</a></td></tr>
</table></td></tr></table></body></html>'''

def h1(t): return f'<h1 style="margin:0 0 16px;font-family:{FD};font-weight:900;font-size:30px;line-height:1.05;text-transform:uppercase;color:#123B4A">{t}</h1>'
def p(t): return f'<p style="margin:0 0 24px;font-size:17px;line-height:1.6;color:#43484A">{t}</p>'
B = lambda t: f'<b style="color:#123B4A">{t}</b>'

# Team welcome copy is switched on by user metadata set when an admin clicks Give access.
team = ('{{ if .Data.perks_admin }}' + h1('Welcome to the team') + p(f'You now have {B("admin access")} to Traveller Perks. Tap the button to sign in and you will go straight to the admin.')
      + '{{ else if .Data.perks_venue }}' + h1('Welcome to Perks') + p(f'You can now manage {B("{{ .Data.perks_venue }}")} on Traveller Perks: your offers, opening hours and photos. Tap the button to sign in.')
      + '{{ else }}')
note = 'This link works once and expires in 1 hour. If you did not ask for it, you can ignore this email.'

T = {
 'confirm-signup': ('Welcome to Traveller Perks',
    shell('Welcome to Traveller Perks', team + h1('Welcome to Perks') + p('Your East Coast traveller club is ready. Tap the button to confirm your email and sign in.') + '{{ end }}', 'Sign in to Perks', note)),
 'magic-link': ('Your Traveller Perks sign-in link',
    shell('Your sign-in link', team + h1('Your sign-in link') + p('Tap the button to sign in to Traveller Perks. No password needed.') + '{{ end }}', 'Sign in to Perks', note)),
 'invite': ('You are invited to Traveller Perks',
    shell('You are invited', team + h1('You are invited') + p('You have been invited to Traveller Perks. Tap the button to accept and sign in.') + '{{ end }}', 'Accept invite', 'This link expires in 24 hours.')),
 'change-email': ('Confirm your new email for Traveller Perks',
    shell('Confirm your new email', h1('Confirm your new email') + p(f'Tap the button to change your Traveller Perks email from {B("{{ .Email }}")} to {B("{{ .NewEmail }}")}.'), 'Confirm new email', 'If you did not ask for this, write to info@ultimate.travel.')),
 'reset-password': ('Reset your Traveller Perks password',
    shell('Reset your password', h1('Reset your password') + p('Tap the button to choose a new password for Traveller Perks.'), 'Reset password', note)),
}
meta = {}
for k,(subj,html) in T.items():
    open(os.path.join(OUT, k + '.html'), 'w').write(html)
    meta[k] = subj
open(os.path.join(OUT, 'subjects.json'), 'w').write(json.dumps(meta, indent=2))
print('built', list(T))
