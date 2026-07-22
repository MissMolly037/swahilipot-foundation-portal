#!/usr/bin/env bash
# ── Swahilipot Hub Portal — background scheduler ──────────────────────────
# Runs every 5 minutes:
#   • check_late_checkins  — late check-in warnings + early check-out digest
#   • send_weekly_report   — Monday morning only, ~08:00–09:00 local time
# Registered as the "Late Check-in Scheduler" workflow in Replit.

set -e
cd "$(dirname "$0")"

echo "[scheduler] Starting (runs every 5 min) — $(date)"

while true; do
  TIMESTAMP="[$(date '+%H:%M:%S')]"
  HOUR=$(date '+%H')
  DAY=$(date '+%u')   # 1=Mon … 7=Sun

  # ── Late check-in + early check-out digest (every 5 min, weekdays) ──────
  python manage.py check_late_checkins 2>&1 | while IFS= read -r line; do
    echo "$TIMESTAMP [late-checkin] $line"
  done

  # ── Weekly attendance report — Monday 08:00–08:59 only ──────────────────
  if [ "$DAY" = "1" ] && [ "$HOUR" = "08" ]; then
    echo "$TIMESTAMP [weekly-report] Sending weekly attendance report..."
    python manage.py send_weekly_report 2>&1 | while IFS= read -r line; do
      echo "$TIMESTAMP [weekly-report] $line"
    done
  fi

  sleep 300
done
