import json
import pytest
import httpx
from smallpict import SmallPictClient, FallbackMode, QuotaExceededError, ValidationError


def test_client_missing_api_key():
    with pytest.raises(ValidationError):
        SmallPictClient(api_key="")


def test_sync_optimize_success():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/optimize"
        assert request.headers.get("X-API-Key") == "sp_live_test_api_key_1234567890"
        assert "X-Signature" in request.headers
        assert "X-Timestamp" in request.headers
        assert "Idempotency-Key" in request.headers

        payload = json.loads(request.content.decode("utf-8"))
        assert payload["filename"] == "banner.png"
        assert payload["options"]["format"] == "avif"

        return httpx.Response(
            200,
            json={
                "job_id": "job_sync_123",
                "status": "completed",
                "url": "https://cdn.smallpict.app/opt/banner.avif",
                "format": "avif",
                "original_size": 200000,
                "compressed_size": 25000,
                "bytes_saved": 175000,
                "savings_percentage": 87.5,
            },
        )

    transport = httpx.MockTransport(mock_handler)
    http_client = httpx.Client(transport=transport)

    with SmallPictClient(
        api_key="sp_live_test_api_key_1234567890",
        secret_key="sec_test_secret_key_123",
        http_client=http_client,
    ) as client:
        result = client.optimize(
            b"fake raw binary bytes",
            filename="banner.png",
            format="avif",
            quality=85,
        )

        assert result.job_id == "job_sync_123"
        assert result.status == "completed"
        assert result.url == "https://cdn.smallpict.app/opt/banner.avif"
        assert result.savings_percentage == 87.5


def test_sync_get_quota():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/quota"
        return httpx.Response(
            200,
            json={
                "plan": "api_velocity",
                "bytes_used": 5000000,
                "quota_limit": 10000000,
                "quota_percentage": 50.0,
            },
        )

    transport = httpx.MockTransport(mock_handler)
    http_client = httpx.Client(transport=transport)

    with SmallPictClient(api_key="sp_live_test", http_client=http_client) as client:
        quota = client.get_quota()
        assert quota.plan == "api_velocity"
        assert quota.bytes_used == 5000000
        assert quota.quota_percentage == 50.0


def test_sync_purge_cdn():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/purge"
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["urls"] == ["https://cdn.smallpict.app/opt/banner.avif"]
        return httpx.Response(202, json={"message": "Purge accepted"})

    transport = httpx.MockTransport(mock_handler)
    http_client = httpx.Client(transport=transport)

    with SmallPictClient(api_key="sp_live_test", http_client=http_client) as client:
        res = client.purge_cdn("https://cdn.smallpict.app/opt/banner.avif")
        assert res.message == "Purge accepted"


def test_sync_validate_key():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("X-API-Key") == "sp_live_valid":
            return httpx.Response(200, json={"plan": "free", "bytes_used": 0, "quota_limit": 100, "quota_percentage": 0.0})
        return httpx.Response(401, json={"error": {"code": "UNAUTHORIZED", "message": "Bad key"}})

    transport = httpx.MockTransport(mock_handler)
    http_client = httpx.Client(transport=transport)

    valid_client = SmallPictClient(api_key="sp_live_valid", http_client=http_client)
    assert valid_client.validate_key() is True

    invalid_client = SmallPictClient(api_key="sp_live_invalid", http_client=http_client)
    assert invalid_client.validate_key() is False


def test_sync_fallback_passthrough_on_quota_exceeded():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(402, json={"error": {"code": "QUOTA_EXCEEDED", "message": "Quota full"}})

    transport = httpx.MockTransport(mock_handler)
    http_client = httpx.Client(transport=transport)

    with SmallPictClient(
        api_key="sp_live_test",
        fallback_mode=FallbackMode.PASSTHROUGH,
        http_client=http_client,
    ) as client:
        result = client.optimize(b"my image bytes", filename="pic.png")
        assert result.job_id == "fallback-passthrough"
        assert result.savings_percentage == 0.0
        assert result.bytes_saved == 0
