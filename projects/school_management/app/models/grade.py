from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Grade(Base):
    """One row = one subject score for one student in one term."""
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject = Column(String(80), nullable=False)
    term = Column(String(30), nullable=False)   # e.g. "Term 1 2026"
    score = Column(Float, nullable=False)
    max_score = Column(Float, default=100.0)
    recorded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    student = relationship("Student", back_populates="grades")