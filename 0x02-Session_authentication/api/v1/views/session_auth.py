#!/usr/bin/env python3
"""Session Views Module."""

from flask import abort, jsonify, request
from api.v1.app import auth
from models.user import User


@app.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """Session login."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(auth.SESSION_NAME, session_id)

    return response
