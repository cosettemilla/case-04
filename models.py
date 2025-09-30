from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class SurveySubmission(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)
    consent: bool = Field(..., description="Must be true to accept")
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = Field(None, max_length=1000)
    user_agent: Optional[str] = None
    submission_id: Optional[str] = None   # ✅ added


class StoredSurveyRecord(SurveySubmission):
    received_at: datetime
    ip: str
