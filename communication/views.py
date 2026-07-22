from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import Department, User
from core.permissions import capability_required, role_required
from core.notify import notify_all, notify_user, notify_dept
from .forms import AnnouncementForm, ChannelForm, ChannelMessageForm, DirectMessageForm
from .models import Announcement, DepartmentChannel, ChannelMessage, DirectMessage, Notification


@login_required
def home(request):
    announcements = Announcement.objects.all()[:10]
    user = request.user
    if user.is_portal_admin():
        channels = DepartmentChannel.objects.select_related("department").all()
    elif user.department_id:
        channels = DepartmentChannel.objects.filter(
            department=user.department
        ).select_related("department")
    else:
        channels = DepartmentChannel.objects.none()

    messages_qs = DirectMessage.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).select_related("sender", "receiver").order_by("-timestamp")[:20]
    dm_form = DirectMessageForm(receiver_queryset=User.objects.filter(
        is_active=True
    ).exclude(pk=user.pk).order_by("first_name", "username"))
    return render(request, "communication/home.html", {
        "announcements":   announcements,
        "channels":        channels,
        "direct_messages": messages_qs,
        "dm_form":         dm_form,
    })


@capability_required("can_publish_announcements")
def announcement_create(request):
    form = AnnouncementForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        announcement = form.save(commit=False)
        announcement.created_by = request.user
        announcement.save()
        notify_all(
            f"Announcement: {announcement.title}",
            f"{request.user} posted an announcement. Check Communication for details.",
            exclude_pk=request.user.pk,
            link="/communication/",
        )
        messages.success(request, "Announcement published.")
        return redirect("communication:home")
    return render(request, "form.html", {"form": form, "title": "New Announcement"})


