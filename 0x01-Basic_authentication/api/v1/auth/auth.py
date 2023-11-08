#!/usr/bin/env python3
"""API uthentication module."""

from typing import List, TypeVar
from flask import request


class Auth:
    """Authentication Class declaration."""

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
