#!/usr/bin/env python3
"""
Password encryption file
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Generate a salt and Hash password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
