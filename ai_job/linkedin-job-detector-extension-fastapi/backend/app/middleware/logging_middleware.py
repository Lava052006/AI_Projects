"""Logging and monitoring middleware for the Job Analysis API."""

import time
import logging
import json
from typing import Dict, Any, Optional
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for structured logging of requests and responses with performance metrics.
    
    This middleware logs all incoming requests with timing information, response status,
    and other relevant metrics for monitoring and debugging purposes.
    """
    
    def __init__(self, app, log_requests: bool = True, log_responses: bool = True):
        """
        Initialize the logging middleware.
        
        Args:
            app: The FastAPI application
            log_requests: Whether to log incoming requests
            log_responses: Whether to log outgoing responses
        """
        super().__init__(app)
        self.log_requests = log_requests
        self.log_responses = log_responses
    
    def _get_client_info(self, request: Request) -> Dict[str, Any]:
        """
        Extract client information from request.
        
        Args:
            request: The FastAPI request object
            
        Returns:
            Dictionary containing client information
        """
        # Get client IP (considering proxy headers)
        client_ip = "unknown"
        if request.client:
            client_ip = request.client.host
        
        # Check for forwarded headers
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            client_ip = real_ip
        
        return {
            "client_ip": client_ip,
            "user_agent": request.headers.get("User-Agent", "unknown"),
            "referer": request.headers.get("Referer"),
        }
    
    def _get_request_info(self, request: Request) -> Dict[str, Any]:
        """
        Extract request information for logging.
        
        Args:
            request: The FastAPI request object
            
        Returns:
            Dictionary containing request information
        """
        return {
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "headers": {
                key: value for key, value in request.headers.items()
                if key.lower() not in ["authorization", "cookie", "x-api-key"]  # Exclude sensitive headers
            },
            "content_type": request.headers.get("Content-Type"),
            "content_length": request.headers.get("Content-Length"),
        }
    
    def _log_request(self, request: Request, client_info: Dict[str, Any]) -> None:
        """
        Log incoming request information.
        
        Args:
            request: The FastAPI request object
            client_info: Client information dictionary
        """
        if not self.log_requests:
            return
        
        request_info = self._get_request_info(request)
        
        log_data = {
            "event": "request_started",
            "timestamp": time.time(),
            "client": client_info,
            "request": request_info,
        }
        
        logger.info(f"Request started: {request.method} {request.url.path}", extra=log_data)
    
    def _log_response(
        self,
        request: Request,
        response: Response,
        client_info: Dict[str, Any],
        duration: float,
        request_size: Optional[int] = None
    ) -> None:
        """
        Log response information with performance metrics.
        
        Args:
            request: The FastAPI request object
            response: The response object
            client_info: Client information dictionary
            duration: Request processing duration in seconds
            request_size: Size of request body in bytes
        """
        if not self.log_responses:
            return
        
        request_info = self._get_request_info(request)
        
        # Get response size if available
        response_size = None
        if hasattr(response, 'headers') and 'content-length' in response.headers:
            try:
                response_size = int(response.headers['content-length'])
            except (ValueError, TypeError):
                pass
        
        log_data = {
            "event": "request_completed",
            "timestamp": time.time(),
            "client": client_info,
            "request": request_info,
            "response": {
                "status_code": response.status_code,
                "headers": dict(response.headers) if hasattr(response, 'headers') else {},
                "size_bytes": response_size,
            },
            "performance": {
                "duration_seconds": round(duration, 4),
                "duration_ms": round(duration * 1000, 2),
                "request_size_bytes": request_size,
                "response_size_bytes": response_size,
            }
        }
        
        # Determine log level based on status code
        if response.status_code >= 500:
            log_level = logging.ERROR
            log_message = f"Request failed: {request.method} {request.url.path} - {response.status_code}"
        elif response.status_code >= 400:
            log_level = logging.WARNING
            log_message = f"Request error: {request.method} {request.url.path} - {response.status_code}"
        else:
            log_level = logging.INFO
            log_message = f"Request completed: {request.method} {request.url.path} - {response.status_code}"
        
        logger.log(log_level, log_message, extra=log_data)
    
    def _get_request_size(self, request: Request) -> Optional[int]:
        """
        Get the size of the request body.
        
        Args:
            request: The FastAPI request object
            
        Returns:
            Request body size in bytes, or None if not available
        """
        content_length = request.headers.get("Content-Length")
        if content_length:
            try:
                return int(content_length)
            except (ValueError, TypeError):
                pass
        return None
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process the request and log information with performance metrics.
        
        Args:
            request: The incoming request
            call_next: The next middleware/handler in the chain
            
        Returns:
            Response from the next handler
        """
        # Record start time
        start_time = time.time()
        
        # Get client information
        client_info = self._get_client_info(request)
        
        # Get request size
        request_size = self._get_request_size(request)
        
        # Log incoming request
        self._log_request(request, client_info)
        
        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log exception and re-raise
            duration = time.time() - start_time
            
            log_data = {
                "event": "request_exception",
                "timestamp": time.time(),
                "client": client_info,
                "request": self._get_request_info(request),
                "exception": {
                    "type": type(e).__name__,
                    "message": str(e),
                },
                "performance": {
                    "duration_seconds": round(duration, 4),
                    "duration_ms": round(duration * 1000, 2),
                }
            }
            
            logger.error(
                f"Request exception: {request.method} {request.url.path} - {type(e).__name__}",
                extra=log_data,
                exc_info=True
            )
            
            raise
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        self._log_response(request, response, client_info, duration, request_size)
        
        return response


