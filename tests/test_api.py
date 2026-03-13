import requests

BASE_URL = "http://127.0.0.1:5000"
token = None

def test_health_check():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    assert r.json()['status'] == 'healthy'


def test_login_success():
    global token
    r = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "admin",
        "password": "Admin@1234"
    })
    assert r.status_code == 200
    assert 'token' in r.json()
    token = r.json()['token']


def test_login_fail():
    r = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "admin",
        "password": "wrongpassword"
    })
    assert r.status_code == 401


def test_get_employees_without_token():
    r = requests.get(f"{BASE_URL}/employees/")
    assert r.status_code == 401


def test_get_employees_with_token():
    r = requests.get(
        f"{BASE_URL}/employees/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 200


def test_analytics_headcount():
    r = requests.get(
        f"{BASE_URL}/analytics/headcount",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 200