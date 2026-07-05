from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from app.enums import EmploymentType, JobStatus

class JobCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    title: str = Field(min_length=1, max_length=200)
    company: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=10_000)
    location: str | None = Field(default=None, max_length=200)
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)
    employment_type: EmploymentType = EmploymentType.full_time
    tags: list[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def _normalize_title(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("title must not be blank")
        return trimmed

    @model_validator(mode="after")
    def _check_salary_bounds(self) -> "JobCreate":
        if (
            self.salary_min and \
            self.salary_max and \
            self.salary_min > self.salary_max
        ):
            raise ValueError("salary_min must be <= salary_max")
        return self

class JobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    company: str
    description: str | None
    location: str | None
    salary_min: int | None
    salary_max: int | None
    employement_type: EmploymentType
    tags: list[str]
    status: JobStatus
    created_at: datetime
    updated_at: datetime