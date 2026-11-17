
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models import Student


def get_by_admission_number(db: Session, admission_number: str) -> Optional[Student]:
    return db.query(Student).filter(Student.admission_number == admission_number).first()

def get_by_id(db: Session, student_id: int) -> Optional[Student]:
    return db.get(Student, student_id)


def create(db: Session, *, registered_by_id: int, **fields) -> Student:
    student = Student(**fields, registered_by_id=registered_by_id)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def list_active(db: Session, class_ids: Optional[List[int]] = None,
                 class_id: Optional[int] = None) -> List[Student]:
    query = db.query(Student).filter(Student.is_active == True)  # noqa: E712
    if class_ids is not None:
        query = query.filter(Student.class_id.in_(class_ids))
    if class_id is not None:
        query = query.filter(Student.class_id == class_id)
    return query.all()


def update(db: Session, student: Student, fields: dict) -> Student:
    for key, value in fields.items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student


def deactivate(db: Session, student: Student) -> None:
    student.is_active = False
    db.commit()