from enum import Enum
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field


class ImageFormat(str, Enum):
    AUTO = "auto"
    AVIF = "avif"
    WEBP = "webp"
    JPEG = "jpeg"
    PNG = "png"


class FitMode(str, Enum):
    COVER = "cover"
    CONTAIN = "contain"
    INSIDE = "inside"
    OUTSIDE = "outside"


class FallbackMode(str, Enum):
    THROW = "throw"
    PASSTHROUGH = "passthrough"


class PurgeType(str, Enum):
    URL = "url"
    ALL = "all"


class OptimizeOptions(BaseModel):
    """Configuration options for image conversion and compression."""
    format: ImageFormat = ImageFormat.AUTO
    quality: int = Field(default=80, ge=1, le=100)
    max_width: Optional[int] = None
    max_height: Optional[int] = None
    fit: FitMode = FitMode.COVER
    lossless: bool = False
    strip_metadata: bool = True
    filename: Optional[str] = None
    mime_type: Optional[str] = None
    idempotency_key: Optional[str] = None


class OptimizeResult(BaseModel):
    """Result returned after successful image optimization."""
    job_id: str
    status: str = "completed"
    url: str
    format: str
    original_size: int
    compressed_size: int
    bytes_saved: int
    savings_percentage: float
    upload_url: Optional[str] = None
    data: Optional[bytes] = None


class JobStatusResult(BaseModel):
    """Status details for an asynchronous conversion task."""
    job_id: str
    status: str
    url: Optional[str] = None
    format: Optional[str] = None
    bytes_saved: Optional[int] = None
    error: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class QuotaResponse(BaseModel):
    """Real-time account quota and CDN bandwidth usage."""
    plan: str
    bytes_used: int
    quota_limit: int
    quota_percentage: float
    cdn_egress_used_bytes: Optional[int] = None
    cdn_egress_quota_bytes: Optional[int] = None
    active_keys_count: Optional[int] = None
    active_sites_count: Optional[int] = None


class PurgeOptions(BaseModel):
    """Options for Edge CDN cache invalidation."""
    urls: Optional[List[str]] = None
    purge_type: PurgeType = PurgeType.URL


class PurgeResponse(BaseModel):
    """CDN cache purge confirmation."""
    message: str
