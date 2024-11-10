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
