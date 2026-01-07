"""Custom error handlers for the Job Analysis API."""

import json
import logging
from typing import Dict, Any
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle Pydantic validation errors (422 Unprocessable Entity).
    
    Args:
        request: The FastAPI request object
        exc: The validation error exception
        
    Returns:
        JSONResponse with detailed validation error information
    """
    logger.warning(f"Validation error on {request.url}: {exc.errors()}")
    
    # Format validation errors for better user experience
    formatted_errors = []
    for error in exc.errors():
        formatted_errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error in request data",
            "errors": formatted_errors
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions with consistent error format.
    
    Args:
        request: The FastAPI request object
        exc: The HTTP exception
        
    Returns:
        JSONResponse with error details
    """
    logger.warning(f"HTTP {exc.status_code} error on {request.url}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions (500 Internal Server Error).
    
    Args:
        request: The FastAPI request object
        exc: The unexpected exception
        
    Returns:
        JSONResponse with generic error message
    """
    # Log the full error for debugging but don't expose sensitive details
    logger.error(f"Unexpected error on {request.url}: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal error occurred while processing the request",
            "status_code": 500
        }
    )


async def malformed_json_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle malformed JSON requests (400 Bad Request).
    
    Args:
        request: The FastAPI request object
        exc: The JSON parsing exception
        
    Returns:
        JSONResponse with JSON parsing error details
    """
    logger.warning(f"Malformed JSON on {request.url}: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Invalid JSON format in request body",
            "status_code": 400
        }
    )


def create_error_response(status_code: int, message: str, details: Dict[str, Any] = None) -> JSONResponse:
    """
    Create a standardized error response.
    
    Args:
        status_code: HTTP status code
        message: Error message
        details: Optional additional details
        
    Returns:
        JSONResponse with standardized error format
    """
    content = {
        "detail": message,
        "status_code": status_code
    }
    
    if details:
        content.update(details)
    
    return JSONResponse(
        status_code=status_code,
        content=content
    )