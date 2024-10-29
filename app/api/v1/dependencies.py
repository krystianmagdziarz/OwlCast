from fastapi import Request
from fastapi_limiter.depends import RateLimiter
from app.core.config import settings

async def rate_limit():
    return RateLimiter(
        times=settings.RATE_LIMIT_PER_SECOND,
        seconds=1
    )
