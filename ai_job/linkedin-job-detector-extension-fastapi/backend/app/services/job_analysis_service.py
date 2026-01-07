"""Job Analysis Service - Coordinates all analyzers and generates final risk assessment."""

from typing import List, Dict, Tuple
from app.models.request import JobAnalysisRequest
from app.models.response import JobAnalysisResponse, VerdictEnum, ConfidenceEnum
from app.models.internal import AnalysisResult, RiskFactor, RiskCategory
from app.analyzers import TextAnalyzer, EmailAnalyzer, URLAnalyzer, PlatformAnalyzer


class JobAnalysisService:
    """
    Core business logic coordinator that orchestrates all analyzers,
    calculates risk scores, and generates final verdicts and explanations.
    """
    
    def __init__(self):
        """Initialize the service with all analyzer components."""
        self.text_analyzer = TextAnalyzer()
        self.email_analyzer = EmailAnalyzer()
        self.url_analyzer = URLAnalyzer()
        self.platform_analyzer = PlatformAnalyzer()
        
        # Risk score calculation weights for different categories
        # Text analysis dominates (70%), metadata limited to 30%
        self.category_weights = {
            RiskCategory.TEXT_ANALYSIS: 0.70,      # 70% - Job description dominates
            RiskCategory.EMAIL_VALIDATION: 0.12,   # 12% - Email credibility
            RiskCategory.URL_VALIDATION: 0.10,     # 10% - Company URL legitimacy
            RiskCategory.PLATFORM_CREDIBILITY: 0.08 # 8% - Platform context
        }
        
        # Verdict thresholds
        self.verdict_thresholds = {
            'safe': 30,        # 0-30: Safe
            'caution': 65,     # 31-65: Caution  
            'high_risk': 100   # 66-100: High Risk
        }

    def analyze_job_posting(self, request: JobAnalysisRequest) -> JobAnalysisResponse:
        """
        Analyze a job posting and return comprehensive risk assessment.
        
        Args:
            request: JobAnalysisRequest containing job posting data
            
        Returns:
            JobAnalysisResponse with risk score, flags, explanation, verdict, and confidence
        """
        # Run all analyzers
        analysis_results = self._run_all_analyzers(request)
        
        # Calculate overall risk score and confidence
        risk_score, confidence_level = self._calculate_overall_risk_score_with_confidence(analysis_results, request)
        
        # Determine verdict based on risk score
        verdict = self._determine_verdict(risk_score)
        
        # Generate flags from all risk factors
        flags = self._generate_flags(analysis_results)
        
        # Generate human-readable explanation
        explanation = self._generate_explanation(analysis_results, risk_score, verdict, confidence_level)
        
        return JobAnalysisResponse(
            risk_score=risk_score,
            flags=flags,
            explanation=explanation,
            verdict=verdict,
            confidence=ConfidenceEnum(confidence_level)
        )

    def _run_all_analyzers(self, request: JobAnalysisRequest) -> Dict[str, AnalysisResult]:
        """
        Run all analyzer components on the job posting data.
        
        Args:
            request: JobAnalysisRequest containing job posting data
            
        Returns:
            Dictionary mapping analyzer names to their results
        """
        results = {}
        
        # Run text analysis
        results['text'] = self.text_analyzer.analyze(request.job_text)
        
        # Run email analysis
        results['email'] = self.email_analyzer.analyze(request.recruiter_email)
        
        # Run URL analysis
        results['url'] = self.url_analyzer.analyze(request.company_url)
        
        # Run platform analysis
        results['platform'] = self.platform_analyzer.analyze(request.platform_source)
        
        return results

    def _calculate_overall_risk_score_with_confidence(self, analysis_results: Dict[str, AnalysisResult], request: JobAnalysisRequest) -> Tuple[int, str]:
        """
        Calculate overall risk score and confidence level.
        
        Args:
            analysis_results: Dictionary of analysis results from all analyzers
            request: Original request to check for missing metadata
            
        Returns:
            Tuple of (risk_score, confidence_level)
        """
        category_scores = {}
        category_confidences = {}
        
        # Collect risk factors by category
        all_risk_factors = []
        for result in analysis_results.values():
            all_risk_factors.extend(result.risk_factors)
        
        # Group risk factors by category and calculate category scores
        for category in RiskCategory:
            category_factors = [f for f in all_risk_factors if f.category == category]
            
            if category_factors:
                # For categories with multiple high-severity factors, use a more aggressive calculation
                if category == RiskCategory.TEXT_ANALYSIS and len(category_factors) > 5:
                    # Use the top 3 highest severity factors for text analysis
                    sorted_factors = sorted(category_factors, key=lambda f: f.severity * f.confidence, reverse=True)
                    top_factors = sorted_factors[:3]
                    
                    # Calculate score using the maximum of the top factors, not average
                    max_weighted_severity = max(
                        factor.severity * factor.confidence 
                        for factor in top_factors
                    )
                    category_scores[category] = max_weighted_severity
                    category_confidences[category] = max(factor.confidence for factor in top_factors)
                else:
                    # Calculate weighted severity for this category
                    total_weighted_severity = sum(
                        factor.severity * factor.confidence 
                        for factor in category_factors
                    )
                    total_confidence = sum(factor.confidence for factor in category_factors)
                    
                    if total_confidence > 0:
                        category_scores[category] = total_weighted_severity / total_confidence
                        category_confidences[category] = min(1.0, total_confidence / len(category_factors))
                    else:
                        category_scores[category] = 0
                        category_confidences[category] = 0
            else:
                category_scores[category] = 0
                category_confidences[category] = 0
        
        # Calculate weighted overall score
        weighted_score = 0
        total_weight = 0
        
        for category, weight in self.category_weights.items():
            if category in category_scores:
                # Adjust weight by confidence
                adjusted_weight = weight * category_confidences[category]
                weighted_score += category_scores[category] * adjusted_weight
                total_weight += adjusted_weight
        
        # Normalize by total weight
        if total_weight > 0:
            base_score = weighted_score / total_weight
        else:
            base_score = 0
        
        # Apply professional language bonus (reduces risk for well-structured descriptions)
        text_result = analysis_results.get('text')
        if text_result:
            professional_bonus = self._calculate_professional_bonus(request.job_text)
            base_score = max(0, base_score - professional_bonus)
        
        # Apply platform-specific risk multiplier
        platform_multiplier = self._get_platform_risk_multiplier(analysis_results.get('platform'))
        adjusted_score = base_score * platform_multiplier
        
        # Calculate confidence level
        confidence_level = self._calculate_confidence_level(analysis_results, request)
        
        # Ensure score is within bounds
        final_score = max(0, min(100, int(round(adjusted_score))))
        
        return final_score, confidence_level

    def _calculate_professional_bonus(self, job_text: str) -> float:
        """
        Calculate bonus for professional language and structure.
        
        Args:
            job_text: Job description text
            
        Returns:
            Bonus points to subtract from risk score (0-25)
        """
        if not job_text:
            return 0
        
        bonus = 0
        text_lower = job_text.lower()
        
        # Professional structure indicators
        structure_indicators = [
            'responsibilities:', 'requirements:', 'qualifications:', 
            'about the role:', 'job description:', 'duties include:',
            'we are looking for:', 'the ideal candidate:', 'about us:',
            'what you\'ll do:', 'what we offer:', 'benefits:', 'perks:',
            'key responsibilities:', 'required skills:', 'preferred qualifications:'
        ]
        
        structure_count = sum(1 for indicator in structure_indicators if indicator in text_lower)
        if structure_count >= 3:
            bonus += 10  # Well-structured job posting
        elif structure_count >= 2:
            bonus += 7
        elif structure_count >= 1:
            bonus += 4
        
        # Professional language indicators
        professional_terms = [
            'bachelor\'s degree', 'master\'s degree', 'years of experience',
            'proven track record', 'strong communication skills', 'team player',
            'competitive salary', 'benefits package', 'equal opportunity employer',
            'professional development', 'career growth', 'health insurance',
            '401k', 'pto', 'paid time off', 'work-life balance', 'remote work',
            'hybrid work', 'flexible schedule', 'mentorship', 'training'
        ]
        
        professional_count = sum(1 for term in professional_terms if term in text_lower)
        if professional_count >= 5:
            bonus += 8  # Very professional language
        elif professional_count >= 3:
            bonus += 5
        elif professional_count >= 1:
            bonus += 2
        
        # Technical skills mentioned (indicates legitimate technical role)
        technical_skills = [
            'python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes',
            'react', 'angular', 'node.js', 'git', 'agile', 'scrum', 'devops',
            'machine learning', 'data analysis', 'project management', 'html',
            'css', 'typescript', 'mongodb', 'postgresql', 'redis', 'api',
            'microservices', 'ci/cd', 'jenkins', 'terraform', 'ansible'
        ]
        
        technical_count = sum(1 for skill in technical_skills if skill in text_lower)
        if technical_count >= 4:
            bonus += 7  # Technical role with many specific skills
        elif technical_count >= 2:
            bonus += 4
        elif technical_count >= 1:
            bonus += 2
        
        # Length and detail bonus (longer, more detailed descriptions are typically more legitimate)
        word_count = len(job_text.split())
        if word_count >= 200:
            bonus += 5  # Very detailed description
        elif word_count >= 100:
            bonus += 3  # Good detail level
        elif word_count >= 50:
            bonus += 1  # Adequate detail
        
        return min(25, bonus)  # Cap at 25 points

    def _calculate_confidence_level(self, analysis_results: Dict[str, AnalysisResult], request: JobAnalysisRequest) -> str:
        """
        Calculate confidence level based on available information and signal consistency.
        
        Args:
            analysis_results: Dictionary of analysis results from all analyzers
            request: Original request to check completeness
            
        Returns:
            Confidence level: "High", "Medium", or "Low"
        """
        # Check metadata completeness
        has_email = bool(request.recruiter_email and request.recruiter_email.strip())
        has_url = bool(request.company_url and request.company_url.strip())
        has_platform = bool(request.platform_source and request.platform_source.strip())
        
        metadata_completeness = sum([has_email, has_url, has_platform]) / 3.0
        
        # Check text quality
        text_result = analysis_results.get('text')
        text_confidence = text_result.confidence if text_result else 0.5
        
        # Check for conflicting signals
        text_factors = text_result.risk_factors if text_result else []
        email_factors = analysis_results.get('email', AnalysisResult(risk_factors=[], confidence=0.5, analyzer_name="EmailAnalyzer")).risk_factors
        url_factors = analysis_results.get('url', AnalysisResult(risk_factors=[], confidence=0.5, analyzer_name="URLAnalyzer")).risk_factors
        
        high_risk_text = any(f.severity >= 70 for f in text_factors)
        high_risk_metadata = any(f.severity >= 70 for f in email_factors + url_factors)
        
        # Determine confidence level
        if metadata_completeness >= 0.67 and text_confidence >= 0.8:
            if not (high_risk_text and not high_risk_metadata) and not (high_risk_metadata and not high_risk_text):
                return "High"  # Complete info, consistent signals
        
        if text_confidence >= 0.7 and len(request.job_text.split()) >= 50:
            return "Medium"  # Good text analysis even with missing metadata
        
        return "Low"  # Incomplete info or conflicting signals

    def _get_platform_risk_multiplier(self, platform_result: AnalysisResult) -> float:
        """
        Get platform-specific risk multiplier from platform analyzer.
        
        Args:
            platform_result: AnalysisResult from platform analyzer
            
        Returns:
            Risk multiplier (1.0 = no adjustment)
        """
        if not platform_result or not platform_result.risk_factors:
            return 1.0
        
        # Look for platform-specific risk factors that indicate higher/lower risk
        multiplier = 1.0
        
        for factor in platform_result.risk_factors:
            if 'high fraud' in factor.description.lower():
                multiplier = max(multiplier, 1.4)
            elif 'messaging apps' in factor.description.lower():
                multiplier = max(multiplier, 1.3)
            elif 'social media' in factor.description.lower():
                multiplier = max(multiplier, 1.2)
            elif 'lower credibility' in factor.description.lower():
                multiplier = max(multiplier, 1.1)
        
        return multiplier

    def _determine_verdict(self, risk_score: int) -> VerdictEnum:
        """
        Determine verdict category based on risk score.
        
        Args:
            risk_score: Overall risk score (0-100)
            
        Returns:
            VerdictEnum representing the risk level
        """
        if risk_score <= self.verdict_thresholds['safe']:
            return VerdictEnum.SAFE
        elif risk_score <= self.verdict_thresholds['caution']:
            return VerdictEnum.CAUTION
        else:
            return VerdictEnum.HIGH_RISK

    def _generate_flags(self, analysis_results: Dict[str, AnalysisResult]) -> List[str]:
        """
        Generate list of risk flags from all analysis results.
        
        Prioritizes the most significant risk factors and limits to avoid overwhelming users.
        
        Args:
            analysis_results: Dictionary of analysis results from all analyzers
            
        Returns:
            List of descriptive flag strings
        """
        all_risk_factors = []
        
        # Collect all risk factors
        for result in analysis_results.values():
            all_risk_factors.extend(result.risk_factors)
        
        # Sort by severity (weighted by confidence) in descending order
        all_risk_factors.sort(
            key=lambda f: f.severity * f.confidence, 
            reverse=True
        )
        
        # Generate flags from top risk factors
        flags = []
        seen_descriptions = set()
        
        for factor in all_risk_factors:
            # Avoid duplicate or very similar flags
            if factor.description not in seen_descriptions:
                flags.append(factor.description)
                seen_descriptions.add(factor.description)
                
                # Limit to top 8 flags to avoid overwhelming users
                if len(flags) >= 8:
                    break
        
        return flags

    def _generate_explanation(
        self, 
        analysis_results: Dict[str, AnalysisResult], 
        risk_score: int, 
        verdict: VerdictEnum,
        confidence_level: str
    ) -> str:
        """
        Generate human-readable explanation of the risk assessment.
        
        Args:
            analysis_results: Dictionary of analysis results from all analyzers
            risk_score: Overall risk score
            verdict: Determined verdict
            
        Returns:
            Human-readable explanation string
        """
        # Collect and prioritize risk factors
        all_risk_factors = []
        for result in analysis_results.values():
            all_risk_factors.extend(result.risk_factors)
        
        # Sort by weighted severity
        all_risk_factors.sort(
            key=lambda f: f.severity * f.confidence, 
            reverse=True
        )
        
        # Start building explanation
        explanation_parts = []
        
        # Opening statement based on verdict and confidence
        if verdict == VerdictEnum.SAFE:
            explanation_parts.append(
                f"This job posting appears legitimate with a low risk score of {risk_score} ({confidence_level.lower()} confidence)."
            )
        elif verdict == VerdictEnum.CAUTION:
            explanation_parts.append(
                f"This job posting shows some concerning signs with a moderate risk score of {risk_score} ({confidence_level.lower()} confidence)."
            )
        else:  # HIGH_RISK
            explanation_parts.append(
                f"This job posting has significant red flags with a high risk score of {risk_score} ({confidence_level.lower()} confidence)."
            )
        
        # Add details about top risk factors (limit to top 3 for readability)
        if all_risk_factors:
            top_factors = all_risk_factors[:3]
            
            if len(top_factors) == 1:
                explanation_parts.append(f"The main concern is: {top_factors[0].description.lower()}.")
            else:
                concerns = [factor.description.lower() for factor in top_factors]
                if len(concerns) == 2:
                    explanation_parts.append(f"Key concerns include: {concerns[0]} and {concerns[1]}.")
                else:
                    explanation_parts.append(
                        f"Key concerns include: {', '.join(concerns[:-1])}, and {concerns[-1]}."
                    )
        
        # Add category-specific insights
        category_insights = self._get_category_insights(analysis_results)
        if category_insights:
            explanation_parts.append(category_insights)
        
        # Add recommendation based on verdict
        if verdict == VerdictEnum.SAFE:
            explanation_parts.append(
                "The job posting meets standard legitimacy criteria, but always verify details independently."
            )
        elif verdict == VerdictEnum.CAUTION:
            explanation_parts.append(
                "Exercise caution and verify company details before proceeding with any application."
            )
        else:  # HIGH_RISK
            explanation_parts.append(
                "Strong recommendation to avoid this opportunity and report if encountered on job platforms."
            )
        
        return " ".join(explanation_parts)

    def _get_category_insights(self, analysis_results: Dict[str, AnalysisResult]) -> str:
        """
        Generate category-specific insights for the explanation.
        
        Args:
            analysis_results: Dictionary of analysis results from all analyzers
            
        Returns:
            Category-specific insight string or empty string
        """
        insights = []
        
        # Text analysis insights
        text_result = analysis_results.get('text')
        if text_result and text_result.risk_factors:
            high_severity_text_factors = [
                f for f in text_result.risk_factors 
                if f.severity >= 60
            ]
            if high_severity_text_factors:
                insights.append("the job description contains suspicious elements")
        
        # Email analysis insights
        email_result = analysis_results.get('email')
        if email_result and email_result.risk_factors:
            high_severity_email_factors = [
                f for f in email_result.risk_factors 
                if f.severity >= 60
            ]
            if high_severity_email_factors:
                insights.append("the recruiter email raises credibility concerns")
        
        # URL analysis insights
        url_result = analysis_results.get('url')
        if url_result and url_result.risk_factors:
            high_severity_url_factors = [
                f for f in url_result.risk_factors 
                if f.severity >= 60
            ]
            if high_severity_url_factors:
                insights.append("the company URL appears questionable")
        
        # Platform analysis insights
        platform_result = analysis_results.get('platform')
        if platform_result and platform_result.risk_factors:
            high_severity_platform_factors = [
                f for f in platform_result.risk_factors 
                if f.severity >= 60
            ]
            if high_severity_platform_factors:
                insights.append("the platform source has credibility issues")
        
        if insights:
            if len(insights) == 1:
                return f"Specifically, {insights[0]}."
            elif len(insights) == 2:
                return f"Specifically, {insights[0]} and {insights[1]}."
            else:
                return f"Specifically, {', '.join(insights[:-1])}, and {insights[-1]}."
        
        return ""