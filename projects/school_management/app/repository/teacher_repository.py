# app/repository/teacher_repository.py
"""Pure data-access for Teacher profiles — mostly lookups, since creation
happens inside user_repository.create_teacher_profile as part of registration."""
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models import Teacher


def list_all(db: Session) -> List[Teacher]:
    return db.query(Teacher).all()


def get_by_id(db: Session, teacher_id: int) -> Optional[Teacher]:
    return db.get(Teacher, teacher_id)


def get_by_user_id(db: Session, user_id: int) -> Optional[Teacher]:
    return db.query(Teacher).filter(Teacher.user_id == user_id).first()