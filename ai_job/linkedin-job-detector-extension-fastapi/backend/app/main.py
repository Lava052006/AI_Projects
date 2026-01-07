"""Main FastAPI application entry point."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Import configuration
from app.config import settings

# Import controllers
from app.controllers import job_analysis_router

# Import middleware and error handlers
from app.middleware import (
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler,
    RateLimitingMiddleware,
    JSONParsingMiddleware,
    LoggingMiddleware,
    MetricsMiddleware,
    metrics_collector
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Job Analysis API",
    description="A FastAPI service for analyzing job postings to assess legitimacy and potential risks",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add custom middleware (order matters - first added is outermost)
app.add_middleware(JSONParsingMiddleware)
if settings.log_requests or settings.log_responses:
    app.add_middleware(LoggingMiddleware, log_requests=settings.log_requests, log_responses=settings.log_responses)
if settings.enable_metrics:
    app.add_middleware(MetricsMiddleware)
app.add_middleware(
    RateLimitingMiddleware,
    requests_per_minute=settings.rate_limit_requests_per_minute,
    requests_per_hour=settings.rate_limit_requests_per_hour
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Register routers
app.include_router(job_analysis_router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Job Analysis API is running", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "job-analysis-api"}


@app.get("/metrics")
async def get_metrics():
    """Get API performance metrics."""
    if not settings.enable_metrics:
        return {"detail": "Metrics collection is disabled"}
    return metrics_collector.get_metrics()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )