import sys
import structlog
from typing import Any

def configure_logging() -> None:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.dev.ConsoleRenderer()
        ],
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(structlog.get_logger().level),
        cache_logger_on_first_use=True,
    )

logger = structlog.get_logger()

def log_error(error: Exception, **kwargs: Any) -> None:
    logger.error(
        "error_occurred",
        error_type=type(error).__name__,
        error_message=str(error),
        **kwargs
    )

def log_request(request_id: str, method: str, path: str, status_code: int, duration: float) -> None:
    logger.info(
        "request_processed",
        request_id=request_id,
        method=method,
        path=path,
        status_code=status_code,
        duration=duration
    )
