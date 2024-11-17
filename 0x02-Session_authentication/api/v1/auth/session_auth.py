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
