// Builds the static site into dist/:
//   dist/index.html        perks.ultimate.travel (venue site)
//   dist/app/index.html    traveller web app
//   dist/admin/index.html  venue portal and Perks admin
// Env: SUPABASE_URL, SUPABASE_ANON_KEY (both public-safe). Without them the pages run in demo mode.
import fs from 'node:fs';
import path from 'node:path';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const r = p => fs.readFileSync(path.join(root, p));
const out = path.join(root, 'dist');
fs.rmSync(out, { recursive: true, force: true });
for (const d of ['', 'app', 'admin', 'assets', 'assets/fonts']) fs.mkdirSync(path.join(out, d), { recursive: true });

const json = s => s.replace(/<\//g, '<\\/');
const logo = r('assets/logo-white.png').toString('base64');
const fonts = Object.fromEntries(['500', '700', '900'].map(w => [w, r(`assets/fonts/work-sans-latin-${w}-normal.woff2`).toString('base64')]));
const appData = r('data/app-data.json').toString();
const adminData = r('data/admin-data.json').toString();
const auLand = r('assets/au-east.json').toString().trim();

const fill = (tpl, data) => {
  let t = r(tpl).toString()
    .replace('__DATA__', json(data))
    .replace(/__LOGO__/g, logo)
    .replace('__AULAND__', auLand);
  for (const [w, b] of Object.entries(fonts)) t = t.split(`__WS${w}__`).join(b);
  return t;
};
fs.writeFileSync(path.join(out, 'index.html'), fill('src/site.html', adminData));
fs.writeFileSync(path.join(out, 'app/index.html'), fill('src/app.html', appData));
fs.writeFileSync(path.join(out, 'admin/index.html'), fill('src/admin.html', adminData));
fs.copyFileSync(path.join(root, 'src/auth.js'), path.join(out, 'auth.js'));
fs.writeFileSync(path.join(out, 'config.js'),
  `window.PERKS_CONFIG=${JSON.stringify({ supabaseUrl: process.env.SUPABASE_URL || '', supabaseAnonKey: process.env.SUPABASE_ANON_KEY || '' })};\n`);
fs.copyFileSync(path.join(root, 'assets/logo-white.png'), path.join(out, 'assets/logo-white.png'));
for (const f of fs.readdirSync(path.join(root, 'assets/fonts'))) fs.copyFileSync(path.join(root, 'assets/fonts', f), path.join(out, 'assets/fonts', f));
fs.writeFileSync(path.join(out, 'app/manifest.webmanifest'), JSON.stringify({
  name: 'Traveller Perks', short_name: 'Perks', start_url: '/app/', scope: '/app/', display: 'standalone',
  background_color: '#4ECAC2', theme_color: '#4ECAC2',
  icons: [{ src: '/assets/logo-white.png', sizes: '900x160', type: 'image/png' }],
}, null, 2));
fs.writeFileSync(path.join(out, '404.html'), '<!doctype html><meta charset="utf-8"><title>Not found</title><p style="font-family:sans-serif">Page not found. <a href="/">Go to Traveller Perks</a></p>');
const size = f => (fs.statSync(path.join(out, f)).size / 1024).toFixed(0) + ' KB';
console.log('Built dist/', ['index.html', 'app/index.html', 'admin/index.html'].map(f => `${f} ${size(f)}`).join(', '),
  process.env.SUPABASE_URL ? '(live sign-in on)' : '(demo mode: no Supabase keys)');
