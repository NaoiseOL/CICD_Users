import pytest

def user_payload(uid=1, first_name="Naoise", surname="OLoughlin", age=25, email="naoiseol123@gmail.com", phoneNo="0860378167",booking_number="01"):
    return {"user_id":uid, "first_name":first_name, "surname":surname, "age": age, "email":email, "phoneNo":phoneNo,"booking_number":booking_number}

def test_create_user_ok(client):
    r = client.post("/api/users", json=user_payload())
    assert r.status_code == 201
    data = r.json()
    assert data["user_id"] == 1
    assert data["first_name"] == "Naoise"

def test_duplicate_user_id_conflict(client):
    client.post("/api/users", json=user_payload(uid=2))
    r = client.post("/api/users", json=user_payload(uid=2))
    assert r.status_code == 409 # duplicate id -> conflict
    assert "exists" in r.json()["detail"].lower()

def test_get_user_404(client):
    r = client.get("/api/users/999")
    assert r.status_code == 404

def test_delete_then_404(client):
    client.post("/api/users", json=user_payload(uid=10))
    r1 = client.delete("/api/users/10")
    assert r1.status_code == 204
    r2 = client.delete("/api/users/10")
    assert r2.status_code == 404

def test_put_OK(client):
    client.post("/api/users", json=user_payload(uid=1))

    r = client.put("/api/users/1", json=user_payload(uid=1, first_name="Noah", email="naoiseol@atu.ie", age=24))

    assert r.status_code == 200
    data=r.json()

    assert data["user_id"] == 1
    assert data["first_name"] == "Noah"
    assert data["email"] == "naoiseol@atu.ie"
    assert data["age"] == 24

def test_put_404(client):
    r = client.put("/api/users/999", json=user_payload(uid=1, first_name="Naoise", email="naoise@atu.ie", age=25))

    assert r.status_code == 404