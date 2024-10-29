import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_create_statistics(
    test_client: AsyncClient,
    api_key_headers: dict
):
    stats_data = {
        "url": "https://example.com/test",
        "user_agent": "Mozilla/5.0",
        "screen_width": 1920,
        "screen_height": 1080,
        "language": "en",
        "is_mobile": False,
        "scroll_depth": 80,
        "time_on_page": 120,
        "client_timestamp": datetime.now().isoformat(),
        "visitor_id": "test_visitor_1"
    }
    
    response = await test_client.post(
        "/api/v1/statistics/",
        json=stats_data,
        headers=api_key_headers
    )
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_domain_statistics(
    test_client: AsyncClient,
    api_key_headers: dict
):
    response = await test_client.get(
        "/api/v1/statistics/example.com",
        headers=api_key_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_aggregated_statistics(
    test_client: AsyncClient,
    api_key_headers: dict
):
    response = await test_client.get(
        "/api/v1/statistics/example.com/aggregate",
        headers=api_key_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_views" in data
    assert "unique_visitors" in data
    assert "avg_time_on_page" in data
    assert "bounce_rate" in data
    assert "avg_scroll_depth" in data
