#!/usr/bin/env python3
"""
DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


from user import Base, User


class DB:
    """DB class for managing the database."""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)  # Drop all tables (testing)
        Base.metadata.create_all(self._engine)  # Create all tables
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The created user object.
        """
        # Create a new User instance
        new_user = User(email=email, hashed_password=hashed_password)

        # Add the new user to the session
        self._session.add(new_user)

        # Commit the transaction to persist changes to the database
        self._session.commit()

        # Return the newly created User object
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database using arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering.

        Returns:
            User: The first matching user.

        Raises:
            NoResultFound: If no user matches the criteria.
            InvalidRequestError: If the query arguments are invalid.
        """
        # if not kwargs:
        #     raise InvalidRequestError("No query arguments provided")

        # # Query the database with the provided filters
        # try:
        #     user = self._session.query(User).filter_by(**kwargs).first()
        #     if not user:
        #         raise NoResultFound("No user found matching the criteria")
        #     return user
        # except AttributeError as e:
        #     # Raised when the query uses invalid attributes
        #     raise InvalidRequestError(f"Invalid query argument: {e}")
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        result = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if result is None:
            raise NoResultFound()
        return result
