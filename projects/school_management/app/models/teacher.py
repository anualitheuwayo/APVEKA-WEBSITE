from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Teacher(Base):
    """Extra profile info for a User whose role is 'teacher'."""
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String(120), nullable=False)
    subject_specialty = Column(String(120))   # subject they teach, given at registration
    phone = Column(String(30))

    user = relationship("User", back_populates="teacher_profile")
    class_assignments = relationship("ClassAssignment", back_populates="teacher")