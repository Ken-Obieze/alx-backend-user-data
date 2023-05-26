#!/usr/bin/env python3
"""
Password encryption file
"""
import bcrypt


def hash_password(password):
    """Generate a salt and Hash password."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password

def is_valid(hashed_password, password):
    """Check if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
