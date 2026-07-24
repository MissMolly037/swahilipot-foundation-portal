import os

# =============================================================================
# Server binding
# =============================================================================
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")

# =============================================================================
# Worker configuration
# =============================================================================
workers = int(os.getenv("GUNICORN_WORKERS", "2"))
threads = int(os.getenv("GUNICORN_THREADS", "4"))
worker_class = "gthread"
worker_tmp_dir = "/dev/shm"

# =============================================================================
# Performance
# =============================================================================
timeout = int(os.getenv("GUNICORN_TIMEOUT", "120"))
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "5"))
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", "50"))

# =============================================================================
# Logging
# =============================================================================
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
capture_output = True

# =============================================================================
# Proxy / HTTPS
# =============================================================================
forwarded_allow_ips = "*"
secure_scheme_headers = {
    "X-Forwarded-Proto": "https"
}

# =============================================================================
# Process naming
# =============================================================================
proc_name = "swahilipot-gunicorn"