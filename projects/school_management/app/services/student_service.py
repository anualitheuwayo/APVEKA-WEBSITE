
from typing import Optional, List
from fastapi import HTTPException

from app.models import User, RoleEnum, Student
from app.schemas import StudentCreate, StudentUpdate
from app.repository import student_repository as student_repo
from app.repository import class_repository as class_repo
from app.services import teacher_service   



def register_student(db, payload: StudentCreate, current_user: User) -> Student:
    if student_repo.get_by_admission_number(db, payload.admission_number):
        raise HTTPException(status_code=400, detail="Admission number already in use")
    if payload.class_id is not None and not class_repo.get_by_id(db, payload.class_id):
        raise HTTPException(status_code=404, detail="Class not found")
    return student_repo.create(db, registered_by_id=current_user.id, **payload.model_dump())


def list_visible_students(db, current_user: User, class_id: Optional[int] = None) -> List[Student]:
    if current_user.role == RoleEnum.headmaster:
        return student_repo.list_active(db, class_id=class_id)
    class_ids = teacher_service.class_ids_taught_by(db, current_user)   # <-- changed
    return student_repo.list_active(db, class_ids=class_ids, class_id=class_id)


def get_student_for_user(db, student_id: int, current_user: User) -> Student:
    student = student_repo.get_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if current_user.role == RoleEnum.teacher:
        if student.class_id not in teacher_service.class_ids_taught_by(db, current_user):   # <-- changed
            raise HTTPException(status_code=403, detail="Not your class")
    return student


def update_student(db, student_id: int, payload: StudentUpdate) -> Student:
    student = student_repo.get_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_repo.update(db, student, payload.model_dump(exclude_unset=True))


def deactivate_student(db, student_id: int) -> None:
    student = student_repo.get_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student_repo.deactivate(db, student)