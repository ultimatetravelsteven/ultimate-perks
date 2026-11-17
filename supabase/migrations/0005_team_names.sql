-- Admins can set the display name for anyone on the team (active or waiting)
create or replace function public.set_team_name(p_email text, p_name text)
returns void language plpgsql security definer set search_path = public as $$
declare e text := lower(trim(p_email)); n text := nullif(trim(p_name),'');
begin
  if not public.is_admin() then raise exception 'Only admins can change names'; end if;
  update public.profiles set name = n where lower(email) = e;
  update public.team_invites set name = n where email = e;
end $$;
revoke all on function public.set_team_name(text,text) from public, anon;
grant execute on function public.set_team_name(text,text) to authenticated;
