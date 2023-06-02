#!/usr/bin/env python3
"""API uthentication module."""

from typing import List, TypeVar
from flask import request


class Auth:
    """Authentication Class."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Requires authentication."""
        return False

    def authorization_header(self, request=None) -> str:
        """Add auth header."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get current user."""
        return None

