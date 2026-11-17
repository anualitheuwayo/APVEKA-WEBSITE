from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.enums import RoleEnum


class UserCreate(BaseModel):
    """What the headmaster sends to POST /auth/register (or the one-time bootstrap)."""
    username: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.teacher
    full_name: Optional[str] = None          # required in practice if role == teacher
    subject_specialty: Optional[str] = None  # the subject this teacher will teach
    phone: Optional[str] = None


class UserOut(BaseModel):
    """What we send back after login/registration — notice hashed_password is NOT here."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    role: RoleEnum
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str