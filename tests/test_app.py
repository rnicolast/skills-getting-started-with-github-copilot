def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # there should be a few named activities
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success(client):
    email = "newstudent@mergington.edu"
    resp = client.post("/activities/Chess Club/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in client.get("/activities").json()["Chess Club"]["participants"]


def test_signup_nonexistent(client):
    resp = client.post("/activities/Nonexistent/signup", params={"email": "foo@bar"})
    assert resp.status_code == 404


def test_signup_duplicate(client):
    existing = "michael@mergington.edu"
    resp = client.post("/activities/Chess Club/signup", params={"email": existing})
    assert resp.status_code == 400


def test_unregister_success(client):
    email = "daniel@mergington.edu"
    # make sure it's there first
    assert email in client.get("/activities").json()["Chess Club"]["participants"]
    resp = client.post("/activities/Chess Club/unregister", params={"email": email})
    assert resp.status_code == 200
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]


def test_unregister_nonexistent_activity(client):
    resp = client.post("/activities/Nope/unregister", params={"email": "foo@bar"})
    assert resp.status_code == 404


def test_unregister_not_signed_up(client):
    resp = client.post("/activities/Chess Club/unregister", params={"email": "nobody@nowhere"})
    assert resp.status_code == 400
