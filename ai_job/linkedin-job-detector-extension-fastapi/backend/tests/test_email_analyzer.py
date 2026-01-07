"""Tests for EmailAnalyzer functionality."""

import pytest
from app.analyzers.email_analyzer import EmailAnalyzer
from app.models.internal import RiskCategory


class TestEmailAnalyzer:
    """Test cases for EmailAnalyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = EmailAnalyzer()
    
    def test_valid_email_analysis(self):
        """Test analysis of a valid professional email."""
        result = self.analyzer.analyze("john.doe@company.com")
        
        assert result.analyzer_name == "EmailAnalyzer"
        assert result.confidence > 0.8
        # Valid professional email should have minimal risk factors
        assert len(result.risk_factors) == 0
    
    def test_invalid_email_format(self):
        """Test analysis of invalid email format."""
        result = self.analyzer.analyze("invalid-email-format")
        
        assert result.analyzer_name == "EmailAnalyzer"
        assert result.confidence > 0.8
        assert len(result.risk_factors) >= 1
        
        # Should detect invalid format
        format_errors = [rf for rf in result.risk_factors 
                        if "Invalid email format" in rf.description]
        assert len(format_errors) == 1
        assert format_errors[0].severity >= 90
    
    def test_empty_email_analysis(self):
        """Test analysis of empty email."""
        result = self.analyzer.analyze("")
        
        assert result.analyzer_name == "EmailAnalyzer"
        assert result.confidence == 1.0
        assert len(result.risk_factors) == 1
        assert result.risk_factors[0].severity == 100
        assert "empty or missing" in result.risk_factors[0].description.lower()
    
    def test_disposable_email_detection(self):
        """Test detection of disposable email services."""
        result = self.analyzer.analyze("test@10minutemail.com")
        
        assert result.analyzer_name == "EmailAnalyzer"
        assert len(result.risk_factors) >= 1
        
        # Should detect disposable email patterns
        disposable_flags = [rf for rf in result.risk_factors 
                           if "disposable" in rf.description.lower() or 
                              "temporary" in rf.description.lower()]
        assert len(disposable_flags) >= 1
    
    def test_personal_email_provider(self):
        """Test detection of personal email providers."""
        result = self.analyzer.analyze("recruiter@gmail.com")
        
        assert result.analyzer_name == "EmailAnalyzer"
        # Should flag personal email provider usage
        personal_flags = [rf for rf in result.risk_factors 
                         if "personal email provider" in rf.description.lower()]
        assert len(personal_flags) == 1
        assert personal_flags[0].severity <= 30  # Low severity
    
    def test_suspicious_patterns(self):
        """Test detection of suspicious email patterns."""
        result = self.analyzer.analyze("123456789012345678901234@suspicious.tk")
        
        assert result.analyzer_name == "EmailAnalyzer"
        assert len(result.risk_factors) >= 2
        
        # Should detect multiple suspicious patterns
        pattern_types = [rf.description for rf in result.risk_factors]
        assert any("randomly generated" in desc.lower() for desc in pattern_types)
        assert any("suspicious" in desc.lower() for desc in pattern_types)
    
    def test_risk_factor_categories(self):
        """Test that all risk factors use correct category."""
        result = self.analyzer.analyze("invalid@format")
        
        for risk_factor in result.risk_factors:
            assert risk_factor.category == RiskCategory.EMAIL_VALIDATION
            assert 0 <= risk_factor.severity <= 100
            assert 0.0 <= risk_factor.confidence <= 1.0
            assert len(risk_factor.description) > 0
    
    def test_confidence_calculation(self):
        """Test confidence score calculation."""
        # Valid email should have high confidence
        valid_result = self.analyzer.analyze("professional@company.com")
        assert valid_result.confidence >= 0.8
        
        # Invalid email should still have high confidence in the analysis
        invalid_result = self.analyzer.analyze("invalid-format")
        assert invalid_result.confidence >= 0.8
        
        # Empty email should have maximum confidence
        empty_result = self.analyzer.analyze("")
        assert empty_result.confidence == 1.0