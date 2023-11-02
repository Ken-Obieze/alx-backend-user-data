#!/usr/bin/env python3
"""Pawwsord emcryption."""

import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hash and salt a password using bcrypt.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        bytes: A salted and hashed password as a byte string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
