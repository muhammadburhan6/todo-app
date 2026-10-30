"""Password hashing and JWT helpers."""

import base64
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import os

import jwt

from src.config import JWT_ALGORITHM, JWT_EXPIRE_HOURS, JWT_SECRET


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        200_000,
    )
    return f"{base64.b64encode(salt).decode()}:{base64.b64encode(password_hash).decode()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_text, hash_text = stored_hash.split(":", 1)
        salt = base64.b64decode(salt_text)
        expected_hash = base64.b64decode(hash_text)
    except (ValueError, TypeError):
        return False

    actual_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        200_000,
    )
    return hmac.compare_digest(actual_hash, expected_hash)


def create_access_token(uid: str, email: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": uid,
        "email": email,
        "iat": now,
        "exp": now + timedelta(hours=JWT_EXPIRE_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
