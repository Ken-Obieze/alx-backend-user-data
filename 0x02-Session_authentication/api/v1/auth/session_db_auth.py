#!/usr/bin/env python3
"""Module for Authentication from database."""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
import os

class SessionDBAuth(SessionExpAuth):
    """Session DB Authentication."""
    def create_session(self, user_id=None):
        session_id = super().create_session(user_id)

        if session_id:
            new_session = UserSession(user_id=user_id, session_id=session_id)
            self._db_session.add(new_session)
            self._db_session.commit()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        if session_id is None:
            return None

        user_session = self._db_session.query(UserSession).filter_by(session_id=session_id).first()

        if not user_session:
            return None

        session_dict = {
            "user_id": user_session.user_id,
            "created_at": user_session.created_at
        }

        if self.session_duration <= 0:
            return session_dict["user_id"]

        if "created_at" not in session_dict:
            return None

        expiration_time = session_dict["created_at"] + timedelta(seconds=self.session_duration)

        if datetime.now() < expiration_time:
            return session_dict["user_id"]

        return None

    def destroy_session(self, request=None):
        if request is None:
            return False

        session_id = self.session_cookie(request)
        user_session = self._db_session.query(UserSession).filter_by(session_id=session_id).first()

        if not user_session:
            return False

        self._db_session.delete(user_session)
        self._db_session.commit()

        return True
