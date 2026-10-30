import jwt
import pytest

from src.shared.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_can_be_verified():
    stored_hash = hash_password("strong-password")

    assert verify_password("strong-password", stored_hash) is True
    assert verify_password("wrong-password", stored_hash) is False
    assert "strong-password" not in stored_hash


def test_access_token_contains_user_identity():
    token = create_access_token("user-123", "user@example.com")
    payload = decode_access_token(token)

    assert payload["sub"] == "user-123"
    assert payload["email"] == "user@example.com"


def test_invalid_access_token_is_rejected():
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token("invalid-token")
