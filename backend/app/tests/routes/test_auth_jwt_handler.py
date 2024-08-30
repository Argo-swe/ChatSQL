import jwt
import os
import time
from routes.auth.jwt_handler import JwtHandler


def test_sign_creates_valid_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test_secret")
    JwtHandler.JWT_SECRET = os.getenv("JWT_SECRET", "secret_string")
    token_response = JwtHandler.sign(123)

    assert "access_token" in token_response

    decoded_token = jwt.decode(
        token_response["access_token"], "test_secret", algorithms=["HS256"]
    )
    assert decoded_token["sub"] == 123


def test_decode_valid_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test_secret")

    token_response = JwtHandler.sign(123)
    decoded_token = JwtHandler.decode(token_response["access_token"])

    assert decoded_token["sub"] == 123


def test_decode_expired_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test_secret")

    expired_payload = {"exp": time.time() - 1000, "sub": 123}
    expired_token = jwt.encode(expired_payload, "test_secret", algorithm="HS256")

    decoded_token = JwtHandler.decode(expired_token)
    assert decoded_token is None


def test_invalid_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test_secret")

    invalid_token = "invalid.token.string"

    assert JwtHandler.decode(invalid_token) is None


def test_missing_jwt_secret(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    JwtHandler.JWT_SECRET = os.getenv("JWT_SECRET", "secret_string")
    assert JwtHandler.JWT_SECRET == "secret_string"

    token_response = JwtHandler.sign(123)
    decoded_token = JwtHandler.decode(token_response["access_token"])

    assert decoded_token["sub"] == 123


def test_decode_with_invalid_signature(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test_secret")

    valid_token = JwtHandler.sign(123)["access_token"]

    invalid_token = valid_token[:-1] + "0"

    decoded_token = JwtHandler.decode(invalid_token)
    assert decoded_token is None
