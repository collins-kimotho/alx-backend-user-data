#!/usr/bin/env python3
"""
User model definition using SQLAlchemy
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for our models
Base = declarative_base()


class User(Base):
    """
    User model for the `users` table.
    Attributes:
        id (int): Primary key of the table.
        email (str): Non-nullable column for user email.
        hashed_password (str): Non-nullable column for the hashed password.
        session_id (str): Nullable column for session ID.
        reset_token (str): Nullable column for reset token.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
