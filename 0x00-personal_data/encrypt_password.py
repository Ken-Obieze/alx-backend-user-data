#!/usr/bin/env python3
"""
Password encryption file
"""
import bcrypt


def hash_password(password):
    """Generate a salt and Hash password."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def is_valid(hashed_password, password):
    """Check if the provided password matches the hashed password."""
    is_valid = False
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        is_valid = True
    return is_valid
