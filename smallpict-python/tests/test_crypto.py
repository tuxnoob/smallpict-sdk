import pytest
from smallpict.crypto import (
    EMPTY_SHA256,
    build_string_to_sign,
    hmac_sha256_hex,
    sha256_hex,
)


def test_empty_sha256_constant():
    assert EMPTY_SHA256 == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_sha256_hex_empty_string():
    assert sha256_hex("") == EMPTY_SHA256


def test_sha256_hex_string():
    assert sha256_hex("hello world") == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"


def test_build_string_to_sign():
    result = build_string_to_sign("POST", "/v1/optimize", "1716301234", EMPTY_SHA256)
    assert result == f"POST\n/v1/optimize\n1716301234\n{EMPTY_SHA256}"


def test_hmac_sha256_hex_signature():
    secret_key = "sec_test_secret_key_123"
    string_to_sign = f"POST\n/v1/optimize\n1716301234\n{EMPTY_SHA256}"
    sig = hmac_sha256_hex(secret_key, string_to_sign)
    assert len(sig) == 64
    assert sig.isalnum()
