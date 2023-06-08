#!/usr/bin/env python3
"""Session Views Module."""

from flask import abort, jsonify, request, make_response
from models.user import User
from api.v1.views import app_views
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
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
    from api.v1.app import auth
    cookie_name = getenv('SESSION_NAME')
    session_id = auth.create_session(user.id)
    response = make_response(jsonify(user.to_json()))
    if cookie_name and session_id:
        response.set_cookie(cookie_name, session_id)
    return response

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_logout(user_id: str = None) -> str:
    """Session logout"""
    from api.v1.app import authh
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
