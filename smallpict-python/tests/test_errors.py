import pytest
from smallpict.errors import (
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    QuotaExceededError,
    RateLimitError,
    ServerError,
    SmallPictError,
    ValidationError,
    create_error_from_response,
    sanitize_message,
)


def test_sanitize_message():
    raw = "Failed on key sp_live_1234567890abcdef1234567890abcdef with sec_secret123456"
    sanitized = sanitize_message(raw)
    assert "sp_live_1234567890abcdef1234567890abcdef" not in sanitized
    assert "sec_secret123456" not in sanitized
    assert "sp_live_12...cdef" in sanitized
    assert "***REDACTED***" in sanitized


def test_error_redaction_in_str():
    err = SmallPictError("Key sp_test_11223344556677889900 is invalid", "UNAUTHORIZED", 401)
    assert "sp_test_11223344556677889900" not in str(err)
    assert "sp_test_11...9900" in str(err)


def test_create_error_from_response_mapping():
    err400 = create_error_from_response(400, {"error": {"message": "Invalid format"}})
    assert isinstance(err400, ValidationError)
    assert err400.status_code == 400

    err401 = create_error_from_response(401, {"error": {"message": "Invalid key"}})
    assert isinstance(err401, AuthenticationError)
    assert err401.status_code == 401

    err402 = create_error_from_response(402, {"error": {"message": "Quota full"}})
    assert isinstance(err402, QuotaExceededError)
    assert err402.status_code == 402

    err403 = create_error_from_response(403, {"error": {"message": "Forbidden"}})
    assert isinstance(err403, PermissionDeniedError)
    assert err403.status_code == 403

    err404 = create_error_from_response(404, {"error": {"message": "Not found"}})
    assert isinstance(err404, NotFoundError)
    assert err404.status_code == 404

    err429 = create_error_from_response(
        429, {"error": {"message": "Rate limit"}}, "req_001", "10"
    )
    assert isinstance(err429, RateLimitError)
    assert err429.retry_after_seconds == 10
    assert err429.request_id == "req_001"

    err500 = create_error_from_response(500, {"message": "Internal error"})
    assert isinstance(err500, ServerError)
    assert err500.status_code == 500
