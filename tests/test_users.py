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
    create_response = client.post("/api/users", json=user_payload(uid=10))
    actual_user_id = create_response.json()["user_id"]
    
    r1 = client.delete(f"/api/users/{actual_user_id}")
    assert r1.status_code == 204
    
    r2 = client.delete(f"/api/users/{actual_user_id}")
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

def test_patch_user_ok(client):
    # Create user and capture the actual ID
    create_response = client.post("/api/users", json=user_payload(uid=5))
    created_user = create_response.json()
    actual_user_id = created_user["user_id"]  # Get the real ID (probably 1, not 5)

    patch_data = {
        "first_name": "john",
        "age": 30
    }

    r = client.patch(f"/api/users/{actual_user_id}", json=patch_data)
    assert r.status_code == 200

    data = r.json()

    assert data["first_name"] == "john"
    assert data["age"] == 30

    assert data["surname"] == "OLoughlin" 
    assert data["email"] == "naoiseol123@gmail.com" 
    assert data["phoneNo"] == "0860378167" 

    def test_patch_user_404(client):
        r = client.patch("/api/users/999", json={"first_name": "Dave"})
        assert r.status_code == 404
