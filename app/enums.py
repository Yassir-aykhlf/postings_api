from enum import Enum

class EmploymentType(str, Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    internship = "internship"
    temporary = "temporary"

class JobStatus(str, Enum):
    draft = "draft"
    open = "open"
    closed = "closed"