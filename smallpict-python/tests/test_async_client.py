import json
import pytest
import httpx
from smallpict import AsyncSmallPictClient, FallbackMode, QuotaExceededError, ValidationError


@pytest.mark.asyncio
async def test_async_client_missing_api_key():
    with pytest.raises(ValidationError):
        AsyncSmallPictClient(api_key="")


@pytest.mark.asyncio
async def test_async_optimize_success():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/optimize"
        assert request.headers.get("X-API-Key") == "sp_live_async_key"

        return httpx.Response(
            200,
            json={
                "job_id": "job_async_123",
                "status": "completed",
                "url": "https://cdn.smallpict.com/opt/async.webp",
                "format": "webp",
                "original_size": 150000,
                "compressed_size": 30000,
                "bytes_saved": 120000,
                "savings_percentage": 80.0,
            },
        )

    transport = httpx.MockTransport(mock_handler)
    http_client = httpx.AsyncClient(transport=transport)

    async with AsyncSmallPictClient(
        api_key="sp_live_async_key",
        http_client=http_client,
    ) as client:
        result = await client.optimize(
            b"async image bytes",
            filename="async.png",
            format="webp",
        )

        assert result.job_id == "job_async_123"
        assert result.status == "completed"
        assert result.url == "https://cdn.smallpict.com/opt/async.webp"
        assert result.savings_percentage == 80.0


@pytest.mark.asyncio
async def test_async_get_quota():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "plan": "scale",
                "bytes_used": 1000,
                "quota_limit": 50000,
                "quota_percentage": 2.0,
            },
        )

    transport = httpx.MockTransport(mock_handler)
    http_client = httpx.AsyncClient(transport=transport)

    async with AsyncSmallPictClient(api_key="sp_live_async_key", http_client=http_client) as client:
        quota = await client.get_quota()
        assert quota.plan == "scale"
        assert quota.quota_percentage == 2.0


@pytest.mark.asyncio
async def test_async_purge_cdn():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(202, json={"message": "Purge accepted"})

    transport = httpx.MockTransport(mock_handler)
    http_client = httpx.AsyncClient(transport=transport)

    async with AsyncSmallPictClient(api_key="sp_live_async_key", http_client=http_client) as client:
        res = await client.purge_cdn(["https://cdn.smallpict.com/opt/async.webp"])
        assert res.message == "Purge accepted"


@pytest.mark.asyncio
async def test_async_validate_key():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("X-API-Key") == "sp_live_valid":
            return httpx.Response(200, json={"plan": "free", "bytes_used": 0, "quota_limit": 100, "quota_percentage": 0.0})
        return httpx.Response(401, json={"error": {"code": "UNAUTHORIZED", "message": "Bad key"}})

    transport = httpx.MockTransport(mock_handler)
    http_client = httpx.AsyncClient(transport=transport)

    valid_client = AsyncSmallPictClient(api_key="sp_live_valid", http_client=http_client)
    assert await valid_client.validate_key() is True

    invalid_client = AsyncSmallPictClient(api_key="sp_live_invalid", http_client=http_client)
    assert await invalid_client.validate_key() is False
