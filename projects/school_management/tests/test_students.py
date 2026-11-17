def test_headmaster_can_register_student(client, headmaster_headers, class_a):
    r = client.post("/students", json={
        "admission_number": "ADM001", "full_name": "Iradukunda John", "class_id": class_a["id"],
    }, headers=headmaster_headers)
    assert r.status_code == 201
    assert r.json()["admission_number"] == "ADM001"


def test_duplicate_admission_number_rejected(client, headmaster_headers, class_a):
    payload = {"admission_number": "ADM001", "full_name": "Iradukunda John", "class_id": class_a["id"]}
    client.post("/students", json=payload, headers=headmaster_headers)
    r = client.post("/students", json=payload, headers=headmaster_headers)
    assert r.status_code == 400


def test_registering_student_with_unknown_class_rejected(client, headmaster_headers):
    r = client.post("/students", json={
        "admission_number": "ADM002", "full_name": "Uwase Grace", "class_id": 9999,
    }, headers=headmaster_headers)
    assert r.status_code == 404


def test_teacher_cannot_register_student(client, teacher_headers):
    r = client.post("/students", json={"admission_number": "ADM003", "full_name": "X"}, headers=teacher_headers)
    assert r.status_code == 403


def test_teacher_with_no_assignment_sees_no_students(client, headmaster_headers, teacher_headers, class_a):
    client.post("/students", json={
        "admission_number": "ADM004", "full_name": "In Class A", "class_id": class_a["id"],
    }, headers=headmaster_headers)

    r = client.get("/students", headers=teacher_headers)
    assert r.status_code == 200
    assert r.json() == [] 


def test_teacher_sees_only_students_in_assigned_class(
    client, headmaster_headers, teacher_assigned_to_class_a, class_a
):
    other_class = client.post("/classes", json={"name": "P2 A", "grade_level": "Primary 2"},
                               headers=headmaster_headers).json()

    client.post("/students", json={
        "admission_number": "ADM005", "full_name": "In Class A", "class_id": class_a["id"],
    }, headers=headmaster_headers)
    client.post("/students", json={
        "admission_number": "ADM006", "full_name": "In Class Other", "class_id": other_class["id"],
    }, headers=headmaster_headers)

    r = client.get("/students", headers=teacher_assigned_to_class_a)
    assert r.status_code == 200
    names = [s["full_name"] for s in r.json()]
    assert names == ["In Class A"] 


def test_headmaster_sees_all_students(client, headmaster_headers, class_a):
    client.post("/students", json={
        "admission_number": "ADM007", "full_name": "Student One", "class_id": class_a["id"],
    }, headers=headmaster_headers)
    client.post("/students", json={
        "admission_number": "ADM008", "full_name": "Student Two",
    }, headers=headmaster_headers)  

    r = client.get("/students", headers=headmaster_headers)
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_teacher_gets_403_viewing_student_outside_their_class(
    client, headmaster_headers, teacher_assigned_to_class_a
):
    other_class = client.post("/classes", json={"name": "P2 A", "grade_level": "Primary 2"},
                               headers=headmaster_headers).json()
    other_student = client.post("/students", json={
        "admission_number": "ADM009", "full_name": "Not Mine", "class_id": other_class["id"],
    }, headers=headmaster_headers).json()

    r = client.get(f"/students/{other_student['id']}", headers=teacher_assigned_to_class_a)
    assert r.status_code == 403