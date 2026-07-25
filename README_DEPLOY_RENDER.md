# MIDEX card — deploying to Render (with a free, always-persistent database)

This setup means: **set it up once, then never touch it again.** No monthly
login, no data getting wiped, no card required.

## Why a separate database at all?
Render's free web services wipe their local disk on every restart/redeploy,
and free services auto-restart after ~15 minutes idle. If we used the
default SQLite file, every admin edit would get quietly reset. So the
database lives on a separate, always-on free service instead (Neon or
Supabase), while Render just runs the Django code.

## 1. Create a free Postgres database (Neon)
1. Go to neon.tech → sign up (no card needed) → create a project.
2. Copy the connection string it gives you — looks like:
   `postgresql://user:password@host/dbname?sslmode=require`
   (Supabase works the same way if you'd rather use that instead.)

## 2. Push this code to GitHub
Render deploys from a Git repo. Create a repo, push this folder to it.

## 3. Deploy on Render
1. render.com → sign up (no card needed for the free tier) → New →
   **Blueprint** → connect your GitHub repo. Render reads `render.yaml`
   automatically and sets up the service.
2. In the service's **Environment** tab, paste your Neon connection string
   into `DATABASE_URL`.
3. Once it's live, note your URL, e.g. `midex-card.onrender.com`, and make
   sure `DJANGO_ALLOWED_HOSTS` covers it (the default `.onrender.com` in
   render.yaml already does).

## 4. Create your admin login
Render dashboard → your service → **Shell** tab:
```
python manage.py createsuperuser
```

## 5. Visit it
- Site: `https://midex-card.onrender.com/`
- Admin: `https://midex-card.onrender.com/admin/`

## 6. Keep it awake — no more manual visits, ever
Render's free service sleeps after ~15 min with no traffic; the next
visitor then waits ~30–50 seconds while it wakes up. To avoid that, use a
free "keep-alive" pinger — a robot that visits your site automatically so
Render never sees it go idle:

1. Go to **cron-job.org** (or **UptimeRobot** — either works) → sign up free.
2. Create a new cron job / monitor:
   - URL: `https://midex-card.onrender.com/`
   - Interval: every 10 minutes
3. Save it. That's the whole setup — it runs forever in the background,
   no card, no login needed from you again.

## Result
- Data: safe forever (lives on Neon, untouched by Render restarts)
- Uptime: always awake (kept alive by the free pinger)
- Your time after today: zero
