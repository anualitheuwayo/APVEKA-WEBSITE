from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class ClassAssignment(Base):
    """Join table: which teacher teaches which class."""
    __tablename__ = "class_assignments"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("school_classes.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("teacher_id", "class_id", name="uq_teacher_class"),
    )

    teacher = relationship("Teacher", back_populates="class_assignments")
    school_class = relationship("SchoolClass", back_populates="teacher_assignments")