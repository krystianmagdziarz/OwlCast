import pytest
from app.db.redis import redis

@pytest.mark.asyncio
async def test_redis_connection():
    await redis.init_redis()
    redis_instance = await redis.get_redis()
    
    await redis_instance.set("test_key", "test_value")
    value = await redis_instance.get("test_key")
    assert value == "test_value"
    
    await redis_instance.delete("test_key")
    await redis.close_redis()

@pytest.mark.asyncio
async def test_redis_reconnection():
    await redis.close_redis()
    redis_instance = await redis.get_redis()
    assert redis_instance is not None
