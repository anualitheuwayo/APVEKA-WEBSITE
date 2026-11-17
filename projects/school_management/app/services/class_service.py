# app/services/class_service.py
"""
Business rules for classes and teacher assignments.
"""
from fastapi import HTTPException

from app.schemas import SchoolClassCreate, SchoolClassUpdate, TeacherAssignmentCreate
from app.repository import class_repository as class_repo
from app.repository import teacher_repository as teacher_repo
from app.repository import class_assignment_repository as assignment_repo


def create_class(db, payload: SchoolClassCreate):
    if class_repo.get_by_name(db, payload.name):
        raise HTTPException(status_code=400, detail="Class name already exists")
    return class_repo.create(db, **payload.model_dump())


def list_classes(db):
    return class_repo.list_all(db)


def get_class(db, class_id: int):
    school_class = class_repo.get_by_id(db, class_id)
    if not school_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return school_class


def update_class(db, class_id: int, payload: SchoolClassUpdate):
    school_class = class_repo.get_by_id(db, class_id)
    if not school_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_repo.update(db, school_class, payload.model_dump(exclude_unset=True))


def assign_teacher_to_class(db, class_id: int, payload: TeacherAssignmentCreate):
    """Creates one ClassAssignment row: 'this teacher teaches this class.'"""
    if not class_repo.get_by_id(db, class_id):
        raise HTTPException(status_code=404, detail="Class not found")
    if not teacher_repo.get_by_id(db, payload.teacher_id):
        raise HTTPException(status_code=404, detail="Teacher not found")
    if assignment_repo.exists(db, teacher_id=payload.teacher_id, class_id=class_id):
        raise HTTPException(status_code=400, detail="This teacher is already assigned to this class")
    return assignment_repo.create(db, teacher_id=payload.teacher_id, class_id=class_id)