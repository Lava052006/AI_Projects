"""Tests for TextAnalyzer functionality."""

import pytest
from app.analyzers.text_analyzer import TextAnalyzer
from app.models.internal import RiskCategory


class TestTextAnalyzer:
    """Test cases for TextAnalyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = TextAnalyzer()
    
    def test_empty_text_analysis(self):
        """Test analysis of empty job text."""
        result = self.analyzer.analyze("")
        
        assert result.analyzer_name == "TextAnalyzer"
        assert result.confidence == 1.0
        assert len(result.risk_factors) == 1
        assert result.risk_factors[0].severity == 100
        assert "empty" in result.risk_factors[0].description.lower()
    
    def test_legitimate_job_analysis(self):
        """Test analysis of a legitimate job posting."""
        legitimate_job = """
        Software Engineer Position
        
        We are seeking a skilled Software Engineer with 3+ years of experience in Python development.
        
        Requirements:
        - Bachelor's degree in Computer Science or related field
        - Experience with Python, FastAPI, and SQL databases
        - Knowledge of Docker and AWS preferred
        - Strong problem-solving skills
        
        Responsibilities:
        - Develop and maintain web applications
        - Collaborate with cross-functional teams
        - Write clean, maintainable code
        
        Benefits:
        - Health insurance
        - 401k matching
        - Paid time off
        """
        
        result = self.analyzer.analyze(legitimate_job)
        
        assert result.analyzer_name == "TextAnalyzer"
        assert result.confidence > 0.7
        # Should have minimal risk factors for legitimate job
        assert len(result.risk_factors) <= 2
    
    def test_suspicious_job_analysis(self):
        """Test analysis of a suspicious job posting."""
        suspicious_job = """
        URGENT!!! MAKE MONEY FAST!!!
        
        Work from home! No experience required! Guaranteed income!
        Easy money handling and money transfer duties.
        Start immediately! Call 555-123-4567 or email scam@fake.com
        
        $5000 per week guaranteed!!!
        """
        
        result = self.analyzer.analyze(suspicious_job)
        
        assert result.analyzer_name == "TextAnalyzer"
        assert len(result.risk_factors) > 0
        
        # Should detect multiple fraud indicators
        fraud_categories = [rf.description for rf in result.risk_factors]
        assert any("keywords" in desc.lower() for desc in fraud_categories)
        assert any("capital letters" in desc.lower() for desc in fraud_categories)
    
    def test_short_job_description(self):
        """Test analysis of very short job description."""
        short_job = "Need worker. Good pay."
        
        result = self.analyzer.analyze(short_job)
        
        assert result.analyzer_name == "TextAnalyzer"
        assert len(result.risk_factors) > 0
        
        # Should flag short description
        descriptions = [rf.description for rf in result.risk_factors]
        assert any("short" in desc.lower() for desc in descriptions)
    
    def test_money_transfer_keywords(self):
        """Test detection of money transfer fraud keywords."""
        money_transfer_job = """
        Administrative Assistant needed for money transfer operations.
        Handle wire transfers and Western Union transactions.
        Process payments and transfer funds daily.
        """
        
        result = self.analyzer.analyze(money_transfer_job)
        
        assert len(result.risk_factors) > 0
        descriptions = [rf.description for rf in result.risk_factors]
        assert any("money" in desc.lower() and "transfer" in desc.lower() for desc in descriptions)
    
    def test_confidence_calculation(self):
        """Test that confidence scores are calculated properly."""
        # Short text should have lower confidence
        short_result = self.analyzer.analyze("Short job description.")
        
        # Longer text should have higher confidence
        long_result = self.analyzer.analyze("This is a much longer job description " * 20)
        
        assert isinstance(short_result.confidence, float)
        assert isinstance(long_result.confidence, float)
        assert 0.0 <= short_result.confidence <= 1.0
        assert 0.0 <= long_result.confidence <= 1.0