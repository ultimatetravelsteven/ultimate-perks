-- Traveller Perks: venues and brands managed in admin, shared by app, website and admin.
-- The admin edits the full record (data jsonb). The public only ever reads safe fields
-- through public_venues() / public_brands(): no contacts, payment details, notes or stats.

create table if not exists public.perk_venues (
  id text primary key,
  status text not null default 'draft' check (status in ('live','pending','prospect','draft','expired','suspended')),
  town text,
  data jsonb not null,
  updated_at timestamptz not null default now(),
  updated_by uuid references auth.users(id) on delete set null
);
create table if not exists public.perk_brands (
  id text primary key,
  data jsonb not null,
  updated_at timestamptz not null default now()
);
alter table public.perk_venues enable row level security;
alter table public.perk_brands enable row level security;

create or replace function public.my_venue_ref() returns text
language sql stable security definer set search_path = public as $$
  select venue_ref from public.profiles where id = auth.uid();
$$;

create or replace function public.my_brand_id() returns text
language sql stable security definer set search_path = public as $$
  select nullif(v.data->>'brandId','') from public.perk_venues v where v.id = (select venue_ref from public.profiles where id = auth.uid());
$$;
create or replace function public.venue_status(p_id text) returns text
language sql stable security definer set search_path = public as $$
  select status from public.perk_venues where id = p_id;
$$;
grant execute on function public.my_brand_id() to authenticated;
grant execute on function public.venue_status(text) to authenticated;

-- admins: everything
drop policy if exists "admin venues" on public.perk_venues;
create policy "admin venues" on public.perk_venues for all using (public.is_admin()) with check (public.is_admin());
drop policy if exists "admin brands" on public.perk_brands;
create policy "admin brands" on public.perk_brands for all using (public.is_admin()) with check (public.is_admin());

-- venue owners: read and edit their own venue and the other locations of their brand; can't change status
drop policy if exists "owner reads venues" on public.perk_venues;
create policy "owner reads venues" on public.perk_venues for select using (
  id = public.my_venue_ref() or (public.my_brand_id() is not null and data->>'brandId' = public.my_brand_id()));
drop policy if exists "owner edits venues" on public.perk_venues;
create policy "owner edits venues" on public.perk_venues for update using (
  id = public.my_venue_ref() or (public.my_brand_id() is not null and data->>'brandId' = public.my_brand_id()))
  with check (status = public.venue_status(id));
drop policy if exists "owner reads brands" on public.perk_brands;
create policy "owner reads brands" on public.perk_brands for select using (auth.uid() is not null);

-- public, safe fields only; prospects only when admin > Settings > Show prospects is on
create or replace function public.public_venues()
returns setof jsonb language sql stable security definer set search_path = public as $$
  select jsonb_build_object(
    'id', v.id, 'status', v.status, 'town', v.town,
    'name', v.data->'name', 'cat', v.data->'cat', 'addr', v.data->'addr', 'lat', v.data->'lat', 'lon', v.data->'lon',
    'logo', v.data->'logo', 'photos', v.data->'photos', 'desc', v.data->'desc', 'web', v.data->'web', 'insta', v.data->'insta',
    'hours', v.data->'hours', 'hoursReal', v.data->'hoursReal', 'brandId', v.data->'brandId', 'featuredUntil', v.data->'featuredUntil',
    'booking', jsonb_build_object('mode', v.data->'booking'->'mode', 'url', v.data->'booking'->'url', 'provider', v.data->'booking'->'provider'),
    'offers', coalesce((select jsonb_agg(jsonb_build_object('t', o->'t', 'terms', o->'terms', 'when', o->'when', 'flashUntil', o->'flashUntil'))
                          from jsonb_array_elements(v.data->'offers') o where coalesce((o->>'paused')::boolean, false) = false), '[]'::jsonb))
  from public.perk_venues v
  where v.status = 'live'
     or (v.status = 'prospect' and coalesce((select (value->>'showProspects')::boolean from public.settings where key = 'site'), false));
$$;
create or replace function public.public_brands()
returns setof jsonb language sql stable security definer set search_path = public as $$
  select jsonb_build_object('id', b.id, 'name', b.data->'name', 'category', b.data->'category', 'offer', b.data->'offer',
                            'logo', b.data->'logo', 'photo', b.data->'photo')
  from public.perk_brands b;
$$;
grant execute on function public.public_venues() to anon, authenticated;
grant execute on function public.public_brands() to anon, authenticated;
grant execute on function public.my_venue_ref() to authenticated;
