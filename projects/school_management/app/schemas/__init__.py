from app.schemas.user import UserCreate, UserOut, Token, LoginRequest
from app.schemas.teacher import TeacherOut
from app.schemas.school_class import (
    SchoolClassCreate, SchoolClassUpdate, SchoolClassOut,
    TeacherAssignmentCreate, ClassAssignmentOut,
)
from app.schemas.student import StudentCreate, StudentUpdate, StudentOut
from app.schemas.attendance import AttendanceCreate, AttendanceOut
from app.schemas.grade import GradeCreate, GradeOut