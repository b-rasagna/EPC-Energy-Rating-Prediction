from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/login",
        data={"username": "admin", "password": "pass123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_fail():
    response = client.post(
        "/login",
        data={"username": "admin", "password": "wrong"}
    )
    assert response.status_code == 401

def test_select_model_and_predict_by_lmk():
    # Login
    login = client.post(
        "/login",
        data={"username": "admin", "password": "pass123"}
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Select model
    select = client.post(
        "/select_model",
        json={"model_name": "Random Forest"},
        headers=headers
    )
    assert select.status_code == 200

    # Predict by LMK_KEY
    predict = client.post(
        "/predict/by-lmk",
        json={"lmk_key": "1795390458252020032613265028200560"},
        headers=headers
    )
    assert predict.status_code == 200
    response_json = predict.json()
    assert "predicted_rating_letter" in response_json
    assert "predicted_potential_energy_rating" in response_json

def test_predict_by_address():
    login = client.post(
        "/login",
        data={"username": "admin", "password": "pass123"}
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/select_model",
        json={"model_name": "Random Forest"},
        headers=headers
    )

    predict = client.post(
        "/predict/by-address",
        json={"address": "36, Lea Hall Green, B20 2AW"},
        headers=headers
    )
    assert predict.status_code == 200
    result = predict.json()
    assert "predicted_rating_letter" in result
    assert "predicted_potential_energy_rating" in result
