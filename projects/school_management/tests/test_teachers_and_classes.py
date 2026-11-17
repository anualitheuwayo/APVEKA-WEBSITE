def test_headmaster_can_list_teachers(client, headmaster_headers, teacher_headers):
    r = client.get("/teachers", headers=headmaster_headers)
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["full_name"] == "Uwimana Jane"


def test_teacher_cannot_list_teachers(client, teacher_headers):
    r = client.get("/teachers", headers=teacher_headers)
    assert r.status_code == 403


def test_headmaster_can_create_class(client, headmaster_headers):
    r = client.post("/classes", json={"name": "Low A", "grade_level": "Nursery - Low"}, headers=headmaster_headers)
    assert r.status_code == 201
    assert r.json()["name"] == "Low A"


def test_duplicate_class_name_rejected(client, headmaster_headers):
    payload = {"name": "P6 A", "grade_level": "Primary 6"}
    client.post("/classes", json=payload, headers=headmaster_headers)
    r = client.post("/classes", json=payload, headers=headmaster_headers)
    assert r.status_code == 400


def test_teacher_cannot_create_class(client, teacher_headers):
    r = client.post("/classes", json={"name": "P3 A"}, headers=teacher_headers)
    assert r.status_code == 403


def test_headmaster_can_assign_teacher_to_class(client, headmaster_headers, teacher_headers, class_a):
    teachers = client.get("/teachers", headers=headmaster_headers).json()
    teacher_id = teachers[0]["id"]

    r = client.post(f"/classes/{class_a['id']}/teachers", json={"teacher_id": teacher_id}, headers=headmaster_headers)
    assert r.status_code == 201
    assert r.json()["teacher_id"] == teacher_id
    assert r.json()["class_id"] == class_a["id"]


def test_duplicate_assignment_rejected(client, headmaster_headers, teacher_headers, class_a):
    teachers = client.get("/teachers", headers=headmaster_headers).json()
    teacher_id = teachers[0]["id"]

    client.post(f"/classes/{class_a['id']}/teachers", json={"teacher_id": teacher_id}, headers=headmaster_headers)
    r = client.post(f"/classes/{class_a['id']}/teachers", json={"teacher_id": teacher_id}, headers=headmaster_headers)
    assert r.status_code == 400


def test_assigning_unknown_teacher_rejected(client, headmaster_headers, class_a):
    r = client.post(f"/classes/{class_a['id']}/teachers", json={"teacher_id": 9999}, headers=headmaster_headers)
    assert r.status_code == 404


def test_teacher_cannot_assign_teacher_to_class(client, teacher_headers, class_a):
    r = client.post(f"/classes/{class_a['id']}/teachers", json={"teacher_id": 1}, headers=teacher_headers)
    assert r.status_code == 403