class MetricsCollector:
    """
    Simple in-memory metrics collector for monitoring API performance.
    
    In production, this should be replaced with a proper metrics system
    like Prometheus, StatsD, or similar.
    """
    
    def __init__(self):
        """Initialize the metrics collector."""
        self.metrics = {
            "requests_total": 0,
            "requests_by_method": {},
            "requests_by_status": {},
            "response_times": [],
            "errors_total": 0,
            "start_time": time.time(),
        }
    
    def record_request(
        self,
        method: str,
        status_code: int,
        duration: float,
        path: str = None
    ) -> None:
        """
        Record a request for metrics collection.
        
        Args:
            method: HTTP method
            status_code: Response status code
            duration: Request duration in seconds
            path: Request path (optional)
        """
        self.metrics["requests_total"] += 1
        
        # Track by method
        if method not in self.metrics["requests_by_method"]:
            self.metrics["requests_by_method"][method] = 0
        self.metrics["requests_by_method"][method] += 1
        
        # Track by status code
        if status_code not in self.metrics["requests_by_status"]:
            self.metrics["requests_by_status"][status_code] = 0
        self.metrics["requests_by_status"][status_code] += 1
        
        # Track response times (keep last 1000 for memory efficiency)
        self.metrics["response_times"].append(duration)
        if len(self.metrics["response_times"]) > 1000:
            self.metrics["response_times"] = self.metrics["response_times"][-1000:]
        
        # Track errors
        if status_code >= 400:
            self.metrics["errors_total"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current metrics summary.
        
        Returns:
            Dictionary containing current metrics
        """
        response_times = self.metrics["response_times"]
        uptime = time.time() - self.metrics["start_time"]
        
        metrics = {
            "uptime_seconds": round(uptime, 2),
            "requests_total": self.metrics["requests_total"],
            "requests_by_method": self.metrics["requests_by_method"],
            "requests_by_status": self.metrics["requests_by_status"],
            "errors_total": self.metrics["errors_total"],
            "error_rate": (
                self.metrics["errors_total"] / max(self.metrics["requests_total"], 1)
            ) * 100,
        }
        
        if response_times:
            metrics["response_times"] = {
                "count": len(response_times),
                "avg_ms": round(sum(response_times) / len(response_times) * 1000, 2),
                "min_ms": round(min(response_times) * 1000, 2),
                "max_ms": round(max(response_times) * 1000, 2),
            }
        
        return metrics


# Global metrics collector instance
metrics_collector = MetricsCollector()


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware for collecting performance metrics.
    
    This middleware works alongside LoggingMiddleware to collect
    quantitative metrics about API performance.
    """
    
    def __init__(self, app, collector: MetricsCollector = None):
        """
        Initialize the metrics middleware.
        
        Args:
            app: The FastAPI application
            collector: Metrics collector instance (uses global if None)
        """
        super().__init__(app)
        self.collector = collector or metrics_collector
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process the request and collect metrics.
        
        Args:
            request: The incoming request
            call_next: The next middleware/handler in the chain
            
        Returns:
            Response from the next handler
        """
        start_time = time.time()
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Record metrics
            self.collector.record_request(
                method=request.method,
                status_code=response.status_code,
                duration=duration,
                path=request.url.path
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            
            # Record error metrics (assume 500 status)
            self.collector.record_request(
                method=request.method,
                status_code=500,
                duration=duration,
                path=request.url.path
            )
            
            raise