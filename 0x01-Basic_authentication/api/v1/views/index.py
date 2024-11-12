#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> None:
    """
    Test endpoint that raises a 401 Unauthorized error.
        By calling this endpoint, it triggers the 401 error handler.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app_views.route('forbidden', strict_slashes=False)
def forbidden() -> None:
    """
    Custom error handler for 403 Forbidden status code.
        Args:
        error (Forbidden): The 403 error that was raised.
            Returns:
        Tuple[Response, int]: JSON response with error message&status code403.
    """
    return jsonify({"error": "Forbidden"}), 403
