import requests

BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """Registers a new user."""
    response = requests.post("{}/users".format(BASE_URL), data={"email": email, "password": password})
    assert response.status_code == 200, "Unexpected status code: {}".format(response.status_code)
    assert response.json() == {"email": email, "message": "user created"}, "Unexpected response: {}".format(response.json())


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempts to log in with an incorrect password."""
    response = requests.post("{}/sessions".format(BASE_URL), data={"email": email, "password": password})
    assert response.status_code == 401, "Unexpected status code: {}".format(response.status_code)


def log_in(email: str, password: str) -> str:
    """Logs in with valid credentials and returns the session ID."""
    response = requests.post("{}/sessions".format(BASE_URL), data={"email": email, "password": password})
    assert response.status_code == 200, "Unexpected status code: {}".format(response.status_code)
    session_id = response.cookies.get("session_id")
    assert session_id is not None, "Session ID not found in cookies"
    return session_id


def profile_unlogged() -> None:
    """Attempts to access the profile endpoint without being logged in."""
    response = requests.get("{}/profile".format(BASE_URL))
    assert response.status_code == 403, "Unexpected status code: {}".format(response.status_code)


def profile_logged(session_id: str) -> None:
    """Accesses the profile endpoint with a valid session ID."""
    response = requests.get("{}/profile".format(BASE_URL), cookies={"session_id": session_id})
    assert response.status_code == 200, "Unexpected status code: {}".format(response.status_code)
    assert "email" in response.json(), "Unexpected response: {}".format(response.json())


def log_out(session_id: str) -> None:
    """Logs out by invalidating the session ID."""
    response = requests.delete("{}/sessions".format(BASE_URL), cookies={"session_id": session_id})
    assert response.status_code == 200, "Unexpected status code: {}".format(response.status_code)
    assert response.json() == {"message": "session deleted"}, "Unexpected response: {}".format(response.json())


def reset_password_token(email: str) -> str:
    """Requests a password reset token."""
    response = requests.post("{}/reset_password".format(BASE_URL), data={"email": email})
    assert response.status_code == 200, "Unexpected status code: {}".format(response.status_code)
    reset_token = response.json().get("reset_token")
    assert reset_token is not None, "Reset token not found in response"
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Updates the password using a reset token."""
    response = requests.put(
        "{}/reset_password".format(BASE_URL),
        data={"email": email, "reset_token": reset_token, "new_password": new_password},
    )
    assert response.status_code == 200, "Unexpected status code: {}".format(response.status_code)
    assert response.json() == {"email": email, "message": "Password updated"}, "Unexpected response: {}".format(response.json())


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
