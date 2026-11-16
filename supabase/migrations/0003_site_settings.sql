-- Traveller Perks: public site settings (beta flag, show prospects)
insert into public.settings (key, value)
values ('site', '{"beta": true, "showProspects": false}'::jsonb)
on conflict (key) do nothing;

drop policy if exists "read prices" on public.settings;
create policy "read public settings" on public.settings for select
  using (key in ('prices', 'site') or public.is_admin());
