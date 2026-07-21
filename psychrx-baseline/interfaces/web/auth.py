"""Password-gated access for the hosted PsychRx web application."""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import time
from dataclasses import dataclass
from http.cookies import SimpleCookie


SESSION_COOKIE = "psychrx_session"
DEFAULT_SESSION_TTL_SECONDS = 8 * 60 * 60


@dataclass(frozen=True)
class WebAccessPolicy:
    """Environment-backed access policy for the web interface and API."""

    required: bool
    password: str
    session_secret: str
    session_ttl_seconds: int = DEFAULT_SESSION_TTL_SECONDS

    @classmethod
    def from_environment(cls) -> "WebAccessPolicy":
        required = os.getenv("PSYCHRX_AUTH_REQUIRED", "false").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        password = os.getenv("PSYCHRX_ACCESS_PASSWORD", "")
        session_secret = os.getenv("PSYCHRX_SESSION_SECRET", "")
        ttl_text = os.getenv(
            "PSYCHRX_SESSION_TTL_SECONDS",
            str(DEFAULT_SESSION_TTL_SECONDS),
        )
        try:
            ttl = max(300, int(ttl_text))
        except ValueError:
            ttl = DEFAULT_SESSION_TTL_SECONDS
        return cls(required, password, session_secret, ttl)

    def validate(self) -> None:
        """Reject an unsafe protected-mode configuration at server startup."""
        if not self.required:
            return
        if len(self.password) < 8:
            raise RuntimeError(
                "PSYCHRX_ACCESS_PASSWORD must contain at least 8 characters."
            )
        if len(self.session_secret) < 32:
            raise RuntimeError(
                "PSYCHRX_SESSION_SECRET must contain at least 32 characters."
            )

    def password_matches(self, candidate: str) -> bool:
        """Compare the supplied password without timing-dependent equality."""
        if not self.required:
            return True
        return hmac.compare_digest(candidate.encode("utf-8"), self.password.encode("utf-8"))

    def issue_session(self, now: int | None = None) -> str:
        """Create a signed, expiring session token without storing patient data."""
        issued_at = int(time.time()) if now is None else int(now)
        nonce = secrets.token_urlsafe(18)
        payload = f"{issued_at}.{nonce}"
        signature = hmac.new(
            self.session_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return f"{payload}.{signature}"

    def session_is_valid(self, token: str, now: int | None = None) -> bool:
        """Validate signature and expiration of a session token."""
        if not self.required:
            return True
        try:
            issued_text, nonce, signature = token.split(".", 2)
            issued_at = int(issued_text)
        except (TypeError, ValueError):
            return False
        payload = f"{issued_at}.{nonce}"
        expected = hmac.new(
            self.session_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        current_time = int(time.time()) if now is None else int(now)
        age = current_time - issued_at
        return (
            hmac.compare_digest(signature, expected)
            and 0 <= age <= self.session_ttl_seconds
        )

    def request_is_authenticated(self, cookie_header: str | None) -> bool:
        """Read and validate the PsychRx session cookie from a request."""
        if not self.required:
            return True
        cookie = SimpleCookie()
        try:
            cookie.load(cookie_header or "")
        except Exception:
            return False
        morsel = cookie.get(SESSION_COOKIE)
        return bool(morsel and self.session_is_valid(morsel.value))
