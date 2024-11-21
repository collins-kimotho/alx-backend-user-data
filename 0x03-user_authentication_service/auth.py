#!/usr/bin/env python3
"""A module for authentication-related routines.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a UUID.
    Returns:
        str: A string rep of a UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Adds a new user to the database.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a user's login details are valid.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Creates a new session for a user.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieves a user based on a given session ID.
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroys a session associated with a given user.
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for a user.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password given the user's reset token.
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        new_password_hash = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )
# #!/usr/bin/env python3
# """
# Authentication module for user registration and management.
# """

# import bcrypt
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm.exc import NoResultFound
# from sqlalchemy.exc import InvalidRequestError

# from db import DB
# from user import User


# class Auth:
#     """Auth class to interact with the authentication database."""

#     def __init__(self):
#         """Initialize the Auth instance."""
#         self._db = DB()
#         # Private DB instance for interacting with the database

#     def register_user(self, email: str, password: str) -> User:
#         """
#         Register a new user with email and password.

#         Args:
#             email (str): The user's email.
#             password (str): The user's password.

#         Returns:
#             User: The created User object.

#         Raises:
#             ValueError: If a user with the given email already exists.
#         """
#         # Check if the user already exists
#         # try:
#         #     self._db.find_user_by(email=email)
#         #     raise ValueError(f"User {email} already exists")
#         # except NoResultFound:
#         #     # User does not exist, proceed to create a new user
#         #     hashed_password = self._hash_password(password)
#         #     # Add the user to the database
#         #     new_user = self._db.add_user(
#         #         email, hashed_password.decode('utf-8'))  # Store as string
#         # return new_user
#         # """Adds a new user to the database.
#         # """
#         try:
#             self._db.find_user_by(email=email)
#         except NoResultFound:
#             return self._db.add_user(email, _hash_password(password))
#         raise ValueError("User {} already exists".format(email))

#     def _hash_password(self, password: str) -> bytes:
#         """
#         Hash a password using bcrypt.

#         Args:
#             password (str): The password string.

#         Returns:
#             bytes: The hashed password.
#         """
#         # Convert password string to bytes
#         password_bytes = password.encode('utf-8')
#         salt = bcrypt.gensalt()  # Generate a salt
#         # Hash the password with the salt
#         hashed_password = bcrypt.hashpw(password_bytes, salt)
#         return hashed_password
