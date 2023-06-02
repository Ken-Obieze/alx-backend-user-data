#!/usr/bin/env python3
"""Basic Auth module."""


from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
            Performs base64 encoding on the authorization_header
            extract base64 of authorization header after 'Basic '
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]
