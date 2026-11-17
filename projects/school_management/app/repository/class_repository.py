
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models import SchoolClass


def get_by_name(db: Session, name: str) -> Optional[SchoolClass]:
    return db.query(SchoolClass).filter(SchoolClass.name == name).first()

def get_by_id(db: Session, class_id: int) -> Optional[SchoolClass]:
    return db.get(SchoolClass, class_id)

def create(db: Session, **fields) -> SchoolClass:
    school_class = SchoolClass(**fields)
    db.add(school_class)
    db.commit()
    db.refresh(school_class)
    return school_class


def update(db: Session, school_class: SchoolClass, fields: dict) -> SchoolClass:
    for key, value in fields.items():
        setattr(school_class, key, value)
    db.commit()
    db.refresh(school_class)
    return school_class


def list_all(db: Session) -> List[SchoolClass]:
    return db.query(SchoolClass).all()