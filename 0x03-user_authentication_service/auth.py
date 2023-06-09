#!/usr/bin/env python3
"""Auth module
"""

from db import DB
from user import User
from bcrypt import hashpw, gensalt, checkpw
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hashes the input password using bcrypt

    Args:
        password: Input password string

    Returns:
        Salted hash of the input password as bytes
    """
    encoded_password = password.encode('utf-8')
    salt = gensalt()
    hashed_password = hashpw(encoded_password, salt)
    return hashed_password


def _generate_uuid(self) -> str:
        """Generates a string representation of a new UUID."""
        return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.
        Args:
            email: Email of the user
            password: Password of the user

        Returns:
            User object of the newly registered user

        Raises:
            ValueError: If a user already exists with the given email
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if login credentials are valid."""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a new session for the user."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return
