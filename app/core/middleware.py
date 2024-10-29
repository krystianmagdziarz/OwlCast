import time
import uuid
from fastapi import Request
from prometheus_client import Counter, Histogram
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from app.core.logging import log_request, log_error

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)

async def metrics_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    start_time = time.time()
    response = None
    
    # Start OpenTelemetry span
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span(
        f"{request.method} {request.url.path}",
        kind=trace.SpanKind.SERVER,
    ) as span:
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", str(request.url))
        span.set_attribute("http.request_id", request_id)
        
        try:
            response = await call_next(request)
            
            # Record metrics
            duration = time.time() - start_time
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            
            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
            
            # Log request
            log_request(
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration=duration
            )
            
            span.set_status(Status(StatusCode.OK))
            span.set_attribute("http.status_code", response.status_code)
            
            return response
            
        except Exception as e:
            log_error(
                e,
                request_id=request_id,
                method=request.method,
                path=request.url.path
            )
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            raise
