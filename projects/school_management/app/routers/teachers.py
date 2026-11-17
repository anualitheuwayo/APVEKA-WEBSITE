# app/routers/teachers.py
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from app.models import User
from app.schemas import TeacherOut
from app.core import require_headmaster
from app.services import teacher_service

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get("", response_model=List[TeacherOut])
def list_teachers(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_headmaster),  # headmaster needs teacher ids to assign classes
):
    return teacher_service.list_teachers(db)