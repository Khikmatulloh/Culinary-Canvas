# users/signals.py
from django.contrib.auth.signals import user_login_failed
import logging

logger = logging.getLogger("django.security.login")


def log_failed_login(sender, credentials, request, **kwargs):
    username = credentials.get("username") or credentials.get("email") or "<unknown>"
    ip = "<no-request>"
    try:
        if request is not None:
            ip = request.META.get("REMOTE_ADDR") or request.META.get("HTTP_X_FORWARDED_FOR") or "<unknown>"
    except Exception:
        ip = "<error-reading-ip>"
    logger.warning("Failed login attempt username=%s ip=%s", username, ip)


# connect signal
user_login_failed.connect(log_failed_login)