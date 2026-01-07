# Job Analysis API Design Document

## Overview

The Job Analysis API is a FastAPI-based service that evaluates job postings for potential fraud and suspicious activity. The system analyzes multiple data points including job descriptions, company information, recruiter details, and platform sources to generate comprehensive risk assessments. The API provides a single POST endpoint that accepts job posting data and returns structured risk analysis results.

## Architecture

The system follows a layered architecture pattern:

- **API Layer**: FastAPI application handling HTTP requests and responses
- **Service Layer**: Business logic for job analysis and risk assessment
- **Analysis Layer**: Specialized analyzers for different data types (text, email, URL)
- **Data Models**: Pydantic models for request/response validation and serialization

The architecture emphasizes separation of concerns, making the system maintainable and allowing individual components to be tested and modified independently.

## Components and Interfaces

### API Controller
- **JobAnalysisController**: Handles the `/analyze-job` POST endpoint
- Validates incoming requests using Pydantic models
- Orchestrates the analysis process
- Formats and returns responses

### Analysis Service
- **JobAnalysisService**: Core business logic coordinator
- Aggregates results from individual analyzers
- Calculates overall risk scores
- Generates final verdicts and explanations

### Specialized Analyzers
- **TextAnalyzer**: Evaluates job descriptions for suspicious patterns
- **EmailAnalyzer**: Validates email formats and assesses domain reputation
- **URLAnalyzer**: Checks company URL validity and domain characteristics
- **ContextAnalyzer**: Assesses platform credibility and context

### Data Models
- **JobAnalysisRequest**: Input validation model
- **JobAnalysisResponse**: Output formatting model
- **RiskAssessment**: Internal risk calculation model

## Data Models

### Request Model
```python
class JobAnalysisRequest(BaseModel):
    job_text: str
    company_url: str
    recruiter_email: str
    platform_source: str
```

### Response Model
```python
class JobAnalysisResponse(BaseModel):
    risk_score: int  # 0-100
    flags: List[str]
    explanation: str
    verdict: Literal["Safe", "Suspicious", "High Risk"]
```

### Internal Models
```python
class RiskFactor(BaseModel):
    category: str
    severity: int
    description: str
    
class AnalysisResult(BaseModel):
    risk_factors: List[RiskFactor]
    confidence: float
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*
Property 1: Valid requests always produce complete responses
*For any* valid job analysis request with all required fields, the system should return a response containing risk_score, flags, explanation, and verdict
**Validates: Requirements 1.4**

Property 2: Risk scores are always within valid bounds
*For any* job analysis request, the returned risk_score should be an integer between 0 and 100 inclusive
**Validates: Requirements 2.5, 5.2**

Property 3: Verdicts use only predefined categories
*For any* job analysis response, the verdict should be exactly one of "Safe", "Caution", or "High Risk"
**Validates: Requirements 3.3, 5.5**

Property 4: Response format consistency
*For any* successful job analysis request, the response should be valid JSON with consistent field names (risk_score, flags, explanation, verdict)
**Validates: Requirements 5.1**

Property 5: Flags are always descriptive arrays
*For any* job analysis response, the flags field should be an array of non-empty strings
**Validates: Requirements 5.3**

Property 6: Input validation rejects incomplete requests
*For any* request missing required fields (job_text, company_url, recruiter_email, platform_source), the system should return a 422 status code with field-specific error messages
**Validates: Requirements 4.2**

Property 7: Email validation consistency
*For any* email address input, the system should consistently validate format and assess domain characteristics
**Validates: Requirements 2.3**

Property 8: URL validation consistency
*For any* URL input, the system should consistently validate format and assess domain legitimacy
**Validates: Requirements 2.2**

Property 9: Explanations are always provided
*For any* job analysis response, the explanation field should contain non-empty, human-readable text
**Validates: Requirements 3.2, 5.4**

Property 10: Text analysis consistency
*For any* job text input, the analysis should consistently evaluate content for fraud indicators and suspicious patterns
**Validates: Requirements 2.1**

## Error Handling

The system implements comprehensive error handling at multiple levels:

### Input Validation Errors
- **400 Bad Request**: Malformed JSON or invalid request format
- **422 Unprocessable Entity**: Missing required fields or invalid field values
- Field-specific error messages for debugging

### Processing Errors
- **500 Internal Server Error**: Unexpected system failures
- Error messages that don't expose sensitive system details
- Graceful degradation when individual analyzers fail

### Rate Limiting
- **429 Too Many Requests**: When request limits are exceeded
- Configurable rate limiting per client/IP

### Logging and Monitoring
- Structured logging for all error conditions
- Error tracking for system reliability monitoring
- Performance metrics collection

## Testing Strategy

The testing approach combines unit testing and property-based testing to ensure comprehensive coverage:

### Unit Testing
- Test specific examples of valid and invalid inputs
- Test individual analyzer components in isolation
- Test error handling scenarios with known inputs
- Test API endpoint integration with FastAPI test client

### Property-Based Testing
- Use **Hypothesis** for Python property-based testing framework
- Configure each property-based test to run a minimum of 100 iterations
- Test universal properties that should hold across all inputs
- Generate random but valid job posting data for comprehensive testing

**Property-Based Test Requirements:**
- Each property-based test must be tagged with: `**Feature: job-analysis-api, Property {number}: {property_text}**`
- Each correctness property must be implemented by a single property-based test
- Tests must validate real functionality without mocks for core logic

### Test Data Generation
- Smart generators for realistic job posting content
- Email address generators with various domain types
- URL generators with different validity levels
- Platform source generators covering major job boards

### Integration Testing
- End-to-end API testing with realistic job posting scenarios
- Error condition testing with malformed requests
- Performance testing under load conditions

The dual testing approach ensures both specific edge cases are covered (unit tests) and general correctness properties hold across all inputs (property tests).

Each analyzer must return:
- score: float (0–1)
- flags: List[str]
- confidence: float (0–1)

ExplanationGenerator:
- Ranks risk factors by severity
- Selects top 2 contributors
- Generates human-readable explanation
