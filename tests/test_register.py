
def test_success_register(client):
    payload = {
        "login": "alice",
        "username": "Alice",
        "email": "a@example.com",
        "password": "secret"
    }
    resp = client.post("/auth/registry", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "Alice"

def test_duplicate_login(client):
    payload = {
        "login": "mark",
        "username": "Mark",
        "email": "m@example.com",
        "password": "secret"
    }
    # первая регистрация
    resp1 = client.post("/auth/registry", json=payload)
    assert resp1.status_code == 200

    # вторая — конфликт
    resp2 = client.post("/auth/registry", json=payload)
    assert resp2.status_code == 409            
