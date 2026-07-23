from pathlib import Path
import os

# ── Load .env file if it exists (no extra packages needed) ────────────────
# Uses direct os.environ assignment so .env values ALWAYS win over any
# stale values that might already be in the environment from a prior run.
_env_file = Path(__file__).resolve().parent.parent / ".env"
if _env_file.exists():
    for _line in _env_file.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _key, _, _val = _line.partition("=")
            _key = _key.strip()
            _val = _val.strip()
            # Always overwrite so the .env file is the single source of truth
            os.environ[_key] = _val

try:
    import dj_database_url
except ImportError:
    dj_database_url = None

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------
# Security Settings
# ------------------------------------------------------------------------------

# Debug mode
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() in {"1", "true", "yes"}

# Secret Key
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    if DEBUG:
        # Development fallback only
        SECRET_KEY = "dev-only-change-me"
    else:
        raise RuntimeError(
            "DJANGO_SECRET_KEY environment variable must be set in production."
        )

# Allowed Hosts
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if host.strip()
]

# Development tunnel
ALLOWED_HOSTS.append("oppose-shrink-speed.ngrok-free.dev")

# Local development
ALLOWED_HOSTS.extend([
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
])

# Remove duplicate entries
ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS))

# ── Replit hosting: automatically trust all *.replit.app / *.replit.dev domains
_replit_domains = os.getenv("REPLIT_DOMAINS", "")
for _d in _replit_domains.split(","):
    _d = _d.strip()
    if _d:
        ALLOWED_HOSTS.append(_d)

ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "attendance",
    "communication",
    "tasks",
    "events",
    "suggestions",
    "dashboard",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "core.middleware.ReplitCsrfMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # Single-login: must come after MessageMiddleware so messages.warning() works
    "core.middleware.SingleLoginMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "swahilipot_portal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
            "communication.context_processors.unread_notifications",
            "core.context_processors.site_settings",
        ]},
    }
]

WSGI_APPLICATION = "swahilipot_portal.wsgi.application"

if dj_database_url:
    DATABASES = {"default": dj_database_url.config(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}", conn_max_age=600)}
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard:home"
LOGOUT_REDIRECT_URL = "login"

# ── Email ─────────────────────────────────────────────────────────────────
# Set DJANGO_EMAIL_HOST_USER and DJANGO_EMAIL_HOST_PASSWORD in your .env file
# to enable real email sending (e.g. Gmail SMTP with an App Password).
#
# How to get a Gmail App Password (one-time setup):
#   1. Sign in to https://myaccount.google.com
#   2. Security → 2-Step Verification → turn ON if not already
#   3. Visit https://myaccount.google.com/apppasswords
#   4. Select Mail / Windows Computer → Generate
#   5. Copy the 16-char password → paste as DJANGO_EMAIL_HOST_PASSWORD in .env
#
# ── Testing email locally ─────────────────────────────────────────────────
# If DJANGO_EMAIL_HOST_USER / DJANGO_EMAIL_HOST_PASSWORD are NOT set in .env,
# the system automatically falls back to the CONSOLE backend.
#
# In console mode:
#   - No email is actually sent.
#   - The full password-reset email (including the reset link) is printed
#     directly to the terminal window where you ran `python manage.py runserver`.
#   - Copy the link from the terminal and paste it into your browser to
#     complete the password reset — it works exactly like a real email.
#
_email_user     = os.getenv("DJANGO_EMAIL_HOST_USER", "").strip()
_email_password = os.getenv("DJANGO_EMAIL_HOST_PASSWORD", "").strip()

EMAIL_HOST          = "smtp.gmail.com"
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_USE_SSL       = False
EMAIL_HOST_USER     = _email_user
EMAIL_HOST_PASSWORD = _email_password
DEFAULT_FROM_EMAIL  = (
    f"Swahilipot Hub Portal <{_email_user}>" if _email_user
    else "Swahilipot Hub Portal <noreply@swahilipothub.co.ke>"
)
SERVER_EMAIL = _email_user or "noreply@swahilipothub.co.ke"

# Use real SMTP only when both user and password are provided; otherwise console
if _email_user and _email_password:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
X_FRAME_OPTIONS = "DENY"

# ── CSRF trusted origins for reverse proxies (Cloudflare Tunnel, ngrok, etc.)
# Add your tunnel URL here, e.g. DJANGO_CSRF_TRUSTED_ORIGINS=https://abc.trycloudflare.com
_csrf_origins = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").strip()
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(",") if o.strip()]

# ── Replit: trust ALL *.replit.dev and *.replit.app preview/production domains
# This covers dev previews (*.replit.dev, *.kirk.replit.dev, etc.) and
# deployed production URLs (*.replit.app).
CSRF_TRUSTED_ORIGINS += [
    "https://*.replit.dev",
    "https://*.replit.app",
    "https://*.kirk.replit.dev",
    "https://*.repl.co",
]
ALLOWED_HOSTS += [".replit.dev", ".replit.app", ".kirk.replit.dev", ".repl.co"]

# Also add any domains explicitly listed in REPLIT_DOMAINS env var
for _d in _replit_domains.split(","):
    _d = _d.strip()
    if _d and _d not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_d)
        CSRF_TRUSTED_ORIGINS.append(f"https://{_d}")
        CSRF_TRUSTED_ORIGINS.append(f"http://{_d}")

# ── Site base URL (used for QR code generation when no HTTP request is available)
# Set this to the full public URL of your server, e.g. via ngrok:
#   DJANGO_SITE_BASE_URL=https://abc123.ngrok-free.app
# When running locally without ngrok: http://127.0.0.1:8000
SITE_BASE_URL = os.getenv("DJANGO_SITE_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

# ── Google Form integration ───────────────────────────────────────────────────
# Set these in your .env file — no code changes needed.
#
# GOOGLE_FORM_BASE_URL          — the /viewform URL of your Google Form
#   e.g. https://docs.google.com/forms/d/e/1FAIpQLSe.../viewform
#
# GOOGLE_FORM_EVENT_ID_FIELD    — entry.XXXXXXXXX key for your "Event ID" question
#   How to find it:
#     1. Open your Google Form
#     2. Click ⋮ (three dots) → "Get pre-filled link"
#     3. Type anything in the Event ID field → click "Get link"
#     4. Copy the URL — find the part ?entry.XXXXXXXXX=  and copy entry.XXXXXXXXX
#
# GOOGLE_FORM_EVENT_NAME_FIELD  — entry.YYYYYYYYY for an "Event Name" question (optional)
#
GOOGLE_FORM_BASE_URL         = os.getenv("GOOGLE_FORM_BASE_URL", "").strip()
GOOGLE_FORM_EVENT_ID_FIELD   = os.getenv("GOOGLE_FORM_EVENT_ID_FIELD", "").strip()
GOOGLE_FORM_EVENT_NAME_FIELD = os.getenv("GOOGLE_FORM_EVENT_NAME_FIELD", "").strip()

# ── Web Push (VAPID) ──────────────────────────────────────────────────────────
VAPID_PUBLIC_KEY  = os.getenv("VAPID_PUBLIC_KEY", "")
VAPID_MAILTO      = os.getenv("VAPID_MAILTO", "admin@swahilipothub.co.ke")

# ── Production security hardening (only when DEBUG=False) ─────────────────────
# Replit's proxy already handles HTTPS/TLS so we do NOT set SECURE_SSL_REDIRECT
# (it would cause infinite redirect loops behind the proxy).
if not DEBUG:
    SESSION_COOKIE_SECURE       = True
    CSRF_COOKIE_SECURE          = True
    SECURE_HSTS_SECONDS         = 31536000        # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
