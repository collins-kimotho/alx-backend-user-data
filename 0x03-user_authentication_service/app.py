#!/usr/bin/env python3
"""
Flask app that returns a simple JSON response.
Flask app with user authentication features.
"""

from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

# Initialize the Flask app
app = Flask(__name__)
AUTH = Auth()


#  Define the route for the home page
@app.route('/', methods=['GET'])
def home():
    """Return a simple JSON response."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
    POST /users endpoint for user registration

    Expects form data:
        - email: The user's email
        - password: The user's password
    Returns:
        - On SUccess: JSON payload
        - On failure: JSON payload and 400 status code
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({
            "message": "email and password are requred"
        }), 400

    try:
        # Register the user
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        # Handle duplicate email registration
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """
    POST /sessions route to log in a user.
    Expects form data with "email" and "password".
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(401)  # Invalid request if email or password is missing.

    if not AUTH.valid_login(email, password):
        abort(401)  # Invalid login credentials.

    # Create a new session.
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)  # Abort if the session could not be created.

    # Set session_id in a cookie and return a JSON response.
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/profile', methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    GET /profile route to fetch the user's email based on their session_id.
    Expects "session_id" in the request cookies.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_passsword_token() -> str:
    """
    POST /reset_password
    Request form data should contain email
    Respond with a reset token if the email exists
    """
    email = request.form.get("email")
    if not email:
        abort(400)

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    Update a user's pw using their reset token.
    Responds to PUT /reset_password.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(400)

    try:
        # Attempt to update the user's pw
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


# Run the app when the script is executed
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
