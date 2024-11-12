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
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from the request.
        Args:
            request: The Flask request object.
        Returns:
            str: None, as authorization header extraction is not implemented.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user from the request.
        Args:
            request: The Flask request object.
        Returns:
            TypeVar('User'): None, as user extraction is not implemented.
        """
        return None
