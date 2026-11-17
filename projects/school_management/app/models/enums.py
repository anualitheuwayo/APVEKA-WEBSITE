
import enum


class RoleEnum(str, enum.Enum):
    headmaster = "headmaster"
    teacher = "teacher"


class AttendanceStatus(str, enum.Enum):
    present = "present"
    absent = "absent"