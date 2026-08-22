"""
SmallPict Official Python SDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
High-performance cloud image optimization, format transcoding (WebP, AVIF),
CDN edge invalidation, and real-time quota tracking.
"""

from .client import SmallPictClient
from .aclient import AsyncSmallPictClient
from .errors import (
    SmallPictError,
    ValidationError,
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    QuotaExceededError,
    RateLimitError,
    ServerError,
    TimeoutError,
    NetworkError,
    sanitize_message,
)
from .models import (
    ImageFormat,
    FitMode,
    FallbackMode,
    PurgeType,
    OptimizeOptions,
    OptimizeResult,
    JobStatusResult,
    QuotaResponse,
    PurgeOptions,
    PurgeResponse,
)

__version__ = "1.0.0"
__all__ = [
    "SmallPictClient",
    "AsyncSmallPictClient",
    "SmallPictError",
    "ValidationError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "QuotaExceededError",
    "RateLimitError",
    "ServerError",
    "TimeoutError",
    "NetworkError",
    "sanitize_message",
    "ImageFormat",
    "FitMode",
    "FallbackMode",
    "PurgeType",
    "OptimizeOptions",
    "OptimizeResult",
    "JobStatusResult",
    "QuotaResponse",
    "PurgeOptions",
    "PurgeResponse",
]
