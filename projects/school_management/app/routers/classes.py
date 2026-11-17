
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.models import User
from app.schemas import (
    SchoolClassCreate, SchoolClassUpdate, SchoolClassOut,
    TeacherAssignmentCreate, ClassAssignmentOut,
)
from app.core import get_current_user, require_headmaster
from app.services import class_service

router = APIRouter(prefix="/classes", tags=["classes"])


@router.post("", response_model=SchoolClassOut, status_code=status.HTTP_201_CREATED)
def create_class(
    payload: SchoolClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_headmaster),
):
    return class_service.create_class(db, payload)


@router.get("", response_model=List[SchoolClassOut])
def list_classes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return class_service.list_classes(db)


@router.get("/{class_id}", response_model=SchoolClassOut)
def get_class(class_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return class_service.get_class(db, class_id)


@router.put("/{class_id}", response_model=SchoolClassOut)
def update_class(
    class_id: int,
    payload: SchoolClassUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_headmaster),
):
    return class_service.update_class(db, class_id, payload)


@router.post("/{class_id}/teachers", response_model=ClassAssignmentOut, status_code=status.HTTP_201_CREATED)
def assign_teacher_to_class(
    class_id: int,
    payload: TeacherAssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_headmaster),  # only the headmaster assigns teachers to classes
):
    return class_service.assign_teacher_to_class(db, class_id, payload)