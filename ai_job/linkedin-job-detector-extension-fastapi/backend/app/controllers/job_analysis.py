"""Job Analysis Controller - Handles the /analyze-job POST endpoint."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import logging
from typing import Dict, Any

from app.models.request import JobAnalysisRequest
from app.models.response import JobAnalysisResponse
from app.services.job_analysis_service import JobAnalysisService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1",
    tags=["job-analysis"],
    responses={
        400: {"description": "Bad Request - Malformed JSON"},
        422: {"description": "Unprocessable Entity - Validation Error"},
        429: {"description": "Too Many Requests - Rate Limit Exceeded"},
        500: {"description": "Internal Server Error"},
    }
)

# Initialize service
job_analysis_service = JobAnalysisService()


@router.post(
    "/analyze-job",
    response_model=JobAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze Job Posting",
    description="Analyze a job posting for potential fraud and suspicious activity",
    responses={
        200: {
            "description": "Successful analysis",
            "model": JobAnalysisResponse,
        },
        400: {
            "description": "Bad Request - Malformed JSON or invalid request format",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid JSON format in request body",
                        "status_code": 400
                    }
                }
            }
        },
        422: {
            "description": "Unprocessable Entity - Missing required fields or invalid field values",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Validation error in request data",
                        "errors": [
                            {
                                "field": "body -> job_text",
                                "message": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        },
        429: {
            "description": "Too Many Requests - Rate limit exceeded",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Rate limit exceeded: 60 requests per minute",
                        "status_code": 429,
                        "retry_after": 60
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error - Unexpected system failure",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "An internal error occurred while processing the request",
                        "status_code": 500
                    }
                }
            }
        }
    }
)
async def analyze_job_posting(request: JobAnalysisRequest) -> JobAnalysisResponse:
    """
    Analyze a job posting for potential fraud and suspicious activity.
    
    This endpoint accepts job posting details and returns a comprehensive risk assessment
    including risk score, flags, explanation, and verdict.
    
    Args:
        request: JobAnalysisRequest containing job posting data
        
    Returns:
        JobAnalysisResponse with risk assessment results
        
    Raises:
        HTTPException: For various error conditions (400, 422, 429, 500)
    """
    try:
        logger.info(f"Received job analysis request for platform: {request.platform_source}")
        
        # Perform the analysis using the service
        result = job_analysis_service.analyze_job_posting(request)
        
        logger.info(
            f"Analysis completed - Risk Score: {result.risk_score}, "
            f"Verdict: {result.verdict}, Flags: {len(result.flags)}"
        )
        
        return result
        
    except Exception as e:
        # Log the error and re-raise to be handled by global exception handler
        logger.error(f"Error in job analysis: {str(e)}", exc_info=True)
        raise


@router.get(
    "/health",
    summary="Health Check",
    description="Check if the job analysis service is healthy and operational",
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "service": "job-analysis-controller",
                        "analyzers": {
                            "text_analyzer": "operational",
                            "email_analyzer": "operational", 
                            "url_analyzer": "operational",
                            "platform_analyzer": "operational"
                        }
                    }
                }
            }
        }
    }
)
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for the job analysis controller.
    
    Returns:
        Dictionary with health status information
    """
    try:
        # Test that the service can be instantiated (basic health check)
        test_service = JobAnalysisService()
        
        return {
            "status": "healthy",
            "service": "job-analysis-controller",
            "analyzers": {
                "text_analyzer": "operational",
                "email_analyzer": "operational",
                "url_analyzer": "operational", 
                "platform_analyzer": "operational"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service health check failed"
        )