from pydantic import BaseModel, Field, validator
from typing import Optional
import re


class JobAnalysisRequest(BaseModel):
    """
    Request model for job analysis endpoint.

    company_url and recruiter_email are OPTIONAL
    because many job posts don't provide them.
    """

    job_text: str = Field(
        ...,
        min_length=10,
        max_length=10000,
        description="The textual content of the job posting"
    )

    company_url: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional company website URL"
    )

    recruiter_email: Optional[str] = Field(
        None,
        max_length=254,
        description="Optional recruiter email address"
    )

    platform_source: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Source platform (e.g. chrome, LinkedIn)"
    )

    # ---------------- VALIDATORS ---------------- #

    @validator("job_text")
    def validate_job_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Job text cannot be empty")
        return v.strip()

    @validator("company_url")
    def validate_company_url(cls, v):
        if v is None or v.strip() == "":
            return None  # ✅ allow empty / missing

        v = v.strip()
        url_pattern = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}(?:\.\d{1,3}){3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$',
            re.IGNORECASE
        )

        if not url_pattern.match(v):
            raise ValueError("Company URL must be a valid URL")

        return v

    @validator("recruiter_email")
    def validate_recruiter_email(cls, v):
        if v is None or v.strip() == "":
            return None  # ✅ allow empty / missing

        v = v.strip().lower()
        email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )

        if not email_pattern.match(v):
            raise ValueError("Recruiter email must be a valid email")

        return v

    @validator("platform_source")
    def validate_platform_source(cls, v):
        if not v or not v.strip():
            raise ValueError("Platform source cannot be empty")
        return v.strip()

    class Config:
        schema_extra = {
            "example": {
                "job_text": "We are hiring a Software Engineer with Python experience.",
                "company_url": "https://example.com",
                "recruiter_email": "hr@example.com",
                "platform_source": "chrome"
            }
        }
