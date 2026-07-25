# MIDEX card — PythonAnywhere deployment

## What this is
A Django site with one editable record (`BusinessCard`). The live card page
and the downloadable PDF both render from that same record, so anything you
change in the admin shows up in both places immediately — nothing to sync
by hand.

- Public page: `/`
- Admin: `/admin/`  (also reachable via `/midex-django-admin/`, which
  redirects to `/admin/`)

## 1. Get the code onto PythonAnywhere
Upload this folder (zip it, upload via the Files tab, then unzip in a Bash
console — `unzip midex_django.zip`), or push it to GitHub and `git clone` it
from a Bash console.

## 2. Create a virtualenv and install dependencies
In a PythonAnywhere Bash console:

```
cd midex_django
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Set required environment variables
Don't deploy with the placeholder secret key. In the **Web** tab, under
"Environment variables", add:

- `DJANGO_SECRET_KEY` — any long random string
- `DJANGO_DEBUG` — `False`
- `DJANGO_ALLOWED_HOSTS` — `yourusername.pythonanywhere.com`

## 4. Configure the Web app
In the **Web** tab:
- Create a new web app → **Manual configuration** → your Python version.
- Set the virtualenv path to `/home/yourusername/midex_django/venv`.
- Edit the WSGI file it generated so it points at this project:

```python
import sys
path = '/home/yourusername/midex_django'
if path not in sys.path:
    sys.path.append(path)

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midexsite.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

- Under **Static files**, add:
  - URL `/static/` → Directory `/home/yourusername/midex_django/staticfiles`
  - URL `/media/` → Directory `/home/yourusername/midex_django/media`

## 5. Run migrations, collect static files, create your admin login

```
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

Follow the prompts to set your admin username/password.

## 6. Reload
Hit the green **Reload** button in the Web tab, then visit:
`https://yourusername.pythonanywhere.com/midex-django-admin/`

Log in and edit the one "Business card" record — company details, contact
info, address, and optionally a new logo. Save, then check
`https://yourusername.pythonanywhere.com/` — the change is live
immediately, and the next PDF download reflects it too.

## Notes
- Only one card record can exist — the admin is deliberately locked to
  editing that single record (no add/delete), since this is a one-person
  business card, not a list of cards.
- The card offers a single action: "Download Card (PDF)". There is no QR
  code and no vCard/"Save Contact" download in this build.

