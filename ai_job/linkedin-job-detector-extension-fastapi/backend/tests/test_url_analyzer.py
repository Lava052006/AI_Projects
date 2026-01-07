"""Tests for URLAnalyzer functionality."""

import pytest
from app.analyzers.url_analyzer import URLAnalyzer
from app.models.internal import RiskCategory


class TestURLAnalyzer:
    """Test cases for URLAnalyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = URLAnalyzer()
    
    def test_valid_url_analysis(self):
        """Test analysis of a valid company URL."""
        result = self.analyzer.analyze("https://www.company.com")
        
        assert result.analyzer_name == "URLAnalyzer"
        assert result.confidence > 0.8
        # Valid company URL should have minimal risk factors
        assert len(result.risk_factors) <= 1  # Might have minor issues like HTTP vs HTTPS
    
    def test_invalid_url_format(self):
        """Test analysis of invalid URL format."""
        result = self.analyzer.analyze("not-a-valid-url")
        
        assert result.analyzer_name == "URLAnalyzer"
        assert result.confidence > 0.8
        assert len(result.risk_factors) >= 1
        
        # Should detect invalid format
        format_errors = [rf for rf in result.risk_factors 
                        if "Invalid URL format" in rf.description]
        assert len(format_errors) == 1
        assert format_errors[0].severity >= 90
    
    def test_empty_url_analysis(self):
        """Test analysis of empty URL."""
        result = self.analyzer.analyze("")
        
        assert result.analyzer_name == "URLAnalyzer"
        assert result.confidence == 1.0
        assert len(result.risk_factors) == 1
        assert result.risk_factors[0].severity == 100
        assert "empty or missing" in result.risk_factors[0].description.lower()
    
    def test_ip_address_detection(self):
        """Test detection of IP addresses instead of domain names."""
        result = self.analyzer.analyze("http://192.168.1.1")
        
        assert result.analyzer_name == "URLAnalyzer"
        assert len(result.risk_factors) >= 1
        
        # Should detect IP address usage
        ip_flags = [rf for rf in result.risk_factors 
                   if "IP address" in rf.description]
        assert len(ip_flags) >= 1
        assert ip_flags[0].severity >= 70
    
    def test_suspicious_tld_detection(self):
        """Test detection of suspicious top-level domains."""
        result = self.analyzer.analyze("https://company.tk")
        
        assert result.analyzer_name == "URLAnalyzer"
        assert len(result.risk_factors) >= 1
        
        # Should detect suspicious TLD
        tld_flags = [rf for rf in result.risk_factors 
                    if "suspicious top-level domain" in rf.description.lower()]
        assert len(tld_flags) >= 1
    
    def test_url_shortener_detection(self):
        """Test detection of URL shortening services."""
        result = self.analyzer.analyze("https://bit.ly/company")
        
        assert result.analyzer_name == "URLAnalyzer"
        assert len(result.risk_factors) >= 1
        
        # Should detect URL shortener
        shortener_flags = [rf for rf in result.risk_factors 
                          if "shortening" in rf.description.lower()]
        assert len(shortener_flags) >= 1
        assert shortener_flags[0].severity >= 70
    
    def test_http_vs_https(self):
        """Test detection of insecure HTTP protocol."""
        result = self.analyzer.analyze("http://company.com")
        
        assert result.analyzer_name == "URLAnalyzer"
        
        # Should flag HTTP as less secure
        http_flags = [rf for rf in result.risk_factors 
                     if "insecure HTTP" in rf.description]
        assert len(http_flags) >= 1
        assert http_flags[0].severity <= 50  # Should be low-medium severity
    
    def test_suspicious_domain_patterns(self):
        """Test detection of suspicious domain patterns."""
        result = self.analyzer.analyze("https://randomstring12345.com")
        
        assert result.analyzer_name == "URLAnalyzer"
        
        # Should detect random-looking domain
        random_flags = [rf for rf in result.risk_factors 
                       if "randomly generated" in rf.description.lower()]
        assert len(random_flags) >= 1
    
    def test_excessive_subdomains(self):
        """Test detection of excessive subdomains."""
        result = self.analyzer.analyze("https://a.b.c.d.e.company.com")
        
        assert result.analyzer_name == "URLAnalyzer"
        
        # Should detect excessive subdomains
        subdomain_flags = [rf for rf in result.risk_factors 
                          if "excessive" in rf.description.lower() and 
                             "subdomain" in rf.description.lower()]
        assert len(subdomain_flags) >= 1
    
    def test_suspicious_ports(self):
        """Test detection of suspicious port numbers."""
        result = self.analyzer.analyze("https://company.com:8080")
        
        assert result.analyzer_name == "URLAnalyzer"
        
        # Should detect suspicious port
        port_flags = [rf for rf in result.risk_factors 
                     if "suspicious port" in rf.description.lower()]
        assert len(port_flags) >= 1
    
    def test_risk_factor_categories(self):
        """Test that all risk factors use correct category."""
        result = self.analyzer.analyze("invalid-url-format")
        
        for risk_factor in result.risk_factors:
            assert risk_factor.category == RiskCategory.URL_VALIDATION
            assert 0 <= risk_factor.severity <= 100
            assert 0.0 <= risk_factor.confidence <= 1.0
            assert len(risk_factor.description) > 0
    
    def test_confidence_calculation(self):
        """Test confidence score calculation."""
        # Valid URL should have high confidence
        valid_result = self.analyzer.analyze("https://www.company.com")
        assert valid_result.confidence >= 0.8
        
        # Invalid URL should still have high confidence in the analysis
        invalid_result = self.analyzer.analyze("invalid-format")
        assert invalid_result.confidence >= 0.8
        
        # Empty URL should have maximum confidence
        empty_result = self.analyzer.analyze("")
        assert empty_result.confidence == 1.0
    
    def test_domain_legitimacy_checks(self):
        """Test various domain legitimacy checks."""
        # Very short domain
        short_result = self.analyzer.analyze("https://ab.com")
        short_flags = [rf for rf in short_result.risk_factors 
                      if "unusually short" in rf.description.lower()]
        assert len(short_flags) >= 1
        
        # Numbers-only domain
        numbers_result = self.analyzer.analyze("https://123456.com")
        numbers_flags = [rf for rf in numbers_result.risk_factors 
                        if "consists only of numbers" in rf.description.lower()]
        assert len(numbers_flags) >= 1
        
        # Excessive hyphens
        hyphens_result = self.analyzer.analyze("https://test-test-test-test-test.com")
        hyphens_flags = [rf for rf in hyphens_result.risk_factors 
                        if "hyphens" in rf.description.lower()]
        assert len(hyphens_flags) >= 1