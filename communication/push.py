"""
Web Push helper — sends a push notification to all of a user's subscriptions.
Uses pywebpush + VAPID for authenticated delivery.
"""
import json
import logging
import os

logger = logging.getLogger(__name__)

_PRIVATE_KEY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "vapid_private.pem",
)


def _vapid_claims():
    mailto = os.getenv("VAPID_MAILTO", "admin@swahilipothub.co.ke")
    return {"sub": f"mailto:{mailto}"}


def send_push(user, title, body, link="/", priority="low", tag="sph-notification"):
    """
    Send a web push to every browser subscription the user has registered.
    Silently skips if pywebpush is unavailable or no subscriptions exist.
    """
    try:
        from pywebpush import webpush, WebPushException
        from .models import PushSubscription
    except ImportError:
        return

    if not os.path.exists(_PRIVATE_KEY_PATH):
        return

    payload = json.dumps({
        "title": title,
        "body": body,
        "link": link,
        "priority": priority,
        "tag": tag,
    })

    subs = PushSubscription.objects.filter(user=user)
    dead = []

    for sub in subs:
        try:
            webpush(
                subscription_info=sub.as_dict(),
                data=payload,
                vapid_private_key=_PRIVATE_KEY_PATH,
                vapid_claims=_vapid_claims(),
                ttl=86400,
            )
        except WebPushException as exc:
            status = getattr(exc.response, "status_code", None)
            if status in (404, 410):
                dead.append(sub.pk)
            else:
                logger.warning("WebPush failed for user %s: %s", user, exc)
        except Exception as exc:
            logger.warning("WebPush error for user %s: %s", user, exc)

    if dead:
        PushSubscription.objects.filter(pk__in=dead).delete()


def send_push_bulk(users, title, body, link="/", priority="low", tag="sph-notification"):
    """Send push to a queryset or list of users."""
    for user in users:
        send_push(user, title, body, link=link, priority=priority, tag=tag)
