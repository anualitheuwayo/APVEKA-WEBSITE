
from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.models import User
from app.schemas import StudentCreate, StudentUpdate, StudentOut
from app.core import get_current_user, require_headmaster
from app.services import student_service

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def register_student(
    payload: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_headmaster),  # only the headmaster registers students
):
    return student_service.register_student(db, payload, current_user)


@router.get("", response_model=List[StudentOut])
def list_students(
    class_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return student_service.list_visible_students(db, current_user, class_id=class_id)


@router.get("/{student_id}", response_model=StudentOut)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return student_service.get_student_for_user(db, student_id, current_user)


@router.put("/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_headmaster),
):
    return student_service.update_student(db, student_id, payload)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_headmaster),
):
    student_service.deactivate_student(db, student_id)