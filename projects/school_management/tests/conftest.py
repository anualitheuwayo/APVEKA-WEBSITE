
import os
import sys

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
import app.models  # noqa: F401 — registers every table on Base.metadata
from main import app as fastapi_app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # keeps the SAME in-memory DB alive across connections
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    fastapi_app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient
    with TestClient(fastapi_app) as test_client:
        yield test_client

    fastapi_app.dependency_overrides.clear()


@pytest.fixture()
def headmaster_headers(client):
    client.post("/auth/bootstrap-headmaster", json={
        "username": "head1", "email": "head@school.com", "password": "pass123", "role": "headmaster",
    })
    r = client.post("/auth/login", json={"username": "head1", "password": "pass123"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def class_a(client, headmaster_headers):
    r = client.post("/classes", json={"name": "P1 A", "grade_level": "Primary 1"}, headers=headmaster_headers)
    return r.json()


@pytest.fixture()
def teacher_headers(client, headmaster_headers):
    """A teacher account, registered by the headmaster, not yet assigned to any class."""
    client.post("/auth/register", json={
        "username": "teacher1", "email": "t1@school.com", "password": "pass123",
        "role": "teacher", "full_name": "Uwimana Jane", "subject_specialty": "Mathematics",
    }, headers=headmaster_headers)
    r = client.post("/auth/login", json={"username": "teacher1", "password": "pass123"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def teacher_assigned_to_class_a(client, headmaster_headers, teacher_headers, class_a):
    """Same teacher as teacher_headers, but now actually assigned to teach class_a."""
    teachers = client.get("/teachers", headers=headmaster_headers).json()
    teacher_id = next(t["id"] for t in teachers if t["full_name"] == "Uwimana Jane")
    client.post(f"/classes/{class_a['id']}/teachers", json={"teacher_id": teacher_id}, headers=headmaster_headers)
    return teacher_headers