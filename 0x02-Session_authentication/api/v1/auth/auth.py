#!/usr/bin/env python3
"""API uthentication module."""

from typing import List, TypeVar
from flask import request
import os


class Auth:
    """Authentication Class."""

    def authorization_header(self, request=None) -> str:
        """Add auth header."""
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """Get current user."""
        return None

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Improving required Auth."""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths or path + "/" in excluded_paths:
            return False
        for ex_path in excluded_paths:
            if ex_path.endswith("*"):
                prefix = ex_path[:-1]
                if path.startswith(prefix):
                    return False
            elif path == ex_path:
                return False
        return True

    def session_cookie(self, request=None):
        """Return cookie value froma a request."""
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
