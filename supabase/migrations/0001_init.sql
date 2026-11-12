-- Traveller Perks: first database schema
-- Run in Supabase: SQL editor > paste > Run (or `supabase db push`).

create extension if not exists "pgcrypto";

-- ---------- people ----------
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text,
  name text,
  role text not null default 'traveller' check (role in ('traveller','venue','admin')),
  venue_id uuid,
  booking_ref text,
  home_country text,
  push_token text,
  created_at timestamptz not null default now()
);

-- every new sign-in gets a profile row (traveller by default)
create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, email, name)
  values (new.id, new.email, coalesce(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name'));
  return new;
end $$;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

create or replace function public.is_admin() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.profiles where id = auth.uid() and role = 'admin');
$$;

-- ---------- places ----------
create table public.towns (
  id text primary key,                -- e.g. 'sydney'
  name text not null,
  lat double precision, lon double precision,
  photo text,
  sort int default 0,
  guide jsonb default '{}'::jsonb     -- free things to do, what's on
);

create table public.brands (
  id text primary key,                -- e.g. 'guzman-y-gomez'
  name text not null,
  category text,
  logo text, photo text,
  created_at timestamptz default now()
);

create table public.venues (
  id uuid primary key default gen_random_uuid(),
  legacy_id int unique,               -- id from the test app
  name text not null,
  town_id text references public.towns(id),
  brand_id text references public.brands(id),
  category text,                      -- Bar, Restaurant, Activity
  status text not null default 'pending' check (status in ('live','pending','prospect','draft','expired','suspended')),
  address text, lat double precision, lon double precision,
  hours jsonb, website text, contact jsonb,
  logo text, photos text[] default '{}',
  listing_until date,
  featured_until date,
  offer_packs int default 0,
  booking jsonb,                      -- widget or tracked link
  created_at timestamptz default now()
);
alter table public.profiles add constraint profiles_venue_fk foreign key (venue_id) references public.venues(id) on delete set null;

create table public.offers (
  id uuid primary key default gen_random_uuid(),
  venue_id uuid not null references public.venues(id) on delete cascade,
  title text not null,
  terms text,
  flash_until timestamptz,            -- set for flash deals
  active boolean default true,
  sort int default 0,
  created_at timestamptz default now()
);

-- ---------- bookable activities (Hero widgets) ----------
create table public.activities (
  id int primary key,                 -- Hero product id
  town_id text references public.towns(id),
  widget_code text not null,          -- e.g. WC-KG5396
  supplier text, title text not null,
  duration text, start_location text,
  price_from numeric(10,2),
  image text,
  details jsonb default '{}'::jsonb,  -- about, photos, times, meeting point, cancellation
  active boolean default true,
  synced_at timestamptz default now()
);

-- ---------- traveller activity ----------
create table public.saves (
  user_id uuid references auth.users(id) on delete cascade,
  venue_id uuid references public.venues(id) on delete cascade,
  created_at timestamptz default now(),
  primary key (user_id, venue_id)
);

create table public.redemptions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete set null,
  venue_id uuid references public.venues(id) on delete cascade,
  offer_id uuid references public.offers(id) on delete set null,
  code text,
  created_at timestamptz default now()
);

create table public.events (           -- taps, views, booking clicks
  id bigint generated always as identity primary key,
  user_id uuid, venue_id uuid, activity_id int,
  kind text not null,                 -- view, save, directions, book_click, booked
  meta jsonb,
  created_at timestamptz default now()
);

create table public.reviews (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete set null,
  venue_id uuid references public.venues(id) on delete cascade,
  rating int check (rating between 1 and 5),
  body text,
  created_at timestamptz default now()
);

-- ---------- money ----------
create table public.payments (
  id uuid primary key default gen_random_uuid(),
  venue_id uuid references public.venues(id) on delete set null,
  kind text,                          -- listing, push, featured, extra_location, offer_pack
  amount_cents int not null,
  status text default 'pending',      -- pending, paid, failed, refunded
  eway_txn text,
  promo_code text,
  created_at timestamptz default now()
);

