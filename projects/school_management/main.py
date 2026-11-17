from fastapi import FastAPI

from database import Base, engine
import app.models  

from app.routers import (
    auth_router, students_router, classes_router,
    teachers_router, attendance_router, grades_router,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="School Management API",
    description=(
        "Headmaster registers students and teachers; teachers mark attendance "
        "and record grades only for the classes they're assigned to teach."
    ),
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(students_router)
app.include_router(classes_router)
app.include_router(teachers_router)
app.include_router(attendance_router)
app.include_router(grades_router)


@app.get("/")
def root():
    return {"status": "ok", "service": "school-management-api"}