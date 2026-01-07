"""Rate limiting middleware for the Job Analysis API."""

import time
import logging
from typing import Dict, Optional
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse

logger = logging.getLogger(__name__)


class RateLimitingMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware that tracks requests per client IP.
    
    Implements a simple sliding window rate limiter that allows a configurable
    number of requests per time window per client.
    """
    
    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        cleanup_interval: int = 300  # 5 minutes
    ):
        """
        Initialize the rate limiting middleware.
        
        Args:
            app: The FastAPI application
            requests_per_minute: Maximum requests per minute per client
            requests_per_hour: Maximum requests per hour per client
            cleanup_interval: How often to clean up old entries (seconds)
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.cleanup_interval = cleanup_interval
        
        # In-memory storage for request tracking
        # In production, consider using Redis or similar
        self.request_counts: Dict[str, Dict[str, list]] = {}
        self.last_cleanup = time.time()
    
    def _get_client_ip(self, request: Request) -> str:
        """
        Extract client IP address from request.
        
        Args:
            request: The FastAPI request object
            
        Returns:
            Client IP address as string
        """
        # Check for forwarded headers first (for proxy/load balancer scenarios)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fall back to direct client IP
        return request.client.host if request.client else "unknown"
    
    def _cleanup_old_entries(self):
        """Remove old request entries to prevent memory leaks."""
        current_time = time.time()
        
        # Only cleanup periodically to avoid performance impact
        if current_time - self.last_cleanup < self.cleanup_interval:
            return
        
        cutoff_time_minute = current_time - 60  # 1 minute ago
        cutoff_time_hour = current_time - 3600  # 1 hour ago
        
        for client_ip in list(self.request_counts.keys()):
            client_data = self.request_counts[client_ip]
            
            # Clean up minute-based tracking
            if "minute" in client_data:
                client_data["minute"] = [
                    timestamp for timestamp in client_data["minute"]
                    if timestamp > cutoff_time_minute
                ]
            
            # Clean up hour-based tracking
            if "hour" in client_data:
                client_data["hour"] = [
                    timestamp for timestamp in client_data["hour"]
                    if timestamp > cutoff_time_hour
                ]
            
            # Remove client entry if no recent requests
            if (not client_data.get("minute") and not client_data.get("hour")):
                del self.request_counts[client_ip]
        
        self.last_cleanup = current_time
    
    def _is_rate_limited(self, client_ip: str) -> Optional[str]:
        """
        Check if a client IP is rate limited.
        
        Args:
            client_ip: Client IP address
            
        Returns:
            Error message if rate limited, None otherwise
        """
        current_time = time.time()
        
        # Initialize client data if not exists
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = {"minute": [], "hour": []}
        
        client_data = self.request_counts[client_ip]
        
        # Check minute-based rate limit
        minute_cutoff = current_time - 60
        recent_minute_requests = [
            timestamp for timestamp in client_data["minute"]
            if timestamp > minute_cutoff
        ]
        
        if len(recent_minute_requests) >= self.requests_per_minute:
            return f"Rate limit exceeded: {self.requests_per_minute} requests per minute"
        
        # Check hour-based rate limit
        hour_cutoff = current_time - 3600
        recent_hour_requests = [
            timestamp for timestamp in client_data["hour"]
            if timestamp > hour_cutoff
        ]
        
        if len(recent_hour_requests) >= self.requests_per_hour:
            return f"Rate limit exceeded: {self.requests_per_hour} requests per hour"
        
        return None
    
    def _record_request(self, client_ip: str):
        """
        Record a request for the given client IP.
        
        Args:
            client_ip: Client IP address
        """
        current_time = time.time()
        
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = {"minute": [], "hour": []}
        
        client_data = self.request_counts[client_ip]
        client_data["minute"].append(current_time)
        client_data["hour"].append(current_time)
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process the request and apply rate limiting.
        
        Args:
            request: The incoming request
            call_next: The next middleware/handler in the chain
            
        Returns:
            Response from the next handler or rate limit error
        """
        # Skip rate limiting for health check endpoints
        if request.url.path in ["/", "/health", "/api/v1/health"]:
            return await call_next(request)
        
        # Cleanup old entries periodically
        self._cleanup_old_entries()
        
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Check if rate limited
        rate_limit_error = self._is_rate_limited(client_ip)
        if rate_limit_error:
            logger.warning(f"Rate limit exceeded for client {client_ip}: {rate_limit_error}")
            
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": rate_limit_error,
                    "status_code": 429,
                    "retry_after": 60  # Suggest retry after 1 minute
                }
            )
        
        # Record the request
        self._record_request(client_ip)
        
        # Log the request for monitoring
        logger.info(f"Request from {client_ip} to {request.url.path}")
        
        # Continue to next handler
        return await call_next(request)