create table public.pushes (
  id uuid primary key default gen_random_uuid(),
  venue_id uuid references public.venues(id) on delete set null,
  town_id text references public.towns(id),
  title text, body text,
  send_at timestamptz,
  status text default 'scheduled',
  sent_count int default 0,
  created_at timestamptz default now()
);

create table public.settings (
  key text primary key,
  value jsonb
);
insert into public.settings (key, value) values
  ('prices', '{"listing":299,"push":99,"featuredWeek":79,"extraLocation":99,"offerPack":49}'::jsonb),
  ('promo_codes', '[{"code":"PERKS6FREE","months":6}]'::jsonb);

-- ---------- row level security ----------
alter table public.profiles enable row level security;
alter table public.towns enable row level security;
alter table public.brands enable row level security;
alter table public.venues enable row level security;
alter table public.offers enable row level security;
alter table public.activities enable row level security;
alter table public.saves enable row level security;
alter table public.redemptions enable row level security;
alter table public.events enable row level security;
alter table public.reviews enable row level security;
alter table public.payments enable row level security;
alter table public.pushes enable row level security;
alter table public.settings enable row level security;

-- public read of what the app shows
create policy "read towns" on public.towns for select using (true);
create policy "read brands" on public.brands for select using (true);
create policy "read live venues" on public.venues for select using (status in ('live','prospect') or public.is_admin() or id = (select venue_id from public.profiles where id = auth.uid()));
create policy "read offers" on public.offers for select using (true);
create policy "read activities" on public.activities for select using (active or public.is_admin());
create policy "read prices" on public.settings for select using (key = 'prices' or public.is_admin());

-- own profile
create policy "own profile read" on public.profiles for select using (id = auth.uid() or public.is_admin());
create policy "own profile update" on public.profiles for update using (id = auth.uid()) with check (role = (select role from public.profiles where id = auth.uid()));

-- travellers
create policy "own saves" on public.saves for all using (user_id = auth.uid()) with check (user_id = auth.uid());
create policy "redeem" on public.redemptions for insert with check (user_id = auth.uid());
create policy "see own redemptions" on public.redemptions for select using (user_id = auth.uid() or public.is_admin() or venue_id = (select venue_id from public.profiles where id = auth.uid()));
create policy "log events" on public.events for insert with check (true);
create policy "write review" on public.reviews for insert with check (user_id = auth.uid());
create policy "read reviews" on public.reviews for select using (true);

-- venues manage their own listing and offers
create policy "venue edits own" on public.venues for update using (id = (select venue_id from public.profiles where id = auth.uid()) or public.is_admin());
create policy "venue offers" on public.offers for all using (venue_id = (select venue_id from public.profiles where id = auth.uid()) or public.is_admin())
  with check (venue_id = (select venue_id from public.profiles where id = auth.uid()) or public.is_admin());
create policy "venue payments read" on public.payments for select using (venue_id = (select venue_id from public.profiles where id = auth.uid()) or public.is_admin());
create policy "venue events read" on public.events for select using (venue_id = (select venue_id from public.profiles where id = auth.uid()) or public.is_admin());

-- admins do everything
create policy "admin all venues" on public.venues for all using (public.is_admin()) with check (public.is_admin());
create policy "admin all towns" on public.towns for all using (public.is_admin()) with check (public.is_admin());
create policy "admin all brands" on public.brands for all using (public.is_admin()) with check (public.is_admin());
create policy "admin all activities" on public.activities for all using (public.is_admin()) with check (public.is_admin());
create policy "admin all profiles" on public.profiles for update using (public.is_admin());
create policy "admin all payments" on public.payments for all using (public.is_admin()) with check (public.is_admin());
create policy "admin all pushes" on public.pushes for all using (public.is_admin()) with check (public.is_admin());
create policy "admin all settings" on public.settings for all using (public.is_admin()) with check (public.is_admin());
create policy "admin all reviews" on public.reviews for delete using (public.is_admin());
