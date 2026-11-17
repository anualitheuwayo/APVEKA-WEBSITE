# app/repository/user_repository.py
"""
Pure data-access for User/Teacher. No business rules, no auth checks —
just 'fetch this from the database' and 'save that to the database.'
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models import User, Teacher, RoleEnum


def get_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_by_username_or_email(db: Session, username: str, email: str) -> Optional[User]:
    return db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()


def headmaster_exists(db: Session) -> bool:
    return db.query(User).filter(User.role == RoleEnum.headmaster).first() is not None


def create_user(db: Session, *, username: str, email: str, hashed_password: str, role: RoleEnum) -> User:
    user = User(username=username, email=email, hashed_password=hashed_password, role=role)
    db.add(user)
    db.flush()  # assigns user.id without fully committing yet
    return user


def create_teacher_profile(db: Session, *, user_id: int, full_name: str,
                            subject_specialty: Optional[str], phone: Optional[str]) -> Teacher:
    teacher = Teacher(user_id=user_id, full_name=full_name,
                       subject_specialty=subject_specialty, phone=phone)
    db.add(teacher)
    return teacher


def commit_and_refresh(db: Session, obj):
    db.commit()
    db.refresh(obj)
    return obj