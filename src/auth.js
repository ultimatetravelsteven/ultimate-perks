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
