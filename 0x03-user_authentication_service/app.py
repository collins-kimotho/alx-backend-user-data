#!/usr/bin/env python3
"""
Flask app that returns a simple JSON response.
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


# Run the app when the script is executed
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
