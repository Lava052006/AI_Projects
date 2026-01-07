"""Response models for the Job Analysis API."""

from pydantic import BaseModel, Field, validator
from typing import List, Literal
from enum import Enum


class VerdictEnum(str, Enum):
    """Enumeration for risk verdict categories."""
    SAFE = "Safe"
    CAUTION = "Caution"
    HIGH_RISK = "High Risk"


class ConfidenceEnum(str, Enum):
    """Enumeration for confidence levels."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class JobAnalysisResponse(BaseModel):
    """Response model for job analysis results.
    
    Contains risk assessment results with score, flags, explanation, verdict, and confidence.
    """
    risk_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="A numerical value (0-100) indicating the likelihood that a job posting is fraudulent or suspicious"
    )
    flags: List[str] = Field(
        ...,
        description="Specific indicators or warning signs identified in the job posting analysis"
    )
    explanation: str = Field(
        ...,
        min_length=1,
        description="Detailed reasoning behind the risk assessment and identified flags"
    )
    verdict: VerdictEnum = Field(
        ...,
        description="A categorical assessment based on the overall analysis"
    )
    confidence: ConfidenceEnum = Field(
        ...,
        description="Confidence level in the analysis based on available information and signal consistency"
    )

    @validator('flags')
    def validate_flags(cls, v):
        """Ensure all flags are non-empty strings."""
        if not isinstance(v, list):
            raise ValueError('Flags must be a list')
        
        # Filter out empty or whitespace-only flags
        valid_flags = []
        for flag in v:
            if isinstance(flag, str) and flag.strip():
                valid_flags.append(flag.strip())
        
        return valid_flags

    @validator('explanation')
    def validate_explanation(cls, v):
        """Ensure explanation is not empty or just whitespace."""
        if not v or not v.strip():
            raise ValueError('Explanation cannot be empty or only whitespace')
        return v.strip()

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        schema_extra = {
            "example": {
                "risk_score": 25,
                "flags": [
                    "Email domain has low reputation",
                    "Job description contains vague requirements"
                ],
                "explanation": "The job posting shows some minor red flags including a recruiter email from a domain with limited online presence and somewhat vague job requirements (medium confidence). However, the company URL appears legitimate and the platform source is reputable.",
                "verdict": "Caution",
                "confidence": "Medium"
            }
        }