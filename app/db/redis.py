from typing import Optional
import aioredis
from app.core.config import settings

class RedisClient:
    redis: Optional[aioredis.Redis] = None
    
    @classmethod
    async def init_redis(cls) -> None:
        if not cls.redis:
            cls.redis = await aioredis.from_url(
                f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                password=settings.REDIS_PASSWORD,
                db=settings.REDIS_DB,
                encoding="utf-8",
                decode_responses=True
            )
    
    @classmethod
    async def close_redis(cls) -> None:
        if cls.redis:
            await cls.redis.close()
            cls.redis = None
    
    @classmethod
    async def get_redis(cls) -> aioredis.Redis:
        if not cls.redis:
            await cls.init_redis()
        return cls.redis

redis = RedisClient()
