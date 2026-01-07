"""URL analyzer for company URL validation and domain legitimacy assessment."""

import re
from typing import List, Set
from urllib.parse import urlparse
from app.models.internal import AnalysisResult, RiskFactor, RiskCategory


class URLAnalyzer:
    """Analyzes company URLs for format validation and domain legitimacy."""
    
    def __init__(self):
        """Initialize the URL analyzer with validation patterns and domain lists."""
        # Basic URL validation patterns
        self.url_pattern = re.compile(
            r'^https?://'  # Protocol
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # Domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # Optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        
        # Suspicious URL patterns
        self.suspicious_patterns = {
            'ip_address': re.compile(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'),
            'suspicious_tlds': re.compile(r'\.(?:tk|ml|ga|cf|click|download|zip|bit|ly|tinyurl)(?:/|$)', re.IGNORECASE),
            'url_shorteners': re.compile(r'(?:bit\.ly|tinyurl|t\.co|goo\.gl|short\.link|ow\.ly)', re.IGNORECASE),
            'excessive_subdomains': re.compile(r'^https?://(?:[^./]+\.){4,}'),  # 4+ subdomains
            'suspicious_keywords': re.compile(r'(?:free|temp|test|demo|fake|scam|phish)', re.IGNORECASE),
            'random_domains': re.compile(r'https?://[a-z0-9]{15,}\.(?:com|net|org)(?:/|$)', re.IGNORECASE)  # Very long random domains (15+ chars)
        }
        
        # Legitimate domain indicators
        self.legitimate_indicators = {
            'established_tlds': {'.com', '.org', '.net', '.edu', '.gov', '.co.uk', '.de', '.fr', '.ca'},
            'business_keywords': ['company', 'corp', 'inc', 'ltd', 'llc', 'group', 'solutions', 'tech', 'systems'],
            'professional_patterns': re.compile(r'(?:careers|jobs|hr|recruiting|talent)', re.IGNORECASE)
        }
        
        # Known suspicious domains and patterns
        self.suspicious_domains = {
            'typosquatting': [
                'gooogle.com', 'microsooft.com', 'amazoon.com', 'facebok.com',
                'linkedinn.com', 'appple.com', 'netflixx.com'
            ],
            'generic_suspicious': [
                'example.com', 'test.com', 'demo.com', 'temp.com',
                'fake.com', 'scam.com', 'phishing.com'
            ]
        }
        
        # Port number patterns (some ports are more suspicious)
        self.suspicious_ports = {8080, 8000, 3000, 4000, 5000, 9000, 9999}

    def analyze(self, company_url: str) -> AnalysisResult:
        """
        Analyze company URL for format validation and domain legitimacy.
        Only adds risk if URL exists AND is explicitly suspicious.
        
        Args:
            company_url: The company's URL to analyze
            
        Returns:
            AnalysisResult containing identified risk factors and confidence score
        """
        if not company_url or not company_url.strip():
            # Empty URL is neutral - no risk added
            return AnalysisResult(
                risk_factors=[],
                confidence=1.0,
                analyzer_name="URLAnalyzer"
            )
        
        url = company_url.strip()
        risk_factors = []
        
        # Basic format validation
        format_valid = self._validate_url_format(url, risk_factors)
        
        if format_valid:
            # Parse URL for detailed analysis
            parsed_url = urlparse(url)
            
            # Only check for explicitly suspicious patterns
            self._check_suspicious_patterns(url, risk_factors)
            
            # Check domain legitimacy for suspicious indicators only
            self._check_suspicious_domain_characteristics(parsed_url, risk_factors)
            
            # Check for URL shorteners and redirects
            self._check_url_shorteners(url, risk_factors)
            
            # Check for suspicious ports
            self._check_suspicious_ports(parsed_url, risk_factors)
        
        # Calculate confidence based on analysis completeness
        confidence = self._calculate_confidence(url, format_valid, len(risk_factors))
        
        return AnalysisResult(
            risk_factors=risk_factors,
            confidence=confidence,
            analyzer_name="URLAnalyzer"
        )

    def _validate_url_format(self, url: str, risk_factors: List[RiskFactor]) -> bool:
        """Validate basic URL format using regex and urllib.parse."""
        # Check basic URL pattern
        if not self.url_pattern.match(url):
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.URL_VALIDATION,
                    severity=90,
                    description="Invalid URL format",
                    confidence=1.0
                )
            )
            return False
        
        # Try to parse with urllib.parse for more detailed validation
        try:
            parsed = urlparse(url)
            
            # Check if scheme is present and valid
            if not parsed.scheme or parsed.scheme not in ['http', 'https']:
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.URL_VALIDATION,
                        severity=80,
                        description="Missing or invalid URL scheme (http/https)",
                        confidence=0.9
                    )
                )
                return False
            
            # Check if netloc (domain) is present
            if not parsed.netloc:
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.URL_VALIDATION,
                        severity=95,
                        description="Missing domain in URL",
                        confidence=1.0
                    )
                )
                return False
            
            # Check for extremely long URLs (potential spam)
            if len(url) > 2000:
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.URL_VALIDATION,
                        severity=50,
                        description="URL is unusually long",
                        confidence=0.7
                    )
                )
            
        except Exception:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.URL_VALIDATION,
                    severity=85,
                    description="URL cannot be parsed properly",
                    confidence=0.9
                )
            )
            return False
        
        return True

    def _check_suspicious_patterns(self, url: str, risk_factors: List[RiskFactor]) -> None:
        """Check for suspicious patterns in the URL."""
        for pattern_name, pattern in self.suspicious_patterns.items():
            if pattern.search(url):
                severity_map = {
                    'ip_address': 70,
                    'suspicious_tlds': 60,
                    'url_shorteners': 75,
                    'excessive_subdomains': 55,
                    'suspicious_keywords': 65,
                    'random_domains': 50
                }
                
                description_map = {
                    'ip_address': "Uses IP address instead of domain name",
                    'suspicious_tlds': "Uses suspicious top-level domain",
                    'url_shorteners': "Uses URL shortening service",
                    'excessive_subdomains': "Has excessive number of subdomains",
                    'suspicious_keywords': "Contains suspicious keywords in domain",
                    'random_domains': "Domain appears randomly generated"
                }
                
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.URL_VALIDATION,
                        severity=severity_map.get(pattern_name, 50),
                        description=description_map.get(pattern_name, f"Suspicious pattern: {pattern_name}"),
                        confidence=0.8
                    )
                )

    def _check_domain_legitimacy(self, parsed_url, risk_factors: List[RiskFactor]) -> None:
        """Check domain legitimacy and characteristics."""
        domain = parsed_url.netloc.lower()
        
        # Remove port if present
        if ':' in domain:
            domain = domain.split(':')[0]
        
        # Check against known suspicious domains
        for category, domains in self.suspicious_domains.items():
            if domain in domains:
                severity_map = {
                    'typosquatting': 85,
                    'generic_suspicious': 90
                }
                
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.URL_VALIDATION,
                        severity=severity_map.get(category, 70),
                        description=f"Domain is known to be suspicious ({category})",
                        confidence=0.9
                    )
                )
                return
        
        # Check domain length and structure
        domain_parts = domain.split('.')
        
        # Very short domain names (excluding TLD)
        if len(domain_parts) >= 2 and len(domain_parts[0]) < 3:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.URL_VALIDATION,
                    severity=40,
                    description="Domain name is unusually short",
                    confidence=0.6
                )
            )
        
        # Very long domain names
        if len(domain_parts) >= 2 and len(domain_parts[0]) > 20:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.URL_VALIDATION,
                    severity=45,
                    description="Domain name is unusually long",
                    confidence=0.6
                )
            )
        
        # Check for numbers-only domain
        if len(domain_parts) >= 2 and domain_parts[0].isdigit():
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.URL_VALIDATION,
                    severity=60,
                    description="Domain name consists only of numbers",
                    confidence=0.7
                )
            )
        
        # Check for excessive hyphens or underscores
        if domain_parts[0].count('-') > 3 or domain_parts[0].count('_') > 1:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.URL_VALIDATION,
                    severity=35,
                    description="Domain contains excessive hyphens or underscores",
                    confidence=0.6
                )
            )

    def _check_suspicious_domain_characteristics(self, parsed_url, risk_factors: List[RiskFactor]) -> None:
        """Check domain for explicitly suspicious characteristics only."""
        domain = parsed_url.netloc.lower()
        
        # Remove port if present
        if ':' in domain:
            domain = domain.split(':')[0]
        
        # Check against known suspicious domains
        for category, domains in self.suspicious_domains.items():
            if domain in domains:
                severity_map = {
                    'typosquatting': 85,
                    'generic_suspicious': 90
                }
                
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.URL_VALIDATION,
                        severity=severity_map.get(category, 70),
                        description=f"Domain is known to be suspicious ({category})",
                        confidence=0.9
                    )
                )
                return
        
        domain_parts = domain.split('.')
        
        # Only flag clearly suspicious characteristics
        # Check for numbers-only domain (highly suspicious)
        if len(domain_parts) >= 2 and domain_parts[0].isdigit():
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.URL_VALIDATION,
                    severity=70,
                    description="Domain name consists only of numbers",
                    confidence=0.8
                )
            )
        
        # Check for excessive hyphens (potential typosquatting)
        if domain_parts[0].count('-') > 4:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.URL_VALIDATION,
                    severity=50,
                    description="Domain contains excessive hyphens",
                    confidence=0.7
                )
            )
        
        # Check for very suspicious TLD combinations with random domains
        suspicious_tld_pattern = re.compile(r'[a-z0-9]{8,}\.(tk|ml|ga|cf)$')
        if suspicious_tld_pattern.match(domain):
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.URL_VALIDATION,
                    severity=65,
                    description="Random domain with suspicious TLD",
                    confidence=0.8
                )
            )

    def _check_url_shorteners(self, url: str, risk_factors: List[RiskFactor]) -> None:
        """Check for URL shorteners which can hide the real destination."""
        # This is already covered in suspicious patterns, but we can add more specific checks
        shortener_services = [
            'bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'short.link',
            'ow.ly', 'is.gd', 'buff.ly', 'rebrand.ly', 'cutt.ly'
        ]
        
        url_lower = url.lower()
        for service in shortener_services:
            if service in url_lower:
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.URL_VALIDATION,
                        severity=70,
                        description=f"Uses URL shortening service ({service})",
                        confidence=0.8
                    )
                )
                break

    def _check_protocol_security(self, parsed_url, risk_factors: List[RiskFactor]) -> None:
        """Check for protocol security issues - removed to make URL neutral."""
        # HTTP vs HTTPS is no longer considered a risk factor
        # Many legitimate companies still use HTTP for non-sensitive pages
        pass

    def _check_suspicious_ports(self, parsed_url, risk_factors: List[RiskFactor]) -> None:
        """Check for suspicious port numbers."""
        if parsed_url.port and parsed_url.port in self.suspicious_ports:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.URL_VALIDATION,
                    severity=45,
                    description=f"Uses potentially suspicious port number: {parsed_url.port}",
                    confidence=0.6
                )
            )

    def _check_legitimate_indicators(self, url: str, parsed_url, risk_factors: List[RiskFactor]) -> None:
        """Check for legitimate business indicators - removed to make URL neutral."""
        # No longer penalizing lack of business indicators
        # Absence of positive signals doesn't indicate risk
        pass

    def _calculate_confidence(self, url: str, format_valid: bool, risk_factor_count: int) -> float:
        """Calculate confidence score based on URL analysis completeness."""
        base_confidence = 0.8
        
        # Lower confidence if format is invalid (less analysis possible)
        if not format_valid:
            base_confidence = 0.9  # High confidence in format validation
        else:
            # Increase confidence with more thorough analysis
            try:
                parsed = urlparse(url)
                if parsed.netloc and parsed.scheme:
                    base_confidence += 0.1
            except Exception:
                pass
            
            # Increase confidence with more risk factors found (more analysis done)
            if risk_factor_count > 0:
                base_confidence += min(0.1, risk_factor_count * 0.02)
        
        return min(1.0, base_confidence)