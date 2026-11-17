# School Management API

A FastAPI-based school management system for managing users, classes, attendance, and grades.

## Features

- **Authentication**: JWT-based login with role-based access control
- **Roles**: `headmaster` and `teacher`
- **Users**: Headmaster registers students and teachers
- **Classes**: Create and manage school classes/sections
- **Class Assignments**: Assign teachers to classes they teach
- **Attendance**: Teachers mark attendance only for classes they're assigned to
- **Grades**: Record and manage student grades

## Authentication Flow

1. **First headmaster**: `POST /auth/bootstrap-headmaster` (no auth required) — creates the initial headmaster account
2. **Login**: `POST /auth/login` — returns a JWT access token
3. **Register users**: `POST /auth/register` — headmaster-only endpoint to create student/teacher accounts

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [PostgreSQL](https://www.postgresql.org/) — database
- [Pydantic](https://docs.pydantic.dev/) — data validation
- [python-jose](https://github.com/mpdavis/python-jose) — JWT handling
- [passlib](https://passlib.readthedocs.io/) — password hashing (bcrypt)
- [python-dotenv](https://pypi.org/project/python-dotenv/) — environment variables

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/schoolmanagement_db
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

`.env` is gitignored — never commit secrets.

## Project Structure

```
app/
  core/           # security (password hashing, JWT) and dependencies
  models/         # SQLAlchemy models (User, Teacher, SchoolClass, ClassAssignment, Attendance, Grade)
  repositories/   # data access layer
  routers/        # API route handlers (auth, students, classes, teachers, attendance, grades)
  schemas/        # Pydantic request/response schemas
  services/       # business logic
tests/            # pytest test suite
database.py       # database engine and session setup
main.py           # FastAPI application entry point
requirements.txt  # Python dependencies
```

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and secret key
   ```

3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

4. Visit `http://localhost:8000/docs` for the interactive API documentation.

## License

MIT