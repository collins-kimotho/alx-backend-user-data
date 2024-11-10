#!/usr/bin/env python3
"""
This module provides a function to hash passwords using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with a unique salt using bcrypt
    and returns the hashed password.
    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: A byte string representing the salted, hashed password.
    """
    # Generate a salt using bcrypt,
    # which includes 12 rounds for security by default.
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    # and return the hashed result as bytes.
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if a given password matches the hashed password using bcrypt.
    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The plain password to verify.
    Returns:
        bool:
        True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
