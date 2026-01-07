# Requirements Document

## Introduction

The Job Analysis API is a FastAPI backend service that analyzes job postings to assess their legitimacy and potential risks. The system evaluates job descriptions, company information, and recruiter details to provide risk assessments and recommendations to help users identify potentially fraudulent or suspicious job opportunities.

## Glossary

- **Job_Analysis_System**: The FastAPI backend service that processes job posting data and returns risk assessments
- **Job_Text**: The textual content of a job posting including description, requirements, and responsibilities
- **Company_URL**: The web address of the hiring company's official website
- **Recruiter_Email**: The email address of the person or entity posting the job
- **Platform_Source**: The job board or platform where the job posting was found (e.g., LinkedIn, Indeed, company website)
- **Risk_Score**: A numerical value (0-100) indicating the likelihood that a job posting is fraudulent or suspicious
- **Risk_Flags**: Specific indicators or warning signs identified in the job posting analysis
- **Risk_Explanation**: Detailed reasoning behind the risk assessment and identified flags
- **Risk_Verdict**: A categorical assessment (e.g., "Safe", "Caution", "High Risk") based on the overall analysis

## Requirements

### Requirement 1

**User Story:** As a job seeker, I want to submit job posting details for analysis, so that I can receive a comprehensive risk assessment before applying.

#### Acceptance Criteria

1. WHEN a user sends a POST request to /analyze-job with job_text, company_url, recruiter_email, and platform_source, THE Job_Analysis_System SHALL accept and process the request
2. WHEN the request contains all required fields, THE Job_Analysis_System SHALL validate the input data format and structure
3. WHEN input validation passes, THE Job_Analysis_System SHALL analyze the provided job posting data
4. WHEN analysis is complete, THE Job_Analysis_System SHALL return a response containing risk_score, flags, explanation, and verdict
5. WHEN the request is malformed or missing required fields, THE Job_Analysis_System SHALL return appropriate error messages with HTTP status codes

### Requirement 2

**User Story:** As a job seeker, I want to receive accurate risk scores and detailed explanations, so that I can make informed decisions about job opportunities.

#### Acceptance Criteria

1. WHEN analyzing job_text, THE Job_Analysis_System SHALL evaluate content for common fraud indicators and suspicious patterns
2. WHEN processing company_url, THE Job_Analysis_System SHALL validate the URL format and assess domain legitimacy
3. WHEN examining recruiter_email, THE Job_Analysis_System SHALL check email format validity and domain reputation
4. WHEN considering platform_source, THE Job_Analysis_System SHALL factor platform credibility into the risk assessment
5. WHEN generating risk_score, THE Job_Analysis_System SHALL produce a numerical value between 0 and 100 based on identified risk factors

### Requirement 3

**User Story:** As a job seeker, I want to understand why a job posting received a specific risk rating, so that I can learn to identify red flags myself.

#### Acceptance Criteria

1. WHEN risk flags are identified, THE Job_Analysis_System SHALL provide specific descriptions of each detected issue
2. WHEN generating explanations, THE Job_Analysis_System SHALL include reasoning for the assigned risk score
3. WHEN determining verdict, THE Job_Analysis_System SHALL categorize risk level as "Safe", "Caution", or "High Risk"
4. WHEN multiple risk factors are present, THE Job_Analysis_System SHALL prioritize and explain the most significant concerns
5. WHEN no significant risks are detected, THE Job_Analysis_System SHALL provide reassuring feedback about positive indicators

### Requirement 4

**User Story:** As a system administrator, I want the API to handle errors gracefully and provide meaningful responses, so that the service remains reliable and user-friendly.

#### Acceptance Criteria

1. WHEN invalid JSON is submitted, THE Job_Analysis_System SHALL return a 400 Bad Request with clear error description
2. WHEN required fields are missing, THE Job_Analysis_System SHALL return a 422 Unprocessable Entity with field-specific error messages
3. WHEN internal processing errors occur, THE Job_Analysis_System SHALL return a 500 Internal Server Error without exposing sensitive system details
4. WHEN the service is unavailable, THE Job_Analysis_System SHALL return appropriate HTTP status codes
5. WHEN rate limiting is exceeded, THE Job_Analysis_System SHALL return a 429 Too Many Requests response

### Requirement 5

**User Story:** As a developer integrating with the API, I want consistent and well-structured response formats, so that I can reliably parse and use the analysis results.

#### Acceptance Criteria

1. WHEN returning successful analysis results, THE Job_Analysis_System SHALL format responses as valid JSON with consistent field names
2. WHEN providing risk_score values, THE Job_Analysis_System SHALL ensure they are integers between 0 and 100
3. WHEN listing flags, THE Job_Analysis_System SHALL return them as an array of descriptive strings
4. WHEN generating explanations, THE Job_Analysis_System SHALL provide clear, human-readable text
5. WHEN determining verdicts, THE Job_Analysis_System SHALL use only predefined categorical values