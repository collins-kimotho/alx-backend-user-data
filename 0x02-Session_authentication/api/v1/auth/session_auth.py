#!/usr/bin/env python3
"""
Session authentication module.
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    Implements session-based authentication.
    """
    # Class attribute to store user_id mapped by session_id
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a new session ID for the given user ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The generated session ID, or None if user_id is invalid.
        """
        # Validate that user_id is not None and is a string
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a unique session ID using uuid4
        session_id = str(uuid.uuid4())

        # Map the session ID to the user ID in the dictionary
        self.user_id_by_session_id[session_id] = user_id

        # Return the generated session ID
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves a user ID based on the given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID,
            or None if invalid.
        """
        # Validate that session_id is not None and is a string
        if session_id is None or not isinstance(session_id, str):
            return None

        # Use .get() to retrieve the user ID from the dictionary
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieve a User instance based on a cookie value.

        - Get the session cookie value using `self.session_cookie(request)`.
        - Retrieve the User ID using `self.user_id_for_session_id`.
        - Return the User instance using `User.get`.
        """
        if request is None:
            return None

        # Get the session cookie value
        session_id = self.session_cookie(request)
        if not session_id:
            return None

        # Get the User ID for the session ID
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        # Retrieve and return the User instance
        return User.get(user_id)
