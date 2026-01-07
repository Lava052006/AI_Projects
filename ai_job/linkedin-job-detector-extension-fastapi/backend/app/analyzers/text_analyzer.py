"""Text analyzer for job description fraud detection."""

import re
from typing import List, Set
from app.models.internal import AnalysisResult, RiskFactor, RiskCategory


class TextAnalyzer:
    """Analyzes job text content for fraud indicators and suspicious patterns."""
    
    def __init__(self):
        """Initialize the text analyzer with fraud detection patterns."""
        # Enhanced fraud indicators with explicit scam signals
        self.fraud_keywords = {
            'personal_info_requests': [
                'ssn', 'social security', 'bank account', 'routing number',
                'credit card', 'personal information', 'id copy', 'passport copy',
                'driver license', 'birth certificate', 'tax information'
            ],
            'financial_requests': [
                'processing fee', 'training fee', 'equipment fee', 'startup cost',
                'registration fee', 'background check fee', 'send money',
                'wire transfer', 'western union', 'moneygram', 'cash advance',
                'money transfer', 'transfer funds', 'transfer money'
            ],
            'urgency_pressure': [
                'immediate start', 'urgent hiring', 'start immediately', 'asap',
                'quick hire', 'fast hiring', 'limited time', 'act now',
                'don\'t wait', 'hurry', 'expires soon', 'today only'
            ],
            'unrealistic_promises': [
                'no experience required', 'guaranteed income', 'easy money',
                'work from home guaranteed', 'make money fast', 'get rich quick',
                'high pay no experience', 'earn thousands weekly', 'instant success'
            ],
            'vague_descriptions': [
                'various duties', 'other duties as assigned', 'miscellaneous tasks',
                'general office work', 'data entry', 'customer service representative',
                'administrative assistant', 'personal assistant'
            ],
            'communication_red_flags': [
                'whatsapp', 'telegram', 'text message', 'sms only',
                'contact via text', 'message me', 'call this number',
                'email me directly', 'respond asap'
            ]
        }
        
        # Enhanced suspicious patterns (regex)
        self.suspicious_patterns = {
            'excessive_caps': re.compile(r'[A-Z]{5,}'),  # 5+ consecutive caps
            'excessive_exclamation': re.compile(r'!{2,}'),  # Multiple exclamation marks
            'phone_in_description': re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),  # Phone numbers
            'email_in_description': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'money_amounts': re.compile(r'\$\d+(?:,\d{3})*(?:\.\d{2})?'),  # Dollar amounts
            'unrealistic_salary': re.compile(r'\$(?:[5-9]\d{3,}|\d{5,})(?:/week|/day|weekly|daily)', re.IGNORECASE),
            'poor_grammar': re.compile(r'\b(?:there|their|they\'re)\b.*\b(?:there|their|they\'re)\b', re.IGNORECASE),
            'multiple_currencies': re.compile(r'[\$£€¥₹]', re.IGNORECASE),
            'instant_keywords': re.compile(r'\b(?:instant|immediate|now|today|asap)\b', re.IGNORECASE)
        }
        
        # Legitimate job indicators (positive signals)
        self.legitimate_indicators = {
            'specific_skills': [
                'python', 'java', 'javascript', 'sql', 'aws', 'docker',
                'kubernetes', 'react', 'angular', 'node.js', 'git',
                'agile', 'scrum', 'ci/cd', 'devops'
            ],
            'professional_terms': [
                'bachelor\'s degree', 'master\'s degree', 'certification',
                'experience required', 'qualifications', 'responsibilities',
                'requirements', 'preferred qualifications'
            ],
            'company_benefits': [
                'health insurance', '401k', 'dental', 'vision', 'pto',
                'paid time off', 'retirement plan', 'stock options'
            ]
        }

    def analyze(self, job_text: str) -> AnalysisResult:
        """
        Analyze job text for fraud indicators and suspicious patterns.
        
        Args:
            job_text: The job description text to analyze
            
        Returns:
            AnalysisResult containing identified risk factors and confidence score
        """
        if not job_text or not job_text.strip():
            return AnalysisResult(
                risk_factors=[
                    RiskFactor(
                        category=RiskCategory.TEXT_ANALYSIS,
                        severity=100,
                        description="Job text is empty or missing",
                        confidence=1.0
                    )
                ],
                confidence=1.0,
                analyzer_name="TextAnalyzer"
            )
        
        job_text_lower = job_text.lower()
        risk_factors = []
        
        # Check for fraud keywords
        fraud_score = self._check_fraud_keywords(job_text_lower, risk_factors)
        
        # Check for suspicious patterns
        pattern_score = self._check_suspicious_patterns(job_text, risk_factors)
        
        # Check for vague or minimal content
        content_score = self._check_content_quality(job_text, risk_factors)
        
        # Check for legitimate indicators (reduces risk)
        legitimacy_bonus = self._check_legitimate_indicators(job_text_lower)
        
        # Calculate overall confidence based on text length and analysis depth
        confidence = self._calculate_confidence(job_text, len(risk_factors))
        
        return AnalysisResult(
            risk_factors=risk_factors,
            confidence=confidence,
            analyzer_name="TextAnalyzer"
        )

    def _check_fraud_keywords(self, job_text_lower: str, risk_factors: List[RiskFactor]) -> int:
        """Check for common fraud keywords in job text with enhanced severity for explicit scams."""
        total_matches = 0
        
        # Severity mapping for different fraud categories
        severity_mapping = {
            'personal_info_requests': 100,  # Maximum risk - increased
            'financial_requests': 98,      # Maximum risk - increased
            'urgency_pressure': 65,        # Medium-high risk
            'unrealistic_promises': 75,    # High risk
            'vague_descriptions': 30,      # Lower risk
            'communication_red_flags': 55  # Medium risk
        }
        
        for category, keywords in self.fraud_keywords.items():
            matches = []
            for keyword in keywords:
                if keyword in job_text_lower:
                    matches.append(keyword)
                    total_matches += 1
            
            if matches:
                base_severity = severity_mapping.get(category, 50)
                # Increase severity for multiple matches in same category
                severity = min(100, base_severity + (len(matches) - 1) * 5)
                
                confidence = 0.9 if category in ['personal_info_requests', 'financial_requests'] else 0.8
                
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.TEXT_ANALYSIS,
                        severity=severity,
                        description=f"Contains {category.replace('_', ' ')} keywords: {', '.join(matches[:3])}",
                        confidence=confidence
                    )
                )
        
        return total_matches

    def _check_suspicious_patterns(self, job_text: str, risk_factors: List[RiskFactor]) -> int:
        """Check for suspicious patterns using regex with enhanced detection."""
        pattern_count = 0
        
        # Enhanced severity mapping
        # Enhanced severity mapping
        severity_mapping = {
            'excessive_caps': 15,
            'excessive_exclamation': 20,
            'phone_in_description': 40,
            'email_in_description': 35,
            'money_amounts': 15,  # Reduced - salary ranges are normal
            'unrealistic_salary': 90,  # Very high risk - increased
            'poor_grammar': 20,
            'multiple_currencies': 30,  # Reduced - salary ranges often use $
            'instant_keywords': 45
        }
        
        for pattern_name, pattern in self.suspicious_patterns.items():
            matches = pattern.findall(job_text)
            if matches:
                pattern_count += len(matches)
                base_severity = severity_mapping.get(pattern_name, 30)
                severity = min(100, base_severity + (len(matches) - 1) * 10)
                
                description_map = {
                    'excessive_caps': f"Excessive use of capital letters ({len(matches)} instances)",
                    'excessive_exclamation': f"Multiple exclamation marks ({len(matches)} instances)",
                    'phone_in_description': f"Phone numbers in job description ({len(matches)} found)",
                    'email_in_description': f"Email addresses in job description ({len(matches)} found)",
                    'money_amounts': f"Specific dollar amounts mentioned ({len(matches)} instances)",
                    'unrealistic_salary': f"Unrealistic salary promises detected ({len(matches)} instances)",
                    'poor_grammar': f"Potential grammar issues detected ({len(matches)} instances)",
                    'multiple_currencies': f"Multiple currency symbols used ({len(matches)} instances)",
                    'instant_keywords': f"Urgency/instant keywords detected ({len(matches)} instances)"
                }
                
                confidence = 0.9 if pattern_name == 'unrealistic_salary' else 0.7
                
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.TEXT_ANALYSIS,
                        severity=severity,
                        description=description_map.get(pattern_name, f"Suspicious pattern: {pattern_name}"),
                        confidence=confidence
                    )
                )
        
        return pattern_count

    def _check_content_quality(self, job_text: str, risk_factors: List[RiskFactor]) -> int:
        """Check for vague or low-quality content."""
        words = job_text.split()
        sentences = job_text.split('.')
        
        quality_issues = 0
        
        # Check for very short descriptions
        if len(words) < 20:
            quality_issues += 1
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.TEXT_ANALYSIS,
                    severity=70,
                    description=f"Very short job description ({len(words)} words)",
                    confidence=0.9
                )
            )
        
        # Check for very long descriptions (might be copy-paste spam)
        elif len(words) > 1000:
            quality_issues += 1
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.TEXT_ANALYSIS,
                    severity=40,
                    description=f"Unusually long job description ({len(words)} words)",
                    confidence=0.6
                )
            )
        
        # Check for lack of specific requirements
        requirement_keywords = ['experience', 'skill', 'requirement', 'qualification', 'must have', 'should have']
        has_requirements = any(keyword in job_text.lower() for keyword in requirement_keywords)
        
        if not has_requirements:
            quality_issues += 1
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.TEXT_ANALYSIS,
                    severity=50,
                    description="No specific requirements or qualifications mentioned",
                    confidence=0.7
                )
            )
        
        return quality_issues

    def _check_legitimate_indicators(self, job_text_lower: str) -> int:
        """Check for legitimate job posting indicators."""
        legitimacy_score = 0
        
        for category, indicators in self.legitimate_indicators.items():
            for indicator in indicators:
                if indicator in job_text_lower:
                    legitimacy_score += 1
        
        return legitimacy_score

    def _calculate_confidence(self, job_text: str, risk_factor_count: int) -> float:
        """Calculate confidence score based on text analysis depth."""
        base_confidence = 0.7
        
        # Increase confidence with more text to analyze
        word_count = len(job_text.split())
        if word_count > 50:
            base_confidence += 0.1
        if word_count > 100:
            base_confidence += 0.1
        
        # Increase confidence with more risk factors found (more analysis done)
        if risk_factor_count > 0:
            base_confidence += min(0.2, risk_factor_count * 0.05)
        
        return min(1.0, base_confidence)