"""
Middleware for the Swahilipot Hub Staff Portal.

1. ReplitCsrfMiddleware  — extends Django's CsrfViewMiddleware to trust any
   Replit preview / production origin at any subdomain depth.  Django's own
   wildcard matching only covers ONE level, so "*.kirk.replit.dev" won't match
   "abc-00-xyz.kirk.replit.dev".  This class adds the exact origin to the
   CSRF_TRUSTED_ORIGINS list on first encounter, so every Replit URL is
   accepted automatically.

2. SingleLoginMiddleware — expires older sessions when the same user logs in
   from a second device or browser.
"""

from urllib.parse import urlparse

from django.contrib.auth import logout
from django.contrib import messages
from django.middleware.csrf import CsrfViewMiddleware

# ── 1. Replit-aware CSRF middleware ───────────────────────────────────────

_REPLIT_SUFFIXES = (".replit.dev", ".replit.app", ".repl.co", ".replit.co")


class ReplitCsrfMiddleware(CsrfViewMiddleware):
    """CsrfViewMiddleware extended to trust all Replit preview/production origins.

    On the first request from any new Replit subdomain the exact origin is
    added to settings.CSRF_TRUSTED_ORIGINS so subsequent requests from the
    same origin pass Django's built-in check without any further patching.
    """

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # Collect the request origin (fall back to Referer if Origin absent)
        raw = request.META.get("HTTP_ORIGIN", "") or request.META.get("HTTP_REFERER", "")
        if raw:
            try:
                parsed = urlparse(raw)
                host = parsed.hostname or ""
                if any(host.endswith(suffix) for suffix in _REPLIT_SUFFIXES):
                    trusted = f"{parsed.scheme}://{parsed.netloc}"
                    from django.conf import settings as _s
                    if trusted not in _s.CSRF_TRUSTED_ORIGINS:
                        _s.CSRF_TRUSTED_ORIGINS.append(trusted)
            except Exception:
                pass

        return super().process_view(request, callback, callback_args, callback_kwargs)


# ── 2. Single-login enforcement ───────────────────────────────────────────

# URL paths that must never trigger a forced logout — these are short-lived
# POST requests where kicking the session mid-flight would silently drop the
# attendance record.
_EXEMPT_PATHS = {
    "/attendance/check-in/",
    "/attendance/check-out/",
    "/attendance/geofence-ping/",
    "/attendance/location-status/",
}


class SingleLoginMiddleware:
    """Expire any earlier session when the same user logs in elsewhere.

    Attendance write endpoints are exempted so that a phone check-in is not
    silently discarded when the same user is simultaneously logged in on a
    desktop browser.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip enforcement for attendance write operations so a phone check-in
        # is never silently dropped mid-flight.
        if request.path in _EXEMPT_PATHS:
            return self.get_response(request)

        if (
            request.user.is_authenticated
            and hasattr(request.user, "last_session_key")
            and request.user.last_session_key
            and request.session.session_key
            and request.user.last_session_key != request.session.session_key
        ):
            # A newer session exists for this user — invalidate the current one
            logout(request)
            messages.warning(
                request,
                "You have been signed out because your account was logged in from another device or browser.",
            )
            from django.shortcuts import redirect
            return redirect("login")

        response = self.get_response(request)
        return response
