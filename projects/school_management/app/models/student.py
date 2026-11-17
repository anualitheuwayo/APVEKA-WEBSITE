from datetime import date

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    admission_number = Column(String(30), unique=True, nullable=False, index=True)
    full_name = Column(String(120), nullable=False)
    date_of_birth = Column(Date)
    gender = Column(String(10))
    parent_name = Column(String(120))
    parent_phone = Column(String(30))
    address = Column(Text)
    class_id = Column(Integer, ForeignKey("school_classes.id"), nullable=True)
    enrollment_date = Column(Date, default=date.today)
    registered_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)

    school_class = relationship("SchoolClass", back_populates="students")
    registered_by = relationship("User")
    attendance_records = relationship("Attendance", back_populates="student")
    grades = relationship("Grade", back_populates="student")