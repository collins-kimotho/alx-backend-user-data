#!/usr/bin/env python3
"""
BasicAuth module
"""
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth.
    Currently empty; functionality will be added later.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic Auth.
        Args:
            authorization_header (str): The value of the Authorization header.
        Returns:
            str: The Base64-encoded part of the header after 'Basic '.
            None: If the header is not in the correct format or is invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 part of the Authorization header.

        Args:
            base64_authorization_header (str): The Base64 string to decode.

        Returns:
            str: The decoded UTF-8 string.
            None: If the input is invalid or decoding fails.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # Decode the Base64 string to bytes, then decode bytes to UTF-8
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user email and password from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header: The decoded Base64 string.

        Returns:
            tuple: (user_email, user_password) if the input is valid.
            (None, None): if the input is invalid or doesn't contain a colon.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the string on the first occurrence of ':'
        user_email, user_password = decoded_base64_authorization_header.split(
            ":", 1)
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns a User instance based on email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: The authenticated User instance,
            or None if authentication fails.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user by email
        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]  # Assuming there is only one user with a unique email

        # Verify if the password matches
        if not user.is_valid_password(user_pwd):
            return None

        return user

        def user_object_from_credentials(
                self, user_email: str, user_pwd: str) -> TypeVar('User'):
            """
            Returns a User instance based on email and password.
            Args:
                user_email (str): The user's email.
                user_pwd (str): The user's password.
            Returns:
                User: The authenticated User instance,
                or None if authentication fails.
            """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user by email
        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]  # Assuming there is only one user with a unique email

        # Verify if the password matches
        if not user.is_valid_password(user_pwd):
            return None

        return user

        # if type(user_email) == str and type(user_pwd) == str:
        #         users = User.search({'email': user_email})
        #     except Exception:
        #         return None
        #     if len(users) <= 0:
        #         return None
        #     if users[0].is_valid_password(user_pwd):
        #         return users[0]
        # return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request based on BasicAuthentication.

        Args:
            request (flask.Request): The incoming HTTP request.

        Returns:
            User: The User instance associated with the provided credentials,
                  or None if authentication fails.
        """
        # # Step 1: Get authorization header
        # auth_header = self.authorization_header(request)
        # if auth_header is None:
        #     return None

        # # Step 2: Extract the Base64 part
        # base64_auth_header = self.extract_base64_authorization_header(
        #     auth_header)
        # if base64_auth_header is None:
        #     return None

        # # Step 3: Decode the Base64 part
        # decoded_auth_header = self.decode_base64_authorization_header(
        #     base64_auth_header)
        # if decoded_auth_header is None:
        #     return None

        # # Step 4: Extract user credentials
        # user_email, user_pwd = self.extract_user_credentials(
        #     decoded_auth_header)
        # if user_email is None or user_pwd is None:
        #     return None

        # # Step 5: Retrieve User instance using credentials
        # return self.user_object_from_credentials(user_email, user_pwd)

        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
