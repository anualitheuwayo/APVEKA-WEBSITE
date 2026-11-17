from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class SchoolClass(Base):
    """A class/section, e.g. 'P1 A' or 'Low A' (nursery)."""
    __tablename__ = "school_classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, nullable=False)
    grade_level = Column(String(30))   # e.g. "Nursery - Low", "Primary 1"

    teacher_assignments = relationship("ClassAssignment", back_populates="school_class")
    students = relationship("Student", back_populates="school_class")