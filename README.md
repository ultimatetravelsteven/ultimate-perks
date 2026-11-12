# Traveller Perks

One repo for the whole Perks product:

| Address | What it is | Source |
|---|---|---|
| perks.ultimate.travel | Venue website: pricing, sign-up, venue sign in | `src/site.html` |
| perks.ultimate.travel/app | Traveller web app: perks, activities, saved | `src/app.html` |
| perks.ultimate.travel/admin | Venue portal and Perks admin | `src/admin.html` |

Later the `/app` web app gets wrapped for the Apple App Store and Google Play.

## How it fits together

- **Hosting:** DigitalOcean App Platform static site (`.do/app.yaml`). Every push to `main` rebuilds and redeploys.
- **Sign-in and database:** Supabase. Google, Facebook, Apple and email-link sign-in. Schema in `supabase/migrations/`.
- **Bookable activities:** Hero widgets (one widget per product, Widget branch). List in `data/hero-widgets.csv`, full details in `data/hero-activity-details.json`.
- **Demo mode:** with no Supabase keys the pages work exactly like the test version, so nothing breaks while accounts are being set up.

## Build

```
npm run build      # writes dist/
npm run serve      # look at it on http://localhost:5173
```

## Setting up the accounts (one time)

### 1. Supabase
1. Sign up at supabase.com with steven@ultimate.travel. New project: name `ultimate-perks`, region **Sydney**, save the database password somewhere safe.
2. SQL Editor > New query > paste all of `supabase/migrations/0001_init.sql` > Run.
3. Project Settings > API: copy the **Project URL** and **anon public** key (these go into DigitalOcean). The **service_role** key is secret: only use it on your own computer for `npm run seed`.
4. Authentication > URL Configuration: Site URL `https://perks.ultimate.travel`, Redirect URLs `https://perks.ultimate.travel/app/` and `https://perks.ultimate.travel/admin/`.
5. Authentication > Providers: turn on Google, Facebook and Apple (steps below).
6. Make yourself admin: Table Editor > profiles > your row > role = `admin` (after you have signed in once).

### 2. Google sign-in
Google Cloud Console (tcpgroup.com.au org) > APIs and Services > Credentials > Create OAuth client ID > Web application. Authorised redirect URI: the callback URL shown on Supabase's Google provider page. Paste the Client ID and Secret into Supabase.

### 3. Facebook sign-in
developers.facebook.com > Create App > Consumer > add Facebook Login. Valid OAuth redirect URI: the Supabase callback URL. Paste App ID and App Secret into Supabase. Switch the app to Live.

### 4. Apple sign-in
Needs the Apple Developer Program ($99 USD a year). Create a Services ID and a Sign in with Apple key, then paste them into Supabase. Also needed for the App Store.

### 5. DigitalOcean
Apps > Create App > GitHub > `ultimate-perks` (it reads `.do/app.yaml`). Add the two environment variables `SUPABASE_URL` and `SUPABASE_ANON_KEY`. Domain: `perks.ultimate.travel`, then add the CNAME record DigitalOcean shows you at your DNS provider.

### 6. Load the data
On your computer, with the service key:
```
SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... npm run seed
```

## Still to build
- App and admin reading and writing Supabase (now: built-in data plus sign-in)
- eWay live payments (Supabase Edge Function)
- Nightly Hero sync for activity prices and dates
- Push notifications
- App Store and Google Play packaging (Capacitor)
