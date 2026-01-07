"""JSON parsing middleware for handling malformed JSON requests."""

import json
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

logger = logging.getLogger(__name__)


class JSONParsingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle malformed JSON requests and return proper 400 errors.
    
    This middleware intercepts requests with JSON content-type and validates
    that the JSON is properly formatted before passing to the application.
    """
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process the request and validate JSON format if applicable.
        
        Args:
            request: The incoming request
            call_next: The next middleware/handler in the chain
            
        Returns:
            Response from the next handler or JSON parsing error
        """
        # Only check JSON for POST/PUT/PATCH requests with JSON content-type
        if (
            request.method in ["POST", "PUT", "PATCH"] and
            request.headers.get("content-type", "").startswith("application/json")
        ):
            try:
                # Try to read and parse the request body
                body = await request.body()
                
                if body:  # Only validate if there's actually a body
                    try:
                        json.loads(body)
                    except json.JSONDecodeError as e:
                        logger.warning(f"Malformed JSON in request to {request.url.path}: {str(e)}")
                        
                        return JSONResponse(
                            status_code=HTTP_400_BAD_REQUEST,
                            content={
                                "detail": "Invalid JSON format in request body",
                                "status_code": 400,
                                "error_type": "json_decode_error"
                            }
                        )
                
                # Recreate the request with the body we just read
                # This is necessary because the body can only be read once
                async def receive():
                    return {"type": "http.request", "body": body}
                
                # Replace the receive callable
                request._receive = receive
                
            except Exception as e:
                logger.error(f"Error processing request body: {str(e)}")
                
                return JSONResponse(
                    status_code=HTTP_400_BAD_REQUEST,
                    content={
                        "detail": "Error processing request body",
                        "status_code": 400
                    }
                )
        
        # Continue to next handler
        return await call_next(request)