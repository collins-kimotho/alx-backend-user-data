#!/usr/bin/env python3
"""
Authentication module for password hashing.
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash a password with bcrypt and return the salted hash.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt
    salt = bcrypt.gensalt()

    # Generate the salted hash
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password
