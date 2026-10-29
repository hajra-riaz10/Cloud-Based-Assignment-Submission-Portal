from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class UrlSubmissionCreate(BaseModel):
    student_name: str = Field(min_length=1, max_length=150)
    registration_number: str = Field(min_length=1, max_length=50)
    assignment_title: str = Field(min_length=1, max_length=200)
    submission_url: HttpUrl

    model_config = ConfigDict(str_strip_whitespace=True)


class UrlSubmissionOut(BaseModel):
    id: int
    student_name: str
    registration_number: str
    assignment_title: str
    submission_url: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)