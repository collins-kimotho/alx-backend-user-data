#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

# Import Auth and BasicAuth
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize `auth` based on `AUTH_TYPE`
auth = None
auth_type = getenv("AUTH_TYPE")
if auth_type == "auth":
    auth = Auth()
if auth_type == 'basic_auth':
    auth = BasicAuth()
if auth_type == 'session_auth':
    auth = SessionAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.before_request
def before_request():
    """
    Handle tasks before processing the request.
    """
    if auth:
        # Skip authentication for specific endpoints
        excluded_paths = ['/api/v1/status/',
                          '/api/v1/unauthorized/',
                          '/api/v1/forbidden/',
                          '/api/v1/auth_session/login/']
        if not auth.require_auth(request.path, excluded_paths):
            return
        if not auth.authorization_header(request) and \
                not auth.session_cookie(request):
            return jsonify({"error": "Unauthorized"}), 401
        user = auth.current_user(request)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
        request.current_user = user  # Assign authenticated user to request


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
