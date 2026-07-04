from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class JobCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    title: str = Field(min_length=1, max_length=200)
    company: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=10_000)
    location: str | None = Field(default=None, max_length=200)
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)
    tags: list[str] = Field(default_factory=list)

class JobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    company: str
    description: str | None
    location: str | None
    salary_min: int | None
    salary_max: int | None
    tags: list[str]
    status: str
    created_at: datetime
    updated_at: datetime