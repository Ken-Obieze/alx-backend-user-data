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

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate if the provided password matches the hashed password.

    Args:
        hashed_password (bytes): Salted and hashed password as a byte string.
        password (str): The plain-text password to be validated.

    Returns:
        bool: True if password matched, otherwise False.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
