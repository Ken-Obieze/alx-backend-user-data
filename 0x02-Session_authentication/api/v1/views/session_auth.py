#!/usr/bin/env python3
"""Session Views Module."""

from flask import abort, jsonify, request
from api.v1.app import auth
from models.user import User
from api.v1.views import app_views
from os import getenv


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
    else:
        from api.v1.app import auth
        _my_session_id = auth.create_session(users[0].id)
        user_data = jsonify(users[0].to_json())
        session_name = getenv("SESSION_NAME")
        user_data.set_cookie(session_name, _my_session_id)
        return user_data, 200

@app.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_logout():
    """Session logout"""h
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
