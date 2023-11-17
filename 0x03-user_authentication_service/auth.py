#!/usr/bin/env python3
"""Auth module."""

from db import DB
from user import User
from bcrypt import hashpw, gensalt, checkpw
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes the input password using bcrypt."""
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """Generates a string representation of a new UUID."""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user."""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

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

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """Gets the user corresponding to a session ID."""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """Destroys the session for the user."""
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Get a reset password token for the user."""
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError(f"User with email {email} does not exist.")
        reset_token = self._generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user's password using reset token."""
        user = self._db.find_user_by_reset_token(reset_token)
        if not user:
            raise ValueError

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self._db.update_user_password(user.id, hashed_password)
        self._db.update_user_reset_token(user.id, None)