@role_required("admin")
def channel_create(request):
    """Admin creates a new department channel."""
    form = ChannelForm(
        request.POST or None,
        dept_queryset=Department.objects.all().order_by("name"),
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Channel created.")
        return redirect("communication:home")
    return render(request, "form.html", {"form": form, "title": "Create Department Channel"})


@role_required("admin")
def channel_delete(request, pk):
    """Admin deletes a department channel."""
    ch = get_object_or_404(DepartmentChannel, pk=pk)
    if request.method == "POST":
        name = ch.name
        ch.delete()
        messages.success(request, f"Channel #{name} deleted.")
    return redirect("communication:home")


@login_required
def channel(request, pk):
    channel_obj = get_object_or_404(DepartmentChannel, pk=pk)
    user = request.user
    # Access: admin sees all; others must belong to the channel's department
    if not user.is_portal_admin() and user.department_id != channel_obj.department_id:
        messages.error(request, "You do not have access to this channel.")
        return redirect("communication:home")

    # Paginate messages — show last 100
    channel_messages = channel_obj.messages.select_related("sender").order_by("timestamp")[:100]

    form = ChannelMessageForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        msg = form.save(commit=False)
        msg.channel = channel_obj
        msg.sender  = user
        msg.save()
        if channel_obj.department:
            notify_dept(
                channel_obj.department,
                f"New message in #{channel_obj.name}",
                f'{user.get_full_name() or user.username} posted in #{channel_obj.name}: "{msg.content[:80]}"',
                exclude_pk=user.pk,
                link=f"/communication/channels/{channel_obj.pk}/",
            )
        return redirect("communication:channel", pk=pk)

    return render(request, "communication/channel.html", {
        "channel": channel_obj,
        "channel_messages": channel_messages,
        "form": form,
    })


@login_required
def send_direct(request):
    user = request.user
    form = DirectMessageForm(
        request.POST or None,
        request.FILES or None,
        receiver_queryset=User.objects.filter(is_active=True).exclude(pk=user.pk),
    )
    if request.method == "POST" and form.is_valid():
        dm = form.save(commit=False)
        dm.sender = user
        dm.save()
        notify_user(
            dm.receiver,
            f"New message from {user.get_full_name() or user.username}",
           f'{user} sent you a message: "{dm.message[:100]}"',
            link="/communication/",
        )
        messages.success(request, "Message sent.")
    return redirect("communication:home")


@login_required
def notification_redirect(request, pk):
    """
    Mark a single notification as read and redirect to its link.
    Called when the user clicks a notification row.

    If ``notif.link`` is empty (older notifications), we infer a sensible
    destination from the notification title so clicking always navigates
    somewhere meaningful rather than looping back to the notifications page.
    """
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.read = True
    notif.save(update_fields=["read"])

    destination = notif.link

    # ── Infer destination from title when link is blank ──────────────────
    if not destination:
        title_lower = notif.title.lower()
        if any(w in title_lower for w in ("event", "registered for", "attendance recorded")):
            destination = "/events/"
        elif any(w in title_lower for w in ("task", "comment on task", "attachment")):
            destination = "/tasks/"
        elif any(w in title_lower for w in ("check-in", "check-out", "check in", "check out",
                                             "auto check", "geofence", "location")):
            destination = "/attendance/"
        elif any(w in title_lower for w in ("message", "announcement", "channel")):
            destination = "/communication/"
        elif any(w in title_lower for w in ("suggestion",)):
            destination = "/suggestions/"
        elif any(w in title_lower for w in ("violation",)):
            destination = "/attendance/violations/"
        elif any(w in title_lower for w in ("welcome", "password", "profile")):
            destination = "/accounts/profile/"
        else:
            destination = "/communication/notifications/"

    return redirect(destination)


@login_required
def notifications(request):
    """
    Shows the current user's personal notifications.
    Supports ?count_only=1 for AJAX polling (returns JSON with total count).
    Marks all as read on POST.
    """
    user_notifs = request.user.notifications.all()

    # AJAX count-only endpoint for live polling
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        unread_qs = user_notifs.filter(read=False)
        # Determine highest priority among unread notifications for sound cue
        priority_order = ["critical", "high", "medium", "low"]
        highest = "low"
        priorities_present = set(unread_qs.values_list("priority", flat=True))
        for p in priority_order:
            if p in priorities_present:
                highest = p
                break
        return JsonResponse({
            "total": user_notifs.count(),
            "unread": unread_qs.count(),
            "highest_priority": highest,
        })

    if request.method == "POST":
        user_notifs.update(read=True)

    notif_list = user_notifs[:50]
    unread_count = user_notifs.filter(read=False).count()

    return render(request, "communication/notifications.html", {
        "notifications": notif_list,
        "unread_count": unread_count,
    })


# ── Web Push subscription endpoints ──────────────────────────────────────────

import json as _json
from django.conf import settings as _settings
from django.views.decorators.csrf import csrf_exempt as _csrf_exempt


@login_required
def push_vapid_key(request):
    """Return the VAPID public key so the browser can subscribe."""
    return JsonResponse({"publicKey": _settings.VAPID_PUBLIC_KEY})


@login_required
def push_subscribe(request):
    """Register or update a push subscription for the current user."""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    from .models import PushSubscription
    try:
        data = _json.loads(request.body)
        endpoint = data["endpoint"]
        keys     = data["keys"]
        p256dh   = keys["p256dh"]
        auth     = keys["auth"]
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "Invalid subscription data"}, status=400)

    sub, created = PushSubscription.objects.update_or_create(
        endpoint=endpoint,
        defaults={"user": request.user, "p256dh": p256dh, "auth": auth},
    )
    return JsonResponse({"ok": True, "created": created})


@login_required
def push_unsubscribe(request):
    """Remove a push subscription."""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    from .models import PushSubscription
    try:
        data     = _json.loads(request.body)
        endpoint = data["endpoint"]
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "Invalid data"}, status=400)

    PushSubscription.objects.filter(user=request.user, endpoint=endpoint).delete()
    return JsonResponse({"ok": True})


@login_required
def push_send_test(request):
    """Send a test push notification to the current user (admin only)."""
    from .push import send_push
    send_push(
        request.user,
        title="🔔 Test Notification",
        body="Push notifications are working on your device!",
        link="/communication/notifications/",
        priority="medium",
        tag="test",
    )
    return JsonResponse({"ok": True, "message": "Test push sent"})
