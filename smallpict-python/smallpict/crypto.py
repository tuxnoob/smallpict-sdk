import hmac
import hashlib
from typing import Union

EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def sha256_hex(data: Union[str, bytes]) -> str:
    """Compute hex-encoded SHA-256 hash of a string or byte sequence."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def hmac_sha256_hex(secret_key: str, string_to_sign: str) -> str:
    """Compute hex-encoded HMAC-SHA256 signature."""
    return hmac.new(
        secret_key.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def build_string_to_sign(method: str, path: str, timestamp: str, body_hash: str) -> str:
    """Construct the canonical string-to-sign per OpenAPI 3.1 contract."""
    clean_path = path if path.startswith("/") else f"/{path}"
    return f"{method.upper()}\n{clean_path}\n{timestamp}\n{body_hash}"
