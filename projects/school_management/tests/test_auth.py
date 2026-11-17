def test_bootstrap_creates_first_headmaster(client):
    r = client.post("/auth/bootstrap-headmaster", json={
        "username": "head1", "email": "head@school.com", "password": "pass123", "role": "headmaster",
    })
    assert r.status_code == 201
    assert r.json()["role"] == "headmaster"


def test_bootstrap_locks_itself_after_first_headmaster(client, headmaster_headers):
    r = client.post("/auth/bootstrap-headmaster", json={
        "username": "head2", "email": "head2@school.com", "password": "pass123", "role": "headmaster",
    })
    assert r.status_code == 403


def test_login_wrong_password_rejected(client, headmaster_headers):
    r = client.post("/auth/login", json={"username": "head1", "password": "wrong"})
    assert r.status_code == 401


def test_login_returns_bearer_token(client, headmaster_headers):
    r = client.post("/auth/login", json={"username": "head1", "password": "pass123"})
    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer"
    assert "access_token" in r.json()


def test_headmaster_can_register_teacher(client, headmaster_headers):
    r = client.post("/auth/register", json={
        "username": "teacher1", "email": "t1@school.com", "password": "pass123",
        "role": "teacher", "full_name": "Uwimana Jane",
    }, headers=headmaster_headers)
    assert r.status_code == 201
    assert r.json()["role"] == "teacher"


def test_registering_teacher_without_full_name_rejected(client, headmaster_headers):
    r = client.post("/auth/register", json={
        "username": "teacher2", "email": "t2@school.com", "password": "pass123", "role": "teacher",
    }, headers=headmaster_headers)
    assert r.status_code == 400


def test_teacher_cannot_register_another_user(client, teacher_headers):
    r = client.post("/auth/register", json={
        "username": "teacher2", "email": "t2@school.com", "password": "pass123", "role": "teacher",
    }, headers=teacher_headers)
    assert r.status_code == 403


def test_unauthenticated_request_rejected(client):
    r = client.get("/auth/me")
    assert r.status_code == 401  