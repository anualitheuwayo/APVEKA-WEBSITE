# tests/test_attendance.py
def test_teacher_can_mark_attendance_for_assigned_class(
    client, headmaster_headers, teacher_assigned_to_class_a, class_a
):
    student = client.post("/students", json={
        "admission_number": "ADM100", "full_name": "Mugisha Eric", "class_id": class_a["id"],
    }, headers=headmaster_headers).json()

    r = client.post("/attendance", json={
        "student_id": student["id"], "class_id": class_a["id"], "status": "present",
    }, headers=teacher_assigned_to_class_a)
    assert r.status_code == 201
    assert r.json()["status"] == "present"


def test_teacher_cannot_mark_attendance_for_unassigned_class(
    client, headmaster_headers, teacher_headers, class_a
):
    """teacher_headers is registered but NOT assigned to class_a — this is the core rule."""
    student = client.post("/students", json={
        "admission_number": "ADM101", "full_name": "Keza Alice", "class_id": class_a["id"],
    }, headers=headmaster_headers).json()

    r = client.post("/attendance", json={
        "student_id": student["id"], "class_id": class_a["id"], "status": "present",
    }, headers=teacher_headers)
    assert r.status_code == 403


def test_headmaster_can_mark_attendance_for_any_class(client, headmaster_headers, class_a):
    student = client.post("/students", json={
        "admission_number": "ADM102", "full_name": "Ineza Sarah", "class_id": class_a["id"],
    }, headers=headmaster_headers).json()

    r = client.post("/attendance", json={
        "student_id": student["id"], "class_id": class_a["id"], "status": "absent",
    }, headers=headmaster_headers)
    assert r.status_code == 201


def test_invalid_attendance_status_rejected(client, headmaster_headers, class_a):
    student = client.post("/students", json={
        "admission_number": "ADM103", "full_name": "Test Student", "class_id": class_a["id"],
    }, headers=headmaster_headers).json()

    r = client.post("/attendance", json={
        "student_id": student["id"], "class_id": class_a["id"], "status": "late",
    }, headers=headmaster_headers)
    assert r.status_code == 422  # "late" isn't a valid AttendanceStatus anymore — remember, we cut it down to just present/absent


def test_teacher_only_sees_attendance_for_their_own_class(
    client, headmaster_headers, teacher_assigned_to_class_a, class_a
):
    other_class = client.post("/classes", json={"name": "P2 B", "grade_level": "Primary 2"},
                               headers=headmaster_headers).json()
    other_student = client.post("/students", json={
        "admission_number": "ADM104", "full_name": "Not Mine", "class_id": other_class["id"],
    }, headers=headmaster_headers).json()
    # headmaster marks attendance in a class the teacher does NOT teach
    client.post("/attendance", json={
        "student_id": other_student["id"], "class_id": other_class["id"], "status": "present",
    }, headers=headmaster_headers)

    r = client.get("/attendance", headers=teacher_assigned_to_class_a)
    assert r.status_code == 200
    assert r.json() == []  # nothing shows up — it's not their class