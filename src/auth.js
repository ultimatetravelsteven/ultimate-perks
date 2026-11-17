// Traveller Perks shared sign-in (app and admin).
// Uses Supabase Auth when /config.js has a Supabase URL and key.
// With no keys set, window.PerksAuth.live is false and the pages run in demo mode.
const cfg = window.PERKS_CONFIG || {};
const live = !!(cfg.supabaseUrl && cfg.supabaseAnonKey);

const PerksAuth = {
  live,
  client: null,
  user: null,
  profile: null,
  _subs: [],
  onChange(fn) { this._subs.push(fn); if (this.user !== undefined) fn(this.user, this.profile); },
  _emit() { this._subs.forEach(fn => { try { fn(this.user, this.profile); } catch (e) { console.error(e); } }); },

  // provider: 'google' | 'facebook' | 'apple'
  async signIn(provider) {
    if (!live) throw new Error('Sign-in is not switched on yet');
    const { error } = await this.client.auth.signInWithOAuth({
      provider,
      options: { redirectTo: location.origin + location.pathname },
    });
    if (error) throw error;
  },
  // Email link sign-in (no password)
  async signInEmail(email) {
    if (!live) throw new Error('Sign-in is not switched on yet');
    const { error } = await this.client.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: location.origin + location.pathname },
    });
    if (error) throw error;
  },
  // Team welcome email: sends a branded sign-in link to someone just given access.
  // New accounts get the "Welcome to the team" version (perks_admin / perks_venue flags).
  async sendTeamEmail(email, role, venueName) {
    if (!live) throw new Error('Emails work on the live site');
    const { createClient } = await import('https://esm.sh/@supabase/supabase-js@2');
    const c = createClient(cfg.supabaseUrl, cfg.supabaseAnonKey, { auth: { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false, storageKey: 'perks-invite' } });
    const data = role === 'admin' ? { perks_admin: true } : { perks_venue: venueName || 'your venue' };
    const { error } = await c.auth.signInWithOtp({ email, options: { emailRedirectTo: location.origin + '/admin/', shouldCreateUser: true, data } });
    if (error) throw error;
  },
  async signOut() {
    if (live) await this.client.auth.signOut();
    this.user = null; this.profile = null; this._emit();
  },
  async loadProfile() {
    if (!this.user) { this.profile = null; return null; }
    const { data } = await this.client.from('profiles').select('*').eq('id', this.user.id).maybeSingle();
    this.profile = data || null;
    return this.profile;
  },
};
window.PerksAuth = PerksAuth;

if (live) {
  const { createClient } = await import('https://esm.sh/@supabase/supabase-js@2');
  PerksAuth.client = createClient(cfg.supabaseUrl, cfg.supabaseAnonKey, {
    auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true },
  });
  const { data } = await PerksAuth.client.auth.getSession();
  PerksAuth.user = data.session ? data.session.user : null;
  // Clear the one-time welcome flags so later sign-in emails use the normal copy
  const md = PerksAuth.user && PerksAuth.user.user_metadata || {};
  if (md.perks_admin || md.perks_venue) PerksAuth.client.auth.updateUser({ data: { perks_admin: null, perks_venue: null } }).catch(() => {});
  await PerksAuth.loadProfile();
  PerksAuth._emit();
  PerksAuth.client.auth.onAuthStateChange(async (_evt, session) => {
    PerksAuth.user = session ? session.user : null;
    await PerksAuth.loadProfile();
    PerksAuth._emit();
  });
} else {
  PerksAuth.user = null;
  PerksAuth._emit();
}
window.dispatchEvent(new Event('perksauth:ready'));
