# app/services/teacher_service.py
"""
Business rules for teacher profiles, including the one lookup almost every
other service needs: 'which classes does this logged-in user teach?'
"""
from typing import List

from app.models import User
from app.repository import teacher_repository as teacher_repo
from app.repository import class_assignment_repository as assignment_repo


def list_teachers(db):
    return teacher_repo.list_all(db)


def class_ids_taught_by(db, current_user: User) -> List[int]:
    """
    Given any logged-in user, find every class_id they're assigned to teach.
    Returns [] for a headmaster or for a teacher with no assignments yet —
    callers decide what an empty list means for them.
    """
    teacher = teacher_repo.get_by_user_id(db, current_user.id)
    if not teacher:
        return []
    return assignment_repo.class_ids_for_teacher(db, teacher.id)