#!/usr/bin/env python3
"""
Session Authentication views.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv
from api.v1.app import auth  # Import only where needed


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login():
    """
    POST /auth_session/login: Handle session authentication login.
    """
    # Retrieve email and password from the request form
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate email
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Validate password
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for the User instance by email
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users or len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]  # Assuming email is unique

    # Validate the password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a Session ID for the User
    session_id = auth.create_session(user.id)
    if not session_id:
        abort(500)

    # Create a response with the User dictionary
    user_json = user.to_json()
    response = jsonify(user_json)

    # Set the session cookie
    session_name = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_auth_logout():
    """
    DELETE /auth_session/logout: Handle session logout.

    Returns:
        JSON response: Empty JSON dictionary with a status code of 200 on success,
                    or aborts with a 404 status code on failure.
    """
    # Attempt to destroy the session
    if not auth.destroy_session(request):
        abort(404)

    # Return an empty JSON dictionary on successful logout
    return jsonify({}), 200
