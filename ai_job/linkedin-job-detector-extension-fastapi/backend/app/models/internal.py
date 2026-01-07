"""Internal data models for risk analysis processing."""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum


class RiskCategory(str, Enum):
    """Categories of risk factors that can be identified."""
    TEXT_ANALYSIS = "text_analysis"
    EMAIL_VALIDATION = "email_validation"
    URL_VALIDATION = "url_validation"
    PLATFORM_CREDIBILITY = "platform_credibility"
    GENERAL = "general"


class RiskFactor(BaseModel):
    """Represents a specific risk factor identified during analysis.
    
    Used internally to track individual risk indicators before aggregation.
    """
    category: RiskCategory = Field(
        ...,
        description="The category of risk this factor belongs to"
    )
    severity: int = Field(
        ...,
        ge=0,
        le=100,
        description="Severity score for this risk factor (0-100)"
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Human-readable description of the risk factor"
    )
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence level in this risk factor assessment (0.0-1.0)"
    )

    @validator('description')
    def validate_description(cls, v):
        """Ensure description is not empty or just whitespace."""
        if not v or not v.strip():
            raise ValueError('Risk factor description cannot be empty')
        return v.strip()

    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class AnalysisResult(BaseModel):
    """Results from an individual analyzer component.
    
    Used to aggregate results from different analysis components.
    """
    risk_factors: List[RiskFactor] = Field(
        default_factory=list,
        description="List of risk factors identified by this analyzer"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall confidence in this analysis result (0.0-1.0)"
    )
    analyzer_name: str = Field(
        ...,
        min_length=1,
        description="Name of the analyzer that produced this result"
    )
    processing_time_ms: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Time taken to process this analysis in milliseconds"
    )

    @validator('analyzer_name')
    def validate_analyzer_name(cls, v):
        """Ensure analyzer name is not empty."""
        if not v or not v.strip():
            raise ValueError('Analyzer name cannot be empty')
        return v.strip()

    def get_max_severity(self) -> int:
        """Get the maximum severity score from all risk factors."""
        if not self.risk_factors:
            return 0
        return max(factor.severity for factor in self.risk_factors)

    def get_weighted_severity(self) -> float:
        """Get severity weighted by confidence scores."""
        if not self.risk_factors:
            return 0.0
        
        total_weighted = sum(
            factor.severity * factor.confidence 
            for factor in self.risk_factors
        )
        total_confidence = sum(factor.confidence for factor in self.risk_factors)
        
        if total_confidence == 0:
            return 0.0
        
        return total_weighted / total_confidence

    class Config:
        """Pydantic configuration."""
        use_enum_values = True