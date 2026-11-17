// Traveller Perks site settings (beta flag, show prospects, free listing promo).
// Reads the public "site" row from Supabase settings. Admins change it in admin > Settings.
// Safe default if anything fails: no prospects shown, beta flag shown.
(function () {
  const cfg = window.PERKS_CONFIG || {};
  const DEF = { beta: true, showProspects: false, freePromo: true };
  window.PERKS_SITE = Object.assign({}, DEF, { loaded: false });

  function flag(on) {
    let el = document.getElementById('perks-beta-flag');
    if (!on) { if (el) el.remove(); return; }
    if (!el) {
      const st = document.createElement('style');
      st.textContent = '/* // CSS NAME: perks-beta-flag // */' +
        '#perks-beta-flag{position:fixed;right:14px;bottom:calc(14px + var(--beta-lift,0px));z-index:9999;display:flex;align-items:center;gap:8px;' +
        'background:#FF775E;color:#fff;font:900 13px/1 "Work Sans",system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;' +
        'padding:9px 14px;border-radius:999px;box-shadow:0 6px 18px rgba(18,59,74,.28);cursor:help;border:0}' +
        '#perks-beta-flag i{width:8px;height:8px;border-radius:50%;background:#fff;opacity:.9}' +
        '#perks-beta-flag[data-open] span.more{display:inline}#perks-beta-flag span.more{display:none;font-weight:700;letter-spacing:.02em;text-transform:none}';
      document.head.appendChild(st);
      el = document.createElement('button');
      el.type = 'button';
      el.id = 'perks-beta-flag';
      el.setAttribute('aria-label', 'Beta: testing mode only. Venues and deals may change.');
      el.innerHTML = '<i></i><span>Beta</span><span class="more">&middot; Testing mode only. Venues and deals may change.</span>';
      el.addEventListener('click', () => el.toggleAttribute('data-open'));
      document.body.appendChild(el);
    }
  }

  function apply(v) {
    window.PERKS_SITE = Object.assign({}, DEF, v || {}, { loaded: true });
    if (document.body) flag(window.PERKS_SITE.beta); else document.addEventListener('DOMContentLoaded', () => flag(window.PERKS_SITE.beta));
    window.dispatchEvent(new CustomEvent('perks:site', { detail: window.PERKS_SITE }));
  }
  window.PerksSiteApply = apply;

  if (document.body) flag(DEF.beta); else document.addEventListener('DOMContentLoaded', () => flag(DEF.beta));
  if (!cfg.supabaseUrl || !cfg.supabaseAnonKey) { apply(DEF); return; }
  const ctl = new AbortController(); setTimeout(() => ctl.abort(), 4000);
  fetch(cfg.supabaseUrl + '/rest/v1/settings?key=eq.site&select=value', {
    headers: { apikey: cfg.supabaseAnonKey, Authorization: 'Bearer ' + cfg.supabaseAnonKey }, signal: ctl.signal,
  }).then(r => r.ok ? r.json() : []).then(rows => apply(rows && rows[0] && rows[0].value)).catch(() => apply(DEF));
})();
