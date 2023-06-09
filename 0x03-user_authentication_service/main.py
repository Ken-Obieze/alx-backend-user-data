#!/usr/bin/env python3
"""Main Module"""

import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

BASE_URL = "http://localhost:5000"

def register_user(email: str, password: str) -> None:
    url = f"{BASE_URL}/users"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 201, f"Registration failed with status code {response.status_code}"

def log_in_wrong_password(email: str, password: str) -> None:
    url = f"{BASE_URL}/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 401, f"Login with wrong password failed with status code {response.status_code}"

def log_in(email: str, password: str) -> str:
    url = f"{BASE_URL}/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 200, f"Login failed with status code {response.status_code}"
    return response.cookies.get("session_id")

def profile_unlogged() -> None:
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403, f"Profile access without session ID failed with status code {response.status_code}"

def profile_logged(session_id: str) -> None:
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200, f"Profile access with session ID failed with status code {response.status_code}"
    payload = response.json()
    assert payload["email"] == EMAIL, f"Profile access returned incorrect email: {payload['email']}"

def log_out(session_id: str) -> None:
    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200, f"Logout failed with status code {response.status_code}"

def reset_password_token(email: str) -> str:
    url = f"{BASE_URL}/reset_password"
    payload = {"email": email}
    response = requests.post(url, data=payload)
    assert response.status_code == 200, f"Reset password token request failed with status code {response.status_code}"
    payload = response.json()
    return payload["reset_token"]

def update_password(email: str, reset_token: str, new_password: str) -> None:
    url = f"{BASE_URL}/reset_password"
    payload = {"email": email, "reset_token": reset_token, "new_password": new_password}
    response = requests.put(url, data=payload)
    assert response.status_code == 200, f"Update password failed with status code {response.status_code}"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password
