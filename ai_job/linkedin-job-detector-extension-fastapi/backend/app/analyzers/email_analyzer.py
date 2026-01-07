"""Email analyzer for recruiter email validation and domain reputation assessment."""

import re
from typing import List, Set
from app.models.internal import AnalysisResult, RiskFactor, RiskCategory


class EmailAnalyzer:
    """Analyzes recruiter email addresses for format validation and domain reputation."""
    
    def __init__(self):
        """Initialize the email analyzer with validation patterns and domain lists."""
        # Email format validation regex (RFC 5322 compliant)
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        
        # Suspicious email patterns
        self.suspicious_patterns = {
            'temp_email': re.compile(r'@(?:10minutemail|tempmail|guerrillamail|mailinator|throwaway)', re.IGNORECASE),
            'random_chars': re.compile(r'^[a-zA-Z0-9]{20,}@'),  # Very long random-looking usernames
            'numbers_only': re.compile(r'^[0-9]+@'),  # Username is only numbers
            'suspicious_tlds': re.compile(r'\.(?:tk|ml|ga|cf|click|download|zip)$', re.IGNORECASE)
        }
        
        # Trusted domain categories
        self.trusted_domains = {
            'major_providers': {
                'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
                'aol.com', 'icloud.com', 'protonmail.com', 'zoho.com'
            },
            'business_providers': {
                'company.com', 'corp.com', 'inc.com', 'ltd.com',
                'enterprise.com', 'business.com', 'office.com'
            },
            'professional_domains': {
                # Common professional email patterns will be detected by heuristics
            }
        }
        
        # Known temporary/disposable email domains
        self.disposable_domains = {
            '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
            'mailinator.com', 'throwaway.email', 'temp-mail.org',
            'fakeinbox.com', 'dispostable.com', 'yopmail.com'
        }
        
        # Suspicious domain patterns
        self.suspicious_domain_patterns = {
            'very_new_tlds': ['.tk', '.ml', '.ga', '.cf', '.click', '.download', '.zip'],
            'typosquatting': ['gmai1.com', 'yaho0.com', 'hotmai1.com', 'outlok.com'],
            'random_domains': re.compile(r'^[a-z0-9]{15,}\.(?:com|net|org)$')  # Very long random domain names (15+ chars)
        }

    def analyze(self, recruiter_email: str) -> AnalysisResult:
        """
        Analyze recruiter email for format validation and domain reputation.
        Only adds risk if email exists AND is explicitly suspicious.
        
        Args:
            recruiter_email: The recruiter's email address to analyze
            
        Returns:
            AnalysisResult containing identified risk factors and confidence score
        """
        if not recruiter_email or not recruiter_email.strip():
            # Empty email is neutral - no risk added
            return AnalysisResult(
                risk_factors=[],
                confidence=1.0,
                analyzer_name="EmailAnalyzer"
            )
        
        email = recruiter_email.strip().lower()
        risk_factors = []
        
        # Basic format validation
        format_valid = self._validate_email_format(email, risk_factors)
        
        if format_valid:
            # Extract domain for further analysis
            domain = email.split('@')[1]
            
            # Only check for explicitly suspicious patterns
            self._check_suspicious_patterns(email, risk_factors)
            
            # Check domain reputation for suspicious indicators
            self._check_domain_reputation(domain, risk_factors)
            
            # Check for disposable email services
            self._check_disposable_email(domain, risk_factors)
            
            # Check for suspicious email characteristics combined with scam indicators
            self._check_suspicious_email_characteristics(email, domain, risk_factors)
        
        # Calculate confidence based on analysis completeness
        confidence = self._calculate_confidence(email, format_valid, len(risk_factors))
        
        return AnalysisResult(
            risk_factors=risk_factors,
            confidence=confidence,
            analyzer_name="EmailAnalyzer"
        )

    def _validate_email_format(self, email: str, risk_factors: List[RiskFactor]) -> bool:
        """Validate basic email format using regex."""
        if not self.email_pattern.match(email):
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.EMAIL_VALIDATION,
                    severity=90,
                    description="Invalid email format",
                    confidence=1.0
                )
            )
            return False
        
        # Additional format checks
        if email.count('@') != 1:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.EMAIL_VALIDATION,
                    severity=95,
                    description="Email contains multiple @ symbols",
                    confidence=1.0
                )
            )
            return False
        
        username, domain = email.split('@')
        
        # Check username length
        if len(username) < 1:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.EMAIL_VALIDATION,
                    severity=100,
                    description="Email username is empty",
                    confidence=1.0
                )
            )
            return False
        
        if len(username) > 64:  # RFC 5321 limit
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.EMAIL_VALIDATION,
                    severity=60,
                    description="Email username exceeds recommended length",
                    confidence=0.8
                )
            )
        
        # Check domain length
        if len(domain) > 253:  # RFC 5321 limit
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.EMAIL_VALIDATION,
                    severity=70,
                    description="Email domain exceeds maximum length",
                    confidence=0.9
                )
            )
        
        return True

    def _check_suspicious_patterns(self, email: str, risk_factors: List[RiskFactor]) -> None:
        """Check for suspicious patterns in the email address."""
        for pattern_name, pattern in self.suspicious_patterns.items():
            if pattern.search(email):
                severity_map = {
                    'temp_email': 85,
                    'random_chars': 60,
                    'numbers_only': 40,
                    'suspicious_tlds': 70
                }
                
                description_map = {
                    'temp_email': "Uses temporary/disposable email service",
                    'random_chars': "Username appears to be randomly generated",
                    'numbers_only': "Username contains only numbers",
                    'suspicious_tlds': "Uses suspicious top-level domain"
                }
                
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.EMAIL_VALIDATION,
                        severity=severity_map.get(pattern_name, 50),
                        description=description_map.get(pattern_name, f"Suspicious pattern: {pattern_name}"),
                        confidence=0.8
                    )
                )

    def _check_domain_reputation(self, domain: str, risk_factors: List[RiskFactor]) -> None:
        """Check domain reputation and characteristics."""
        # Check against known suspicious domains
        if domain in self.disposable_domains:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.EMAIL_VALIDATION,
                    severity=80,
                    description="Uses known disposable email domain",
                    confidence=0.9
                )
            )
            return
        
        # Check for typosquatting attempts
        if domain in self.suspicious_domain_patterns['typosquatting']:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.EMAIL_VALIDATION,
                    severity=75,
                    description="Domain appears to be typosquatting a legitimate service",
                    confidence=0.8
                )
            )
        
        # Check for suspicious TLDs
        for suspicious_tld in self.suspicious_domain_patterns['very_new_tlds']:
            if domain.endswith(suspicious_tld):
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.EMAIL_VALIDATION,
                        severity=50,
                        description=f"Uses potentially suspicious TLD: {suspicious_tld}",
                        confidence=0.6
                    )
                )
                break
        
        # Check for random-looking domains
        if self.suspicious_domain_patterns['random_domains'].match(domain):
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.EMAIL_VALIDATION,
                    severity=55,
                    description="Domain name appears randomly generated",
                    confidence=0.7
                )
            )

    def _check_disposable_email(self, domain: str, risk_factors: List[RiskFactor]) -> None:
        """Check if the email uses a disposable email service."""
        # This is already covered in domain reputation, but we can add more specific checks
        disposable_keywords = ['temp', 'throw', 'disposable', 'fake', '10min', 'guerrilla']
        
        for keyword in disposable_keywords:
            if keyword in domain:
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.EMAIL_VALIDATION,
                        severity=70,
                        description=f"Domain contains disposable email indicator: '{keyword}'",
                        confidence=0.7
                    )
                )
                break

    def _check_email_professionalism(self, email: str, domain: str, risk_factors: List[RiskFactor]) -> None:
        """Check indicators of professional vs personal email usage."""
        username = email.split('@')[0]
        
        # Check if using major personal email providers for recruiting
        if domain in self.trusted_domains['major_providers']:
            # Personal email providers are not necessarily bad, but less professional
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.EMAIL_VALIDATION,
                    severity=20,
                    description="Uses personal email provider instead of company domain",
                    confidence=0.5
                )
            )
        
        # Check for unprofessional username patterns
        unprofessional_patterns = [
            r'\d{4,}',  # Many consecutive numbers
            r'[xX]{2,}',  # Multiple x's
            r'(cool|hot|sexy|fun|party)',  # Unprofessional words
            r'[._-]{3,}'  # Excessive punctuation
        ]
        
        for pattern in unprofessional_patterns:
            if re.search(pattern, username):
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.EMAIL_VALIDATION,
                        severity=30,
                        description="Username contains unprofessional elements",
                        confidence=0.6
                    )
                )
                break
        
        # Check for very short domains (might be suspicious)
        if len(domain.split('.')[0]) < 3:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.EMAIL_VALIDATION,
                    severity=40,
                    description="Domain name is unusually short",
                    confidence=0.6
                )
            )

    def _check_suspicious_email_characteristics(self, email: str, domain: str, risk_factors: List[RiskFactor]) -> None:
        """Check for suspicious email characteristics only when combined with scam indicators."""
        username = email.split('@')[0]
        
        # Only flag personal email providers if combined with suspicious keywords
        if domain in self.trusted_domains['major_providers']:
            # Look for finance/urgent keywords that might indicate scams
            suspicious_keywords = ['money', 'cash', 'urgent', 'immediate', 'quick', 'easy', 'guaranteed']
            if any(keyword in username.lower() for keyword in suspicious_keywords):
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.EMAIL_VALIDATION,
                        severity=60,
                        description="Personal email with finance/urgency keywords",
                        confidence=0.7
                    )
                )
        
        # Check for unprofessional username patterns only if severe
        highly_unprofessional_patterns = [
            r'(money|cash|rich|wealth|profit)',  # Finance-related usernames
            r'(urgent|asap|quick|fast|easy)',    # Urgency-related usernames
            r'[xX]{3,}',  # Multiple x's (xxx)
            r'\d{6,}'     # Very long number sequences
        ]
        
        for pattern in highly_unprofessional_patterns:
            if re.search(pattern, username):
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.EMAIL_VALIDATION,
                        severity=50,
                        description="Email username contains suspicious keywords",
                        confidence=0.7
                    )
                )
                break

    def _calculate_confidence(self, email: str, format_valid: bool, risk_factor_count: int) -> float:
        """Calculate confidence score based on email analysis completeness."""
        base_confidence = 0.8
        
        # Lower confidence if format is invalid (less analysis possible)
        if not format_valid:
            base_confidence = 0.9  # High confidence in format validation
        else:
            # Increase confidence with more thorough analysis
            if '@' in email and len(email.split('@')[1]) > 0:
                base_confidence += 0.1
            
            # Increase confidence with more risk factors found (more analysis done)
            if risk_factor_count > 0:
                base_confidence += min(0.1, risk_factor_count * 0.02)
        
        return min(1.0, base_confidence)