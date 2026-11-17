# app/services/auth_service.py
"""
Business rules for accounts: who can register whom, how login works,
and the one-time bootstrap for the very first headmaster.
"""
from fastapi import HTTPException

from app.models import RoleEnum, User
from app.schemas import UserCreate
from app.core import hash_password, verify_password, create_access_token
from app.repository import user_repository as user_repo


def register_user(db, payload: UserCreate) -> User:
    """Called only after the router confirms the caller is a headmaster."""
    if user_repo.get_by_username_or_email(db, payload.username, payload.email):
        raise HTTPException(status_code=400, detail="Username or email already registered")

    if payload.role == RoleEnum.teacher and not payload.full_name:
        raise HTTPException(status_code=400, detail="full_name is required when registering a teacher")

    user = user_repo.create_user(
        db, username=payload.username, email=payload.email,
        hashed_password=hash_password(payload.password), role=payload.role,
    )
    if payload.role == RoleEnum.teacher:
        user_repo.create_teacher_profile(
            db, user_id=user.id, full_name=payload.full_name,
            subject_specialty=payload.subject_specialty, phone=payload.phone,
        )
    return user_repo.commit_and_refresh(db, user)


def bootstrap_first_headmaster(db, payload: UserCreate) -> User:
    """Unauthenticated on purpose — but locks itself the moment any headmaster exists."""
    if user_repo.headmaster_exists(db):
        raise HTTPException(status_code=403, detail="A headmaster already exists. Ask them to register your account.")
    user = user_repo.create_user(
        db, username=payload.username, email=payload.email,
        hashed_password=hash_password(payload.password), role=RoleEnum.headmaster,
    )
    return user_repo.commit_and_refresh(db, user)


def login(db, username: str, password: str) -> str:
    """Returns a signed JWT access token, or raises 401/403."""
    user = user_repo.get_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")
    return create_access_token(data={"sub": user.username, "role": user.role.value})