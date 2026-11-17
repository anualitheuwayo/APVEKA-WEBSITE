from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class StudentCreate(BaseModel):
    """What the headmaster sends to POST /students to register a new student."""
    admission_number: str
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    address: Optional[str] = None
    class_id: Optional[int] = None


class StudentUpdate(BaseModel):
    """All optional — PUT /students/{id} only changes what's included."""
    full_name: Optional[str] = None
    gender: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    address: Optional[str] = None
    class_id: Optional[int] = None
    is_active: Optional[bool] = None


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    admission_number: str
    full_name: str
    date_of_birth: Optional[date]
    gender: Optional[str]
    parent_name: Optional[str]
    parent_phone: Optional[str]
    address: Optional[str]
    class_id: Optional[int]
    enrollment_date: Optional[date]
    is_active: bool