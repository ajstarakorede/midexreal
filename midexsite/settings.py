import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# SECURITY
# Before you deploy: set a real secret key and turn DEBUG off.
# On Render / PythonAnywhere, set these as environment variables in their
# dashboard rather than editing this file.
# ---------------------------------------------------------------------------
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-key-change-this-before-going-live-!!!",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# e.g. "yourapp.onrender.com" or "yourusername.pythonanywhere.com"
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost"
).split(",")

# Render (and most PaaS hosts) terminate HTTPS at a proxy in front of the
# app, then forward plain HTTP internally. Without these two settings,
# Django doesn't realize the original request was secure, which makes its
# CSRF check fail on any form submission (like saving in the admin) —
# that's what was causing the "server error" when editing.
CSRF_TRUSTED_ORIGINS = [
    ("https://*." + host.lstrip(".")) if host.startswith(".") else ("https://" + host)
    for host in ALLOWED_HOSTS
    if host not in ("127.0.0.1", "localhost")
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "card",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serves static files on Render
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "midexsite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "midexsite.wsgi.application"

# ---------------------------------------------------------------------------
# Database
# - If a DATABASE_URL environment variable is set (Render + Neon/Supabase
#   Postgres), use that — this is what makes your data survive Render's
#   free-tier restarts and redeploys.
# - Otherwise (local dev, or PythonAnywhere), fall back to a local SQLite
#   file, same as before.
# ---------------------------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # populated by collectstatic for deploy
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# NOTE: on Render's free tier, MEDIA_ROOT (admin-uploaded logo) is on the
# ephemeral filesystem just like SQLite would be — it will be wiped on
# restarts/redeploys too. That's fine for now since the logo has a static
# fallback built into the template. If the client uploads a custom logo
# and it needs to survive long-term on Render, that would need an external
# file store (e.g. Cloudinary's free tier) — say the word if you want that
# wired up too.
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
