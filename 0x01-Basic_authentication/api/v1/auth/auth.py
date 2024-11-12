#!/usr/bin/env python3
"""
auth.py - Authentication class template for managing API authentication

This module provides a base class for implementing various
authentication systems.
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class to manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.
        Args:
            path (str): The path to check.
            excluded_paths: A list of paths that don't require authentication.
        Returns:
            bool: False for now.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True

        # Ensure the path ends with a trailing slash for comparison consistency
        if path[-1] != '/':
            path += '/'

        # Check if the modified path is in excluded_paths
        for excluded_path in excluded_paths:
            if excluded_path[-1] != '/':
                excluded_path += '/'
            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from the request.
        Args:
            request: The Flask request object.
        Returns:
            str: None, as authorization header extraction is not implemented.
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user from the request.
        Args:
            request: The Flask request object.
        Returns:
            TypeVar('User'): None, as user extraction is not implemented.
        """
        return None
