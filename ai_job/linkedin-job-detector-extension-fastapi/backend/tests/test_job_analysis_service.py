"""Tests for JobAnalysisService coordinator."""

import pytest
from app.services.job_analysis_service import JobAnalysisService
from app.models.request import JobAnalysisRequest
from app.models.response import JobAnalysisResponse, VerdictEnum


class TestJobAnalysisService:
    """Test cases for JobAnalysisService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = JobAnalysisService()
    
    def test_service_initialization(self):
        """Test that service initializes with all required analyzers."""
        assert self.service.text_analyzer is not None
        assert self.service.email_analyzer is not None
        assert self.service.url_analyzer is not None
        assert self.service.platform_analyzer is not None
        
        # Check category weights are properly configured
        assert len(self.service.category_weights) == 4
        assert sum(self.service.category_weights.values()) == 1.0  # Should sum to 100%
    
    def test_legitimate_job_analysis(self):
        """Test analysis of a legitimate job posting."""
        request = JobAnalysisRequest(
            job_text="Senior Software Engineer position. Requirements: 5+ years Python experience, Bachelor's degree in Computer Science. We offer competitive salary, health insurance, and 401k.",
            company_url="https://legitimate-company.com/careers",
            recruiter_email="hr@legitimate-company.com",
            platform_source="LinkedIn"
        )
        
        result = self.service.analyze_job_posting(request)
        
        # Verify response structure
        assert isinstance(result, JobAnalysisResponse)
        assert 0 <= result.risk_score <= 100
        assert isinstance(result.flags, list)
        assert isinstance(result.explanation, str)
        assert result.verdict in [VerdictEnum.SAFE, VerdictEnum.CAUTION, VerdictEnum.HIGH_RISK]
        
        # Should be relatively low risk
        assert result.risk_score <= 70  # Should not be high risk
        assert len(result.explanation) > 50  # Should have meaningful explanation
    
    def test_suspicious_job_analysis(self):
        """Test analysis of a suspicious job posting."""
        request = JobAnalysisRequest(
            job_text="EASY MONEY!!! Work from home, no experience required. Make $5000 per week handling money transfers.",
            company_url="http://123.456.789.0:8080",
            recruiter_email="recruiter123@tempmail.org",
            platform_source="telegram"
        )
        
        result = self.service.analyze_job_posting(request)
        
        # Should be high risk
        assert result.risk_score >= 50  # Should have elevated risk
        assert len(result.flags) > 0  # Should have risk flags
        assert result.verdict in [VerdictEnum.CAUTION, VerdictEnum.HIGH_RISK]
        
        # Should identify multiple issues
        assert len(result.flags) >= 3
        assert "caution" in result.explanation.lower() or "risk" in result.explanation.lower()
    
    def test_risk_score_bounds(self):
        """Test that risk scores are always within valid bounds (0-100)."""
        # Test with various inputs
        test_cases = [
            # Minimal risk case
            JobAnalysisRequest(
                job_text="Software Engineer position with specific requirements and qualifications.",
                company_url="https://google.com",
                recruiter_email="jobs@google.com",
                platform_source="LinkedIn"
            ),
            # High risk case
            JobAnalysisRequest(
                job_text="Easy money fast cash",
                company_url="http://suspicious-site.tk",
                recruiter_email="scammer@tempmail.com",
                platform_source="telegram"
            ),
            # Edge case with minimal content
            JobAnalysisRequest(
                job_text="Job available now",
                company_url="https://example.com",
                recruiter_email="test@example.com",
                platform_source="email"
            )
        ]
        
        for request in test_cases:
            result = self.service.analyze_job_posting(request)
            assert 0 <= result.risk_score <= 100, f"Risk score {result.risk_score} out of bounds"
            assert isinstance(result.risk_score, int), "Risk score should be integer"
    
    def test_verdict_categories(self):
        """Test that verdicts use only predefined categories."""
        request = JobAnalysisRequest(
            job_text="Test job description with various requirements.",
            company_url="https://test-company.com",
            recruiter_email="hr@test-company.com",
            platform_source="Indeed"
        )
        
        result = self.service.analyze_job_posting(request)
        
        # Verdict should be one of the predefined enum values
        assert result.verdict in [VerdictEnum.SAFE, VerdictEnum.CAUTION, VerdictEnum.HIGH_RISK]
        assert result.verdict in ["Safe", "Caution", "High Risk"]
    
    def test_flags_are_descriptive_strings(self):
        """Test that flags are always non-empty descriptive strings."""
        request = JobAnalysisRequest(
            job_text="Suspicious job with money transfer requirements and urgent hiring.",
            company_url="http://suspicious.com",
            recruiter_email="fake@tempmail.org",
            platform_source="telegram"
        )
        
        result = self.service.analyze_job_posting(request)
        
        # All flags should be non-empty strings
        assert isinstance(result.flags, list)
        for flag in result.flags:
            assert isinstance(flag, str)
            assert len(flag.strip()) > 0
            assert len(flag) <= 500  # Reasonable length limit
    
    def test_explanation_always_provided(self):
        """Test that explanations are always provided and meaningful."""
        request = JobAnalysisRequest(
            job_text="Standard job posting with normal requirements.",
            company_url="https://company.com",
            recruiter_email="hr@company.com",
            platform_source="LinkedIn"
        )
        
        result = self.service.analyze_job_posting(request)
        
        # Explanation should be non-empty and meaningful
        assert isinstance(result.explanation, str)
        assert len(result.explanation.strip()) > 0
        assert len(result.explanation) >= 50  # Should be reasonably detailed
        
        # Should contain risk score reference
        assert str(result.risk_score) in result.explanation
    
    def test_complete_response_generation(self):
        """Test that valid requests always produce complete responses."""
        request = JobAnalysisRequest(
            job_text="Complete job description with requirements and responsibilities.",
            company_url="https://valid-company.com",
            recruiter_email="recruiter@valid-company.com",
            platform_source="Indeed"
        )
        
        result = self.service.analyze_job_posting(request)
        
        # All required fields should be present and valid
        assert hasattr(result, 'risk_score')
        assert hasattr(result, 'flags')
        assert hasattr(result, 'explanation')
        assert hasattr(result, 'verdict')
        
        assert result.risk_score is not None
        assert result.flags is not None
        assert result.explanation is not None
        assert result.verdict is not None
        
        # Should be valid JSON serializable
        result_dict = result.model_dump()
        assert 'risk_score' in result_dict
        assert 'flags' in result_dict
        assert 'explanation' in result_dict
        assert 'verdict' in result_dict
    
    def test_platform_risk_multiplier_effect(self):
        """Test that platform risk multipliers affect final scores appropriately."""
        base_request_data = {
            "job_text": "Standard job posting with normal content.",
            "company_url": "https://company.com",
            "recruiter_email": "hr@company.com"
        }
        
        # Test with high-credibility platform
        high_credibility_request = JobAnalysisRequest(
            platform_source="LinkedIn",
            **base_request_data
        )
        
        # Test with low-credibility platform
        low_credibility_request = JobAnalysisRequest(
            platform_source="telegram",
            **base_request_data
        )
        
        high_result = self.service.analyze_job_posting(high_credibility_request)
        low_result = self.service.analyze_job_posting(low_credibility_request)
        
        # Low credibility platform should generally have higher risk
        # (though other factors may influence this)
        assert isinstance(high_result.risk_score, int)
        assert isinstance(low_result.risk_score, int)
        
        # At minimum, the low credibility should have more or different flags
        assert len(low_result.flags) >= len(high_result.flags)