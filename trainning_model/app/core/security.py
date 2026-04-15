from __future__ import annotations

import base64
import hashlib
import hmac
import secrets

from .config import PBKDF2_ITERATIONS


def _derive_key(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    key = _derive_key(password, salt)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${base64.b64encode(salt).decode()}${base64.b64encode(key).decode()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations_raw, salt_raw, hash_raw = encoded.split("$", 3)
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    try:
        iterations = int(iterations_raw)
        salt = base64.b64decode(salt_raw.encode())
        expected_hash = base64.b64decode(hash_raw.encode())
    except (ValueError, TypeError):
        return False

    actual_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return hmac.compare_digest(actual_hash, expected_hash)
