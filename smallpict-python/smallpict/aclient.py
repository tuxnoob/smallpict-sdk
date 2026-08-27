import os
import io
import time
import uuid
import random
import asyncio
from pathlib import Path
from typing import Optional, Union, List, Dict, Any

import httpx

from .crypto import EMPTY_SHA256, build_string_to_sign, hmac_sha256_hex, sha256_hex
from .errors import (
    NetworkError,
    QuotaExceededError,
    TimeoutError,
    ValidationError,
    create_error_from_response,
)
from .models import (
    FallbackMode,
    FitMode,
    ImageFormat,
    JobStatusResult,
    OptimizeOptions,
    OptimizeResult,
    PurgeOptions,
    PurgeResponse,
    PurgeType,
    QuotaResponse,
)
from .pil_adapter import extract_pil_bytes, is_pil_image


class AsyncSmallPictClient:
    """
    Asynchronous SmallPict API client for asyncio, FastAPI, Starlette, and Celery workflows.
    Supports async context manager (`async with AsyncSmallPictClient(...) as client:`).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        fallback_mode: FallbackMode = FallbackMode.THROW,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self.api_key = api_key or os.environ.get("SMALLPICT_API_KEY", "")
        self.secret_key = secret_key or os.environ.get("SMALLPICT_SECRET_KEY")

        if not self.api_key:
            raise ValidationError(
                "Missing required SmallPict API Key. Provide `api_key` argument or set SMALLPICT_API_KEY environment variable."
            )

        raw_base = base_url or os.environ.get("SMALLPICT_BASE_URL", "https://api.smallpict.app")
        self.base_url = raw_base.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.fallback_mode = fallback_mode

        self._external_client = http_client is not None
        self._client = http_client or httpx.AsyncClient(timeout=self.timeout)

    async def __aenter__(self) -> "AsyncSmallPictClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the underlying HTTP client transport."""
        if not self._external_client:
            await self._client.aclose()

    def _resolve_source(
        self, source: Union[bytes, str, Path, io.IOBase, Any], options: Optional[OptimizeOptions]
    ) -> Dict[str, Any]:
        filename = options.filename if options and options.filename else "image.jpg"
        mime_type = options.mime_type if options and options.mime_type else "image/jpeg"
        filesize = 0
        raw_bytes: Optional[bytes] = None

        if is_pil_image(source):
            quality = options.quality if options else 80
            raw_bytes, detected_mime, detected_fn = extract_pil_bytes(source, quality=quality)
            mime_type = options.mime_type if (options and options.mime_type) else detected_mime
            filename = options.filename if (options and options.filename) else detected_fn
            filesize = len(raw_bytes)
        elif isinstance(source, (str, Path)):
            path_str = str(source)
            if path_str.startswith("http://") or path_str.startswith("https://"):
                filename = path_str.split("/")[-1].split("?")[0] or filename
                return {"filename": filename, "mime_type": mime_type, "filesize": 0, "bytes": None}
            elif os.path.exists(path_str):
                filename = os.path.basename(path_str)
                with open(path_str, "rb") as f:
                    raw_bytes = f.read()
                filesize = len(raw_bytes)
        elif isinstance(source, io.IOBase):
            raw_bytes = source.read()
            if isinstance(raw_bytes, str):
                raw_bytes = raw_bytes.encode("utf-8")
            filesize = len(raw_bytes) if raw_bytes else 0
        elif isinstance(source, bytes):
            raw_bytes = source
            filesize = len(raw_bytes)

        return {
            "filename": filename,
            "mime_type": mime_type,
            "filesize": filesize,
            "bytes": raw_bytes,
        }

    async def _request(
        self,
        method: str,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        clean_path = path if path.startswith("/") else f"/{path}"
        if not clean_path.startswith("/v1/") and not clean_path.startswith("/v2/"):
            clean_path = f"/v1{clean_path}"

        url = f"{self.base_url}{clean_path}"
        body_str = ""
        body_hash = EMPTY_SHA256

        if json_data is not None:
            import json
            body_str = json.dumps(json_data, separators=(",", ":"))
            body_hash = sha256_hex(body_str)

        attempt = 0
        base_delay = 0.25

        while attempt <= self.max_retries:
            attempt += 1
            timestamp = str(int(time.time()))

            headers = {
                "Accept": "application/json",
                "X-API-Key": self.api_key,
            }

            if json_data is not None:
                headers["Content-Type"] = "application/json"

            if self.secret_key:
                string_to_sign = build_string_to_sign(method, clean_path, timestamp, body_hash)
                signature = hmac_sha256_hex(self.secret_key, string_to_sign)
                headers["X-Timestamp"] = timestamp
                headers["X-Signature"] = signature
            else:
                headers["Authorization"] = f"Bearer {self.api_key}"

            if method.upper() in ("POST", "PATCH", "DELETE"):
                headers["Idempotency-Key"] = idempotency_key or str(uuid.uuid4())

            try:
                response = await self._client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    content=body_str.encode("utf-8") if body_str else None,
                    timeout=self.timeout,
                )

                request_id = response.headers.get("x-request-id")
                retry_after_header = response.headers.get("retry-after")

                if response.status_code == 429 or (500 <= response.status_code <= 504):
                    if attempt <= self.max_retries:
                        delay = base_delay * (2 ** (attempt - 1))
                        if retry_after_header:
                            try:
                                delay = float(retry_after_header)
                            except ValueError:
                                pass
                        await asyncio.sleep(delay + random.uniform(0.0, 0.1))
                        continue

                try:
                    data = response.json()
                except Exception:
                    data = response.text

                if not response.is_success:
                    raise create_error_from_response(
                        response.status_code, data, request_id, retry_after_header
                    )

                return data if isinstance(data, dict) else {"response": data}

            except httpx.TimeoutException as exc:
                if attempt <= self.max_retries:
                    await asyncio.sleep(base_delay * (2 ** (attempt - 1)))
                    continue
                raise TimeoutError(f"Request to {clean_path} timed out after {self.timeout}s") from exc
            except (httpx.NetworkError, httpx.TransportError) as exc:
                if attempt <= self.max_retries:
                    await asyncio.sleep(base_delay * (2 ** (attempt - 1)))
                    continue
                raise NetworkError(str(exc), exc) from exc

        raise NetworkError("Request failed after maximum retry attempts")

    async def optimize(
        self,
        source: Union[bytes, str, Path, io.IOBase, Any],
        options: Optional[OptimizeOptions] = None,
        **kwargs: Any,
    ) -> OptimizeResult:
        """
        Asynchronously compress and transcode an image to modern web formats (AVIF, WebP).
        """
        if options is None:
            options = OptimizeOptions(**kwargs) if kwargs else OptimizeOptions()

        resolved = self._resolve_source(source, options)

        payload = {
            "filename": resolved["filename"],
            "mime_type": resolved["mime_type"],
            "filesize": resolved["filesize"],
            "options": {
                "format": options.format.value if hasattr(options.format, "value") else str(options.format),
                "quality": options.quality,
                "max_width": options.max_width,
                "max_height": options.max_height,
                "fit": options.fit.value if hasattr(options.fit, "value") else str(options.fit),
                "lossless": options.lossless,
                "strip_metadata": options.strip_metadata,
            },
        }

        try:
            res = await self._request("POST", "/v1/optimize", json_data=payload, idempotency_key=options.idempotency_key)

            original_size = res.get("original_size", resolved["filesize"])
            compressed_size = res.get("compressed_size", original_size)
            bytes_saved = res.get("bytes_saved", max(0, original_size - compressed_size))
            savings_pct = res.get(
                "savings_percentage",
                round((bytes_saved / original_size * 100), 2) if original_size > 0 else 0.0,
            )

            return OptimizeResult(
                job_id=res.get("job_id", "sync"),
                status=res.get("status", "completed"),
                url=res.get("url", ""),
                format=res.get("format", str(options.format)),
                original_size=original_size,
                compressed_size=compressed_size,
                bytes_saved=bytes_saved,
                savings_percentage=float(savings_pct),
                upload_url=res.get("upload_url"),
            )
        except QuotaExceededError as err:
            if self.fallback_mode == FallbackMode.PASSTHROUGH:
                return OptimizeResult(
                    job_id="fallback-passthrough",
                    status="completed",
                    url=str(source) if isinstance(source, (str, Path)) else "",
                    format=resolved["mime_type"].replace("image/", ""),
                    original_size=resolved["filesize"],
                    compressed_size=resolved["filesize"],
                    bytes_saved=0,
                    savings_percentage=0.0,
                    data=resolved["bytes"],
                )
            raise err

    async def get_quota(self) -> QuotaResponse:
        """Retrieve real-time account storage quota and CDN egress bandwidth metrics."""
        res = await self._request("GET", "/v1/quota")
        return QuotaResponse(**res)

    async def purge_cdn(
        self,
        urls: Optional[Union[List[str], str]] = None,
        purge_type: PurgeType = PurgeType.URL,
    ) -> PurgeResponse:
        """Invalidate cached assets across global CDN edge locations."""
        url_list: List[str] = []
        if isinstance(urls, str):
            url_list = [urls]
        elif isinstance(urls, list):
            url_list = urls

        payload = {
            "purge_type": purge_type.value if hasattr(purge_type, "value") else str(purge_type),
            "urls": url_list,
        }
        res = await self._request("POST", "/v1/purge", json_data=payload)
        return PurgeResponse(**res)

    async def validate_key(self) -> bool:
        """Check if the configured API key is valid and active."""
        try:
            await self.get_quota()
            return True
        except Exception:
            return False

    async def get_job_status(self, job_id: str) -> JobStatusResult:
        """Poll the status of an asynchronous image optimization job."""
        if not job_id:
            raise ValidationError("job_id parameter is required")
        res = await self._request("GET", f"/v1/optimize/status?job_id={job_id}")
        return JobStatusResult(**res)
