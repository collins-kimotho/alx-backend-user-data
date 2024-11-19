#!/usr/bin/env python3
"""
Authentication module for user registration and management.
"""

from db import DB
from user import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from bcrypt import hashpw, gensalt


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize the Auth instance."""
        self._db = DB()
        # Private DB instance for interacting with the database

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        # Check if the user already exists
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User does not exist, proceed to create a new user
            hashed_password = self._hash_password(password)
            # Add the user to the database
            new_user = self._db.add_user(
                email, hashed_password.decode('utf-8'))  # Store as string
            return new_user

    def _hash_password(self, password: str) -> bytes:
        """
        Hash a password using bcrypt.

        Args:
            password (str): The password string.

        Returns:
            bytes: The hashed password.
        """
        # Convert password string to bytes
        password_bytes = password.encode('utf-8')
        salt = gensalt()  # Generate a salt
        # Hash the password with the salt
        hashed_password = hashpw(password_bytes, salt)
        return hashed_password
