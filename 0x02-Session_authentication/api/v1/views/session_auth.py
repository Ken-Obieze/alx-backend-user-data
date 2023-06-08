#!/usr/bin/env python3
"""Session Views Module."""

from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views
from os import getenv


@app_view.sroute('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
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
        _my_session_id = auth.create_session(user.id)
        user_data = jsonify(user.to_json())
        session_name = getenv("SESSION_NAME")
        user_data.set_cookie(session_name, _my_session_id)
        return user_data, 200

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_logout() -> str:
    """Session logout"""
    from api.v1.app import authh
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
