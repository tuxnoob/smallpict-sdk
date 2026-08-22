import re
from typing import Optional, Dict, Any


def sanitize_message(msg: str) -> str:
    """Mask sensitive API keys and tokens from exception strings."""
    if not msg:
        return msg
    # Mask sp_live_..., sp_test_..., sp_sdk_..., sp_wp_...
    msg = re.sub(
        r"sp_(live|test|sdk|wp)_[a-zA-Z0-9_-]{10,}",
        lambda m: f"{m.group(0)[:10]}...{m.group(0)[-4:]}",
        msg,
    )
    # Mask secrets
    msg = re.sub(r"(sec|secret)_[a-zA-Z0-9_-]{8,}", "***REDACTED***", msg, flags=re.IGNORECASE)
    msg = re.sub(r"Bearer\s+[a-zA-Z0-9._-]+", "Bearer ***REDACTED***", msg, flags=re.IGNORECASE)
    return msg


class SmallPictError(Exception):
    """Base exception for all SmallPict Python SDK errors."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: Optional[int] = None,
        request_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.raw_message = message
        self.message = sanitize_message(message)
        self.code = code
        self.status_code = status_code
        self.request_id = request_id
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        status_part = f" HTTP {self.status_code}" if self.status_code else ""
        req_part = f" (Request ID: {self.request_id})" if self.request_id else ""
        return f"[{self.__class__.__name__}] ({self.code}{status_part}): {self.message}{req_part}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} code={self.code!r} status={self.status_code} msg={self.message!r}>"


class ValidationError(SmallPictError):
    """Raised when request payload fails client or server-side schema validation (HTTP 400)."""

    def __init__(
        self,
        message: str,
        request_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, "VALIDATION_FAILED", 400, request_id, details)


class AuthenticationError(SmallPictError):
    """Raised when API key or HMAC signature verification fails (HTTP 401)."""

    def __init__(
        self,
        message: str,
        request_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, "UNAUTHORIZED", 401, request_id, details)


class PermissionDeniedError(SmallPictError):
    """Raised when API key lacks required scope permission (HTTP 403)."""

    def __init__(
        self,
        message: str,
        request_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, "FORBIDDEN", 403, request_id, details)


class NotFoundError(SmallPictError):
    """Raised when requested resource or job ID does not exist (HTTP 404)."""

    def __init__(
        self,
        message: str,
        request_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, "NOT_FOUND", 404, request_id, details)


class QuotaExceededError(SmallPictError):
    """Raised when monthly storage or bandwidth quota is exhausted (HTTP 402)."""

    def __init__(
        self,
        message: str,
        request_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, "QUOTA_EXCEEDED", 402, request_id, details)


class RateLimitError(SmallPictError):
    """Raised when request rate limit is exceeded (HTTP 429)."""

    def __init__(
        self,
        message: str,
        retry_after_seconds: Optional[int] = None,
        request_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, "RATE_LIMIT_EXCEEDED", 429, request_id, details)
        self.retry_after_seconds = retry_after_seconds


class ServerError(SmallPictError):
    """Raised on internal server errors (HTTP 5xx)."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        request_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, "INTERNAL_ERROR", status_code, request_id, details)


class TimeoutError(SmallPictError):
    """Raised when HTTP request exceeds timeout duration."""

    def __init__(
        self,
        message: str = "Request timed out after maximum duration",
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(message, "TIMEOUT_ERROR", 408, request_id)


class NetworkError(SmallPictError):
    """Raised when underlying network connection or transport fails."""

    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        details = {"cause": str(original_error)} if original_error else {}
        super().__init__(
            f"Network communication failed: {message}",
            "NETWORK_ERROR",
            0,
            None,
            details,
        )


def create_error_from_response(
    status_code: int,
    body: Any,
    request_id: Optional[str] = None,
    retry_after_header: Optional[str] = None,
) -> SmallPictError:
    """Factory creating typed SmallPictError from HTTP status code and response payload."""
    message = f"API request failed with HTTP {status_code}"
    code = "INTERNAL_ERROR"
    details: Optional[Dict[str, Any]] = None

    if isinstance(body, dict):
        if "error" in body:
            err_data = body["error"]
            if isinstance(err_data, str):
                message = err_data
            elif isinstance(err_data, dict):
                message = err_data.get("message", message)
                code = err_data.get("code", code)
                details = err_data.get("details")
        elif "message" in body:
            message = str(body["message"])
    elif isinstance(body, str) and body.strip():
        message = body.strip()

    retry_after: Optional[int] = None
    if retry_after_header:
        try:
            retry_after = int(retry_after_header)
        except ValueError:
            pass

    if status_code == 400:
        return ValidationError(message, request_id, details)
    elif status_code == 401:
        return AuthenticationError(message, request_id, details)
    elif status_code == 402:
        return QuotaExceededError(message, request_id, details)
    elif status_code == 403:
        return PermissionDeniedError(message, request_id, details)
    elif status_code == 404:
        return NotFoundError(message, request_id, details)
    elif status_code == 429:
        return RateLimitError(message, retry_after, request_id, details)
    elif status_code >= 500:
        return ServerError(message, status_code, request_id, details)
    else:
        return SmallPictError(message, code, status_code, request_id, details)
