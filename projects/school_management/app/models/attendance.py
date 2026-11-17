from datetime import date

from sqlalchemy import Column, Integer, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship

from database import Base
from app.models.enums import AttendanceStatus


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("school_classes.id"), nullable=False)
    attendance_date = Column(Date, default=date.today, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    recorded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    student = relationship("Student", back_populates="attendance_records")