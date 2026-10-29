
def test_valid_url_submission_is_saved_and_displayed(client):
    payload = {
        "student_name": "Ali Khan",
        "registration_number": "FA22-BCS-001",
        "assignment_title": "Cloud Computing Assignment",
        "submission_url": "https://github.com/example/assignment",
    }

    response = client.post("/api/url-submissions/", json=payload)

    assert response.status_code == 201, response.text
    saved = response.json()

    assert saved["student_name"] == payload["student_name"]
    assert saved["registration_number"] == payload["registration_number"]
    assert saved["assignment_title"] == payload["assignment_title"]
    assert saved["submission_url"] == payload["submission_url"]

    list_response = client.get("/api/url-submissions/")

    assert list_response.status_code == 200, list_response.text
    submissions = list_response.json()

    assert len(submissions) == 1
    assert submissions[0]["registration_number"] == "FA22-BCS-001"


def test_missing_registration_number_is_rejected(client):
    payload = {
        "student_name": "Ali Khan",
        "registration_number": "",
        "assignment_title": "Cloud Computing Assignment",
        "submission_url": "https://github.com/example/assignment",
    }

    response = client.post("/api/url-submissions/", json=payload)

    assert response.status_code == 422
    assert client.get("/api/url-submissions/").json() == []


def test_invalid_submission_url_is_rejected(client):
    payload = {
        "student_name": "Ali Khan",
        "registration_number": "FA22-BCS-001",
        "assignment_title": "Cloud Computing Assignment",
        "submission_url": "not-a-valid-url",
    }

    response = client.post("/api/url-submissions/", json=payload)

    assert response.status_code == 422
    assert client.get("/api/url-submissions/").json() == []
