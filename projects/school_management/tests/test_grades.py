# tests/test_grades.py
def test_teacher_can_record_grade_for_assigned_class(
    client, headmaster_headers, teacher_assigned_to_class_a, class_a
):
    student = client.post("/students", json={
        "admission_number": "ADM200", "full_name": "Mutoni Grace", "class_id": class_a["id"],
    }, headers=headmaster_headers).json()

    r = client.post("/grades", json={
        "student_id": student["id"], "subject": "Mathematics", "term": "Term 1 2026", "score": 78,
    }, headers=teacher_assigned_to_class_a)
    assert r.status_code == 201
    assert r.json()["score"] == 78
    assert r.json()["max_score"] == 100.0  # default, since we didn't send one


def test_teacher_cannot_record_grade_for_unassigned_class(
    client, headmaster_headers, teacher_headers, class_a
):
    """teacher_headers is registered but NOT assigned to class_a."""
    student = client.post("/students", json={
        "admission_number": "ADM201", "full_name": "Habimana Eric", "class_id": class_a["id"],
    }, headers=headmaster_headers).json()

    r = client.post("/grades", json={
        "student_id": student["id"], "subject": "English", "term": "Term 1 2026", "score": 60,
    }, headers=teacher_headers)
    assert r.status_code == 403


def test_recording_grade_for_unknown_student_rejected(client, teacher_assigned_to_class_a):
    r = client.post("/grades", json={
        "student_id": 9999, "subject": "Science", "term": "Term 1 2026", "score": 50,
    }, headers=teacher_assigned_to_class_a)
    assert r.status_code == 404


def test_headmaster_can_record_grade_for_any_student(client, headmaster_headers, class_a):
    student = client.post("/students", json={
        "admission_number": "ADM202", "full_name": "Niyonzima Paul", "class_id": class_a["id"],
    }, headers=headmaster_headers).json()

    r = client.post("/grades", json={
        "student_id": student["id"], "subject": "Kinyarwanda", "term": "Term 1 2026", "score": 88,
    }, headers=headmaster_headers)
    assert r.status_code == 201


def test_teacher_only_sees_grades_for_their_own_class(
    client, headmaster_headers, teacher_assigned_to_class_a, class_a
):
    other_class = client.post("/classes", json={"name": "P3 A", "grade_level": "Primary 3"},
                               headers=headmaster_headers).json()
    other_student = client.post("/students", json={
        "admission_number": "ADM203", "full_name": "Not Mine", "class_id": other_class["id"],
    }, headers=headmaster_headers).json()
    # headmaster records a grade for a student OUTSIDE the teacher's class
    client.post("/grades", json={
        "student_id": other_student["id"], "subject": "Science", "term": "Term 1 2026", "score": 70,
    }, headers=headmaster_headers)

    r = client.get("/grades", headers=teacher_assigned_to_class_a)
    assert r.status_code == 200
    assert r.json() == []  # nothing shows up — that student isn't in their class


def test_student_moving_class_does_not_retroactively_grant_grade_access(
    client, headmaster_headers, teacher_assigned_to_class_a, class_a
):
    """
    This is the specific edge case that makes Grade -> Student -> class_id
    (rather than storing class_id directly) worth testing carefully:
    if a student's class_id changes AFTER a grade was recorded, does the
    join-based permission check use their CURRENT class, correctly?
    """
    student = client.post("/students", json={
        "admission_number": "ADM204", "full_name": "Uwera Diane", "class_id": class_a["id"],
    }, headers=headmaster_headers).json()

    # recorded while still in class_a — teacher can see it
    client.post("/grades", json={
        "student_id": student["id"], "subject": "Mathematics", "term": "Term 1 2026", "score": 65,
    }, headers=teacher_assigned_to_class_a)

    # now move the student to a different class the teacher does NOT teach
    other_class = client.post("/classes", json={"name": "P4 A", "grade_level": "Primary 4"},
                               headers=headmaster_headers).json()
    client.put(f"/students/{student['id']}", json={"class_id": other_class["id"]}, headers=headmaster_headers)

    # the teacher should no longer see this student's grade at all
    r = client.get("/grades", headers=teacher_assigned_to_class_a)
    assert r.status_code == 200
    assert r.json() == []