import pytest
from datetime import datetime
from app.services.statistics import StatisticsService
from app.schemas.statistics import StatisticsCreate

@pytest.mark.asyncio
async def test_create_statistics():
    stats = StatisticsCreate(
        url="https://example.com/test",
        user_agent="Mozilla/5.0",
        screen_width=1920,
        screen_height=1080,
        language="en",
        is_mobile=False,
        scroll_depth=80,
        time_on_page=120,
        client_timestamp=datetime.now(),
        visitor_id="test_visitor_1"
    )
    
    try:
        await StatisticsService.create_statistics(stats)
    except Exception as e:
        pytest.fail(f"Failed to create statistics: {e}")

@pytest.mark.asyncio
async def test_get_domain_statistics():
    stats = await StatisticsService.get_domain_statistics("example.com")
    assert isinstance(stats, list)

@pytest.mark.asyncio
async def test_get_aggregated_statistics():
    stats = await StatisticsService.get_aggregated_statistics("example.com")
    assert stats.total_views >= 0
    assert stats.unique_visitors >= 0
    assert stats.avg_time_on_page >= 0
    assert 0 <= stats.bounce_rate <= 100
    assert 0 <= stats.avg_scroll_depth <= 100
