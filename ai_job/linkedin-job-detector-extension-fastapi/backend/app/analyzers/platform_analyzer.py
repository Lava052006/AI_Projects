"""Platform analyzer for source credibility assessment and platform-specific risk adjustments."""

import re
from typing import List, Dict, Set
from app.models.internal import AnalysisResult, RiskFactor, RiskCategory


class PlatformAnalyzer:
    """Analyzes platform sources for credibility and applies platform-specific risk adjustments."""
    
    def __init__(self):
        """Initialize the platform analyzer with credibility scoring and risk adjustment data."""
        # Platform credibility tiers (higher score = more credible)
        self.platform_credibility = {
            # Tier 1: Highly credible platforms (90-100)
            'tier_1_high_credibility': {
                'linkedin.com': 95,
                'indeed.com': 90,
                'glassdoor.com': 92,
                'monster.com': 88,
                'careerbuilder.com': 87,
                'ziprecruiter.com': 85,
                'dice.com': 90,  # Tech-focused
                'stackoverflow.com': 93,  # Developer jobs
                'github.com': 92,  # Developer jobs
                'angel.co': 88,  # Startup jobs
                'wellfound.com': 88,  # Formerly AngelList
            },
            
            # Tier 2: Moderately credible platforms (70-89)
            'tier_2_moderate_credibility': {
                'craigslist.org': 70,
                'facebook.com': 75,
                'twitter.com': 72,
                'reddit.com': 73,
                'upwork.com': 78,
                'freelancer.com': 76,
                'fiverr.com': 74,
                'flexjobs.com': 82,
                'remote.co': 80,
                'weworkremotely.com': 81,
                'remoteok.io': 79,
                'joblist.com': 75,
                'xing.com': 77,  # European platform
                'seek.com': 78,  # Australian platform
                'chrome': 85,  # Browser extension (neutral)
                'firefox': 85,  # Browser extension (neutral)
                'safari': 85,  # Browser extension (neutral)
                'edge': 85,  # Browser extension (neutral)
            },
            
            # Tier 3: Lower credibility platforms (50-69)
            'tier_3_low_credibility': {
                'telegram.org': 55,
                'whatsapp.com': 50,
                'instagram.com': 60,
                'tiktok.com': 45,
                'snapchat.com': 40,
                'discord.com': 58,
                'slack.com': 65,
                'email': 60,  # Direct email contact
                'sms': 45,  # Text message
                'phone': 55,  # Phone call
            }
        }
        
        # Flatten platform credibility for easy lookup
        self.all_platforms = {}
        for tier, platforms in self.platform_credibility.items():
            self.all_platforms.update(platforms)
        
        # Platform-specific risk patterns
        self.platform_risk_patterns = {
            'social_media_risks': {
                'platforms': ['facebook.com', 'twitter.com', 'instagram.com', 'tiktok.com', 'snapchat.com'],
                'risk_multiplier': 1.3,
                'description': "Social media platforms have higher fraud risk"
            },
            'messaging_app_risks': {
                'platforms': ['telegram.org', 'whatsapp.com', 'discord.com'],
                'risk_multiplier': 1.5,
                'description': "Messaging apps are commonly used for scams"
            },
            'unverified_contact_risks': {
                'platforms': ['email', 'sms', 'phone'],
                'risk_multiplier': 1.2,
                'description': "Direct contact methods lack platform verification"
            },
            'freelance_platform_risks': {
                'platforms': ['upwork.com', 'freelancer.com', 'fiverr.com'],
                'risk_multiplier': 1.1,
                'description': "Freelance platforms may have less employer verification"
            }
        }
        
        # Suspicious platform indicators
        self.suspicious_indicators = {
            'unknown_platform': {
                'severity': 60,
                'description': "Platform is not recognized or well-known"
            },
            'high_risk_platform': {
                'severity': 80,
                'description': "Platform is known for high fraud rates"
            },
            'messaging_only': {
                'severity': 70,
                'description': "Contact only through messaging apps (red flag)"
            },
            'social_media_only': {
                'severity': 65,
                'description': "Job posting only on social media platforms"
            },
            'no_platform_verification': {
                'severity': 55,
                'description': "Platform lacks employer verification processes"
            }
        }
        
        # Platform normalization patterns
        self.platform_patterns = {
            'linkedin': re.compile(r'linkedin\.com|linkedin', re.IGNORECASE),
            'indeed': re.compile(r'indeed\.com|indeed', re.IGNORECASE),
            'glassdoor': re.compile(r'glassdoor\.com|glassdoor', re.IGNORECASE),
            'monster': re.compile(r'monster\.com|monster', re.IGNORECASE),
            'craigslist': re.compile(r'craigslist\.org|craigslist', re.IGNORECASE),
            'facebook': re.compile(r'facebook\.com|facebook|fb\.com', re.IGNORECASE),
            'twitter': re.compile(r'twitter\.com|twitter|x\.com', re.IGNORECASE),
            'telegram': re.compile(r'telegram\.org|telegram|t\.me', re.IGNORECASE),
            'whatsapp': re.compile(r'whatsapp\.com|whatsapp', re.IGNORECASE),
            'email': re.compile(r'^email$|^e-mail$|email contact|direct email', re.IGNORECASE),
            'sms': re.compile(r'^sms$|^text$|text message|phone text', re.IGNORECASE),
            'phone': re.compile(r'^phone$|phone call|telephone|direct call', re.IGNORECASE),
            'chrome': re.compile(r'^chrome$|chrome extension|browser extension', re.IGNORECASE),
            'firefox': re.compile(r'^firefox$|firefox extension', re.IGNORECASE),
            'safari': re.compile(r'^safari$|safari extension', re.IGNORECASE),
            'edge': re.compile(r'^edge$|edge extension', re.IGNORECASE),
        }

    def analyze(self, platform_source: str) -> AnalysisResult:
        """
        Analyze platform source for credibility and apply platform-specific risk adjustments.
        
        Args:
            platform_source: The platform or source where the job posting was found
            
        Returns:
            AnalysisResult containing identified risk factors and confidence score
        """
        if not platform_source or not platform_source.strip():
            return AnalysisResult(
                risk_factors=[
                    RiskFactor(
                        category=RiskCategory.PLATFORM_CREDIBILITY,
                        severity=100,
                        description="Platform source is empty or missing",
                        confidence=1.0
                    )
                ],
                confidence=1.0,
                analyzer_name="PlatformAnalyzer"
            )
        
        platform = platform_source.strip().lower()
        risk_factors = []
        
        # Normalize platform name
        normalized_platform = self._normalize_platform_name(platform)
        
        # Get platform credibility score
        credibility_score = self._get_platform_credibility(normalized_platform, risk_factors)
        
        # Check for platform-specific risk patterns
        self._check_platform_risk_patterns(normalized_platform, risk_factors)
        
        # Check for suspicious platform indicators
        self._check_suspicious_indicators(normalized_platform, platform, risk_factors)
        
        # Apply platform-specific risk adjustments
        self._apply_platform_risk_adjustments(normalized_platform, risk_factors)
        
        # Calculate confidence based on platform recognition and analysis depth
        confidence = self._calculate_confidence(normalized_platform, len(risk_factors))
        
        return AnalysisResult(
            risk_factors=risk_factors,
            confidence=confidence,
            analyzer_name="PlatformAnalyzer"
        )

    def _normalize_platform_name(self, platform: str) -> str:
        """Normalize platform name to standard format for consistent analysis."""
        # First check if the platform is already in our database as-is
        if platform in self.all_platforms:
            return platform
        
        # Extract domain if it looks like a URL
        if '.' in platform and ('http' in platform or 'www' in platform):
            # Simple domain extraction
            domain_match = re.search(r'(?:https?://)?(?:www\.)?([^/\s]+)', platform)
            if domain_match:
                extracted_domain = domain_match.group(1).lower()
                if extracted_domain in self.all_platforms:
                    return extracted_domain
        
        # Check against known patterns for common variations
        for standard_name, pattern in self.platform_patterns.items():
            if pattern.search(platform):
                # Map pattern names back to actual platform names in our database
                pattern_to_platform = {
                    'linkedin': 'linkedin.com',
                    'indeed': 'indeed.com',
                    'glassdoor': 'glassdoor.com',
                    'monster': 'monster.com',
                    'craigslist': 'craigslist.org',
                    'facebook': 'facebook.com',
                    'twitter': 'twitter.com',
                    'telegram': 'telegram.org',
                    'whatsapp': 'whatsapp.com',
                    'email': 'email',
                    'sms': 'sms',
                    'phone': 'phone',
                    'chrome': 'chrome',
                    'firefox': 'firefox',
                    'safari': 'safari',
                    'edge': 'edge',
                }
                return pattern_to_platform.get(standard_name, standard_name)
        
        return platform.lower()

    def _get_platform_credibility(self, normalized_platform: str, risk_factors: List[RiskFactor]) -> int:
        """Get credibility score for the platform and add risk factors if needed."""
        # Check if platform is in our credibility database
        credibility_score = self.all_platforms.get(normalized_platform)
        
        if credibility_score is None:
            # Unknown platform - moderate risk
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.PLATFORM_CREDIBILITY,
                    severity=self.suspicious_indicators['unknown_platform']['severity'],
                    description=self.suspicious_indicators['unknown_platform']['description'],
                    confidence=0.7
                )
            )
            return 50  # Default moderate credibility
        
        # Add risk factors based on credibility tier
        if credibility_score < 50:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.PLATFORM_CREDIBILITY,
                    severity=self.suspicious_indicators['high_risk_platform']['severity'],
                    description=self.suspicious_indicators['high_risk_platform']['description'],
                    confidence=0.9
                )
            )
        elif credibility_score < 70:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.PLATFORM_CREDIBILITY,
                    severity=50,
                    description="Platform has lower credibility rating",
                    confidence=0.8
                )
            )
        elif credibility_score < 85:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.PLATFORM_CREDIBILITY,
                    severity=25,
                    description="Platform has moderate credibility rating",
                    confidence=0.6
                )
            )
        # High credibility platforms (85+) don't add risk factors
        
        return credibility_score

    def _check_platform_risk_patterns(self, normalized_platform: str, risk_factors: List[RiskFactor]) -> None:
        """Check for platform-specific risk patterns."""
        for risk_type, risk_data in self.platform_risk_patterns.items():
            if normalized_platform in risk_data['platforms']:
                # Calculate severity based on risk multiplier
                base_severity = 40
                adjusted_severity = min(100, int(base_severity * risk_data['risk_multiplier']))
                
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.PLATFORM_CREDIBILITY,
                        severity=adjusted_severity,
                        description=risk_data['description'],
                        confidence=0.8
                    )
                )

    def _check_suspicious_indicators(self, normalized_platform: str, original_platform: str, risk_factors: List[RiskFactor]) -> None:
        """Check for suspicious platform indicators."""
        # Check for messaging-only contact
        messaging_platforms = ['telegram', 'whatsapp', 'discord', 'sms']
        if normalized_platform in messaging_platforms:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.PLATFORM_CREDIBILITY,
                    severity=self.suspicious_indicators['messaging_only']['severity'],
                    description=self.suspicious_indicators['messaging_only']['description'],
                    confidence=0.8
                )
            )
        
        # Check for social media only
        social_platforms = ['facebook', 'twitter', 'instagram', 'tiktok', 'snapchat']
        if normalized_platform in social_platforms:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.PLATFORM_CREDIBILITY,
                    severity=self.suspicious_indicators['social_media_only']['severity'],
                    description=self.suspicious_indicators['social_media_only']['description'],
                    confidence=0.7
                )
            )
        
        # Check for platforms with no verification
        unverified_platforms = ['email', 'sms', 'phone', 'craigslist']
        if normalized_platform in unverified_platforms:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.PLATFORM_CREDIBILITY,
                    severity=self.suspicious_indicators['no_platform_verification']['severity'],
                    description=self.suspicious_indicators['no_platform_verification']['description'],
                    confidence=0.6
                )
            )
        
        # Check for very vague platform descriptions
        vague_patterns = ['website', 'online', 'internet', 'web', 'site']
        if any(pattern in original_platform.lower() for pattern in vague_patterns) and len(original_platform.split()) <= 2:
            risk_factors.append(
                RiskFactor(
                    category=RiskCategory.PLATFORM_CREDIBILITY,
                    severity=45,
                    description="Platform description is vague or non-specific",
                    confidence=0.6
                )
            )

    def _apply_platform_risk_adjustments(self, normalized_platform: str, risk_factors: List[RiskFactor]) -> None:
        """Apply platform-specific risk adjustments to existing risk factors."""
        # This method could be used to modify the severity of risk factors
        # based on platform-specific characteristics, but for now we'll
        # keep it simple and just ensure we've captured the main risks
        
        # Example: If platform is known for specific types of fraud,
        # we could increase severity of related risk factors
        
        # High-risk platforms get additional general warning
        high_risk_platforms = ['telegram', 'whatsapp', 'tiktok', 'snapchat']
        if normalized_platform in high_risk_platforms:
            # Check if we already have a high-risk warning
            has_high_risk_warning = any(
                factor.severity >= 70 and 'high fraud' in factor.description.lower()
                for factor in risk_factors
            )
            
            if not has_high_risk_warning:
                risk_factors.append(
                    RiskFactor(
                        category=RiskCategory.PLATFORM_CREDIBILITY,
                        severity=75,
                        description="Platform is associated with higher fraud rates",
                        confidence=0.8
                    )
                )

    def get_platform_risk_multiplier(self, platform_source: str) -> float:
        """
        Get risk multiplier for the platform (used by other analyzers).
        
        Args:
            platform_source: The platform source to analyze
            
        Returns:
            Risk multiplier (1.0 = no adjustment, >1.0 = higher risk, <1.0 = lower risk)
        """
        if not platform_source:
            return 1.0
        
        normalized_platform = self._normalize_platform_name(platform_source.strip().lower())
        
        # Check platform-specific risk patterns
        for risk_data in self.platform_risk_patterns.values():
            if normalized_platform in risk_data['platforms']:
                return risk_data['risk_multiplier']
        
        # Check credibility score
        credibility_score = self.all_platforms.get(normalized_platform, 50)
        
        if credibility_score >= 90:
            return 0.8  # Reduce risk for highly credible platforms
        elif credibility_score >= 80:
            return 0.9  # Slightly reduce risk
        elif credibility_score < 50:
            return 1.4  # Increase risk for low credibility platforms
        elif credibility_score < 70:
            return 1.2  # Moderately increase risk
        
        return 1.0  # No adjustment for moderate credibility

    def _calculate_confidence(self, normalized_platform: str, risk_factor_count: int) -> float:
        """Calculate confidence score based on platform analysis completeness."""
        base_confidence = 0.8
        
        # Increase confidence if platform is recognized
        if normalized_platform in self.all_platforms:
            base_confidence += 0.1
        
        # Increase confidence with more risk factors found (more analysis done)
        if risk_factor_count > 0:
            base_confidence += min(0.1, risk_factor_count * 0.02)
        
        # Increase confidence if we have specific patterns for this platform
        if any(pattern.search(normalized_platform) for pattern in self.platform_patterns.values()):
            base_confidence += 0.05
        
        return min(1.0, base_confidence)