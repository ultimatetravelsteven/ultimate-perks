// Loads the test-app data into Supabase (towns, brands, venues, offers, activities).
// Run once on your computer:  SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... npm run seed
import fs from 'node:fs';
const URL = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!URL || !KEY) { console.error('Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY first.'); process.exit(1); }
const d = JSON.parse(fs.readFileSync(new globalThis.URL('../data/app-data.json', import.meta.url)));
const up = async (table, rows, conflict) => {
  for (let i = 0; i < rows.length; i += 200) {
    const res = await fetch(`${URL}/rest/v1/${table}?on_conflict=${conflict}`, {
      method: 'POST',
      headers: { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json', Prefer: 'resolution=merge-duplicates,return=representation' },
      body: JSON.stringify(rows.slice(i, i + 200)),
    });
    if (!res.ok) throw new Error(`${table}: ${res.status} ${await res.text()}`);
    if (i === 0) var first = await res.json(); else await res.json();
  }
  console.log(`${table}: ${rows.length}`);
  return first;
};
const towns = Object.entries(d.towns).map(([id, t], i) => ({ id, name: t.name, lat: t.lat, lon: t.lon, photo: t.photo || null, sort: i, guide: { free: t.free || [], events: t.events || [] } }));
await up('towns', towns, 'id');
await up('brands', (d.brands || []).map(b => ({ id: b.id, name: b.name, category: b.category, logo: b.logo, photo: b.photo })), 'id');
const venues = d.perks.map(p => ({
  legacy_id: p.id, name: p.name, town_id: p.town, brand_id: p.brand || null, category: p.cat,
  status: p.prospect ? 'prospect' : 'live', address: p.addr, lat: p.lat, lon: p.lon, hours: p.hours,
  logo: p.logo === '@brand' ? null : p.logo, photos: (p.photos || []).filter(x => x && x !== '@brand'),
}));
await up('venues', venues, 'legacy_id');
const res = await fetch(`${URL}/rest/v1/venues?select=id,legacy_id`, { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } });
const map = Object.fromEntries((await res.json()).map(v => [v.legacy_id, v.id]));
const offers = d.perks.flatMap(p => (p.offers || [{ t: p.offer }]).map((o, i) => ({ venue_id: map[p.id], title: o.t, terms: p.terms || null, sort: i })));
await fetch(`${URL}/rest/v1/offers?venue_id=not.is.null`, { method: 'DELETE', headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } });
await up('offers', offers, 'id');
await up('activities', (d.acts || []).map(a => ({ id: a.id, town_id: a.town, widget_code: a.code, supplier: a.sup, title: a.title, duration: a.dur, start_location: a.loc, price_from: a.price, image: a.img, details: a.x || {} })), 'id');
console.log('Done.');
