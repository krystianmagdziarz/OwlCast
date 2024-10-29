from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter
from contextlib import asynccontextmanager
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.core.config import settings
from app.core.logging import configure_logging
from app.db.redis import redis
from app.core.middleware import metrics_middleware
from app.api.v1.endpoints import statistics, metrics

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Configure logging
    configure_logging()
    
    # Initialize Redis
    await redis.init_redis()
    
    # Initialize cache
    redis_instance = await redis.get_redis()
    FastAPICache.init(RedisBackend(redis_instance), prefix="fastapi-cache")
    
    # Initialize rate limiter
    await FastAPILimiter.init(redis_instance)
    
    yield
    
    # Cleanup
    await redis.close_redis()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# Add middleware
app.middleware("http")(metrics_middleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenTelemetry instrumentation
FastAPIInstrumentor.instrument_app(app)

# Include routers
app.include_router(
    statistics.router,
    prefix=f"{settings.API_V1_STR}/statistics",
    tags=["statistics"]
)

app.include_router(
    metrics.router,
    prefix=f"{settings.API_V1_STR}",
    tags=["metrics"]
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to StatCollector API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
