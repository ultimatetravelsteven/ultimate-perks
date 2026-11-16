-- Traveller Perks: team access (admins and venue owners)
-- An admin adds an email and a role. If that person already has an account they get access
-- straight away; if not, they get it automatically the first time they sign in.

alter table public.profiles add column if not exists venue_ref text;   -- venue id used by the admin app

create table if not exists public.team_invites (
  email text primary key check (email = lower(email)),
  name text,
  role text not null check (role in ('admin','venue')),
  venue_ref text,
  venue_name text,
  invited_by uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  accepted_at timestamptz
);
alter table public.team_invites enable row level security;
drop policy if exists "admin manage invites" on public.team_invites;
create policy "admin manage invites" on public.team_invites for all using (public.is_admin()) with check (public.is_admin());

-- New sign-ups pick up any waiting invite
create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
declare inv public.team_invites;
begin
  select * into inv from public.team_invites where email = lower(new.email);
  insert into public.profiles (id, email, name, role, venue_ref)
  values (new.id, lower(new.email),
          coalesce(inv.name, new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name'),
          coalesce(inv.role, 'traveller'), inv.venue_ref);
  if inv.email is not null then
    update public.team_invites set accepted_at = now() where email = inv.email;
  end if;
  return new;
end $$;

-- Admin adds or changes someone's access
create or replace function public.grant_team_access(p_email text, p_role text, p_name text default null,
                                                    p_venue_ref text default null, p_venue_name text default null)
returns text language plpgsql security definer set search_path = public as $$
declare e text := lower(trim(p_email)); hit int;
begin
  if not public.is_admin() then raise exception 'Only admins can add team members'; end if;
  if e !~ '^[^@\s]+@[^@\s]+\.[^@\s]+$' then raise exception 'That email does not look right'; end if;
  if p_role not in ('admin','venue') then raise exception 'Role must be admin or venue'; end if;
  if p_role = 'venue' and coalesce(p_venue_ref,'') = '' then raise exception 'Pick the venue for this owner'; end if;
  insert into public.team_invites (email, name, role, venue_ref, venue_name, invited_by)
  values (e, nullif(trim(p_name),''), p_role, case when p_role='venue' then p_venue_ref end,
          case when p_role='venue' then p_venue_name end, auth.uid())
  on conflict (email) do update set name = excluded.name, role = excluded.role, venue_ref = excluded.venue_ref,
          venue_name = excluded.venue_name, invited_by = excluded.invited_by;
  update public.profiles set role = p_role,
         venue_ref = case when p_role='venue' then p_venue_ref end,
         name = coalesce(nullif(trim(p_name),''), name)
   where lower(email) = e;
  get diagnostics hit = row_count;
  if hit > 0 then
    update public.team_invites set accepted_at = coalesce(accepted_at, now()) where email = e;
    return 'active';
  end if;
  return 'waiting';
end $$;

-- Admin removes someone's access (they keep a normal traveller account)
create or replace function public.revoke_team_access(p_email text)
returns void language plpgsql security definer set search_path = public as $$
declare e text := lower(trim(p_email));
begin
  if not public.is_admin() then raise exception 'Only admins can remove team members'; end if;
  if e = (select lower(email) from public.profiles where id = auth.uid()) then
    raise exception 'You cannot remove your own access';
  end if;
  delete from public.team_invites where email = e;
  update public.profiles set role = 'traveller', venue_ref = null where lower(email) = e;
end $$;

-- Team list for the admin page: everyone with access plus anyone still waiting to sign in
create or replace function public.team_list()
returns table (email text, name text, role text, venue_ref text, venue_name text, status text, added timestamptz)
language sql security definer set search_path = public stable as $$
  select p.email, p.name, p.role, p.venue_ref, i.venue_name, 'active', coalesce(i.created_at, p.created_at)
    from public.profiles p left join public.team_invites i on i.email = lower(p.email)
   where public.is_admin() and p.role in ('admin','venue')
  union all
  select i.email, i.name, i.role, i.venue_ref, i.venue_name, 'waiting', i.created_at
    from public.team_invites i
   where public.is_admin() and not exists (select 1 from public.profiles p where lower(p.email) = i.email)
  order by 6, 3, 1;
$$;

revoke all on function public.grant_team_access(text,text,text,text,text) from public, anon;
revoke all on function public.revoke_team_access(text) from public, anon;
revoke all on function public.team_list() from public, anon;
grant execute on function public.grant_team_access(text,text,text,text,text) to authenticated;
grant execute on function public.revoke_team_access(text) to authenticated;
grant execute on function public.team_list() to authenticated;
