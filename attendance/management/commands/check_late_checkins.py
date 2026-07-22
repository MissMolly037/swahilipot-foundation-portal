"""
Management command: check_late_checkins

Scans all active ProjectSites and sends a push + in-app notification to every
active staff/intern/program_manager/department_head who:
  • has NOT checked in today, AND
  • the current time has passed (expected_check_in_time + grace_minutes), AND
  • a late warning has NOT already been sent today (avoids duplicate spam)

Run this every 5 minutes from the scheduler workflow.
Exits quietly with no output if nothing is late or everything already notified.
"""

import datetime
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Send late check-in push notifications for missed expected check-ins."

    def handle(self, *args, **options):
        from attendance.models import Attendance, ProjectSite
        from accounts.models import User
        from communication.models import Notification
        from core.notify import notify_user, HIGH

        now       = timezone.localtime()
        today     = now.date()
        weekday   = today.weekday()  # 0=Mon … 6=Sun

        # Skip weekends — adjust if your org works weekends
        if weekday >= 5:
            return

        # Staff roles that are expected to check in
        ACTIVE_ROLES = ["staff", "intern", "program_manager", "department_head", "admin"]

        active_sites = ProjectSite.objects.filter(active=True)
        if not active_sites.exists():
            return

        for site in active_sites:
            # Calculate deadline: expected_check_in + grace
            deadline_naive = datetime.datetime.combine(today, site.expected_check_in_time)
            deadline = timezone.make_aware(deadline_naive)
            deadline += datetime.timedelta(minutes=site.grace_minutes)

            if now < deadline:
                # Grace period not yet over for this site
                continue

            # Users who DID check in today at this site
            checked_in_today = set(
                Attendance.objects.filter(
                    project_site=site,
                    check_in_time__date=today,
                ).values_list("user_id", flat=True)
            )

            # All active staff
            candidates = User.objects.filter(
                is_active=True,
                role__in=ACTIVE_ROLES,
            ).exclude(pk__in=checked_in_today)

            # Warning title pattern — used to detect if already sent today
            warning_title_prefix = f"⏰ Late check-in"

            for user in candidates:
                # Check if warning already sent today for this site
                already_warned = Notification.objects.filter(
                    user=user,
                    title__startswith=warning_title_prefix,
                    timestamp__date=today,
                    message__icontains=site.name,
                ).exists()

                if already_warned:
                    continue

                minutes_late = int((now - deadline).total_seconds() / 60)
                late_str = (
                    f"{minutes_late} minute{'s' if minutes_late != 1 else ''}"
                    if minutes_late < 60
                    else f"{minutes_late // 60}h {minutes_late % 60}m"
                )

                title   = f"⏰ Late check-in reminder"
                message = (
                    f"You are {late_str} past the expected check-in time "
                    f"({site.expected_check_in_time.strftime('%H:%M')}) at {site.name}. "
                    f"Please check in as soon as possible."
                )

                notify_user(
                    user,
                    title=title,
                    message=message,
                    priority=HIGH,
                    link="/attendance/",
                )
                logger.info(
                    "Late check-in warning sent to %s (%s late) at site %s",
                    user, late_str, site.name,
                )
                self.stdout.write(
                    f"  ✓ Warned {user.get_full_name() or user.username} — {late_str} late at {site.name}"
                )

        # Also: warn managers when ANY staff member is more than 30 min late
        self._alert_managers_if_needed(today, now, active_sites)

        # Also: daily digest of early check-outs (fires once, after end-of-day)
        self._early_checkout_digest(today, now, active_sites)

    def _alert_managers_if_needed(self, today, now, active_sites):
        """
        Sends a single daily digest push to managers listing who is very late
        (>30 min past deadline). Fires once per day when at least one person
        is severely late.
        """
        from attendance.models import Attendance, ProjectSite
        from accounts.models import User
        from communication.models import Notification
        from core.notify import notify_managers, CRITICAL

        THRESHOLD_MINUTES = 30
        digest_title = "🚨 Staff late check-in alert"

        # Don't send more than once per day
        already_sent = Notification.objects.filter(
            title=digest_title,
            timestamp__date=today,
        ).exists()
        if already_sent:
            return

        very_late = []

        for site in active_sites:
            deadline_naive = __import__("datetime").datetime.combine(today, site.expected_check_in_time)
            deadline = __import__("django.utils.timezone", fromlist=["make_aware"]).make_aware(deadline_naive)
            deadline += __import__("datetime").timedelta(minutes=site.grace_minutes + THRESHOLD_MINUTES)

            if now < deadline:
                continue

            checked_in_today = set(
                Attendance.objects.filter(
                    project_site=site,
                    check_in_time__date=today,
                ).values_list("user_id", flat=True)
            )

            late_users = User.objects.filter(
                is_active=True,
                role__in=["staff", "intern", "program_manager", "department_head"],
            ).exclude(pk__in=checked_in_today)

            for u in late_users:
                very_late.append(f"{u.get_full_name() or u.username} ({site.name})")

        if very_late:
            names = ", ".join(very_late[:10])
            if len(very_late) > 10:
                names += f" and {len(very_late) - 10} more"
            notify_managers(
                title=digest_title,
                message=f"{len(very_late)} staff member(s) have not checked in: {names}.",
                priority=CRITICAL,
                link="/attendance/admin/",
            )
            self.stdout.write(
                self.style.WARNING(
                    f"  ⚠ Manager alert sent — {len(very_late)} very-late staff"
                )
            )

    def _early_checkout_digest(self, today, now, active_sites):
        """
        Sends a single end-of-day digest to managers listing everyone who
        checked out early today.  Fires once per day, only after the latest
        expected_check_out_time across all active sites has passed.
        Skips if no one checked out early, or if the digest was already sent.
        """
        import datetime
        from attendance.models import Attendance
        from communication.models import Notification
        from core.notify import notify_managers, HIGH

        digest_title = "📋 Early check-out summary"

        # Only fire after the latest end-of-day across all sites
        latest_end = max(
            (s.expected_check_out_time for s in active_sites),
            default=None,
        )
        if latest_end is None:
            return
        eod_naive = datetime.datetime.combine(today, latest_end)
        eod = __import__("django.utils.timezone", fromlist=["make_aware"]).make_aware(eod_naive)
        if now < eod:
            return  # End of day hasn't passed yet

        # Don't resend
        already_sent = Notification.objects.filter(
            title=digest_title,
            timestamp__date=today,
        ).exists()
        if already_sent:
            return

        early_records = (
            Attendance.objects
            .filter(
                check_in_time__date=today,
                departure_status=Attendance.DepartureStatus.LEFT_EARLY,
                status=Attendance.Status.CHECKED_OUT,
            )
            .select_related("user", "project_site")
            .order_by("check_out_time")
        )

        if not early_records.exists():
            return

        lines = []
        for rec in early_records:
            name      = rec.user.get_full_name() or rec.user.username
            out_str   = __import__("django.utils.timezone", fromlist=["localtime"]).localtime(rec.check_out_time).strftime("%H:%M")
            expected  = rec.project_site.expected_check_out_time.strftime("%H:%M")
            lines.append(f"{name} — checked out at {out_str} (expected {expected}, {rec.project_site.name})")

        count = len(lines)
        detail = "; ".join(lines[:8])
        if count > 8:
            detail += f"; and {count - 8} more"

        notify_managers(
            title=digest_title,
            message=f"{count} staff member{'s' if count != 1 else ''} checked out early today: {detail}.",
            priority=HIGH,
            link="/attendance/admin/",
        )
        self.stdout.write(
            self.style.WARNING(
                f"  📋 Early check-out digest sent — {count} early departure{'s' if count != 1 else ''}"
            )
        )
