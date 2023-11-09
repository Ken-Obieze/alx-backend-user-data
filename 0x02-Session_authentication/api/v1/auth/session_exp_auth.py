#!/usr/bin/env python3
"""Session Expiration module for the API."""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta

class SessionExpAuth(SessionAuth):
    def __init__(self):
        super().__init__()
        # Set session_duration from environment variable or default to 0
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        # Call create_session method of the parent class
        session_id = super().create_session(user_id)

        if session_id:
            # Create session dictionary
            session_dict = {
                "user_id": user_id,
                "created_at": datetime.now()
            }

            # Add session dictionary to user_id_by_session_id dictionary
            self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        # Return None if session_id is None
        if session_id is None:
            return None

        # Return None if session_id is not in user_id_by_session_id
        if session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]

        # Return user_id if session_duration is 0 or negative
        if self.session_duration <= 0:
            return session_dict["user_id"]

        # Return None if created_at is not in session_dict
        if "created_at" not in session_dict:
            return None

        # Calculate expiration time
        expiration_time = session_dict["created_at"] + timedelta(seconds=self.session_duration)

        # Return user_id if the current time is before the expiration time
        if datetime.now() < expiration_time:
            return session_dict["user_id"]

        return None
