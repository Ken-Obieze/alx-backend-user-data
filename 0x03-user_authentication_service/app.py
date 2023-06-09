#!/usr/bin/env python3
"""
Flask app module
"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index() -> str:
    """Home route"""
    message = {"message": "Bienvenue"}
    return jsonify(message)

@app.route("/users", methods=["POST", strict_slashes=False])
def users() -> str:
    """Register new User."""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": "%s" % email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """this function creates a new session for the user, store it in the
    session ID as a cookie with key "session_id" and returns JSON payload"""
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)

    if not valid_login:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """this method finds the user with requested session ID, destroys the
    session and redirect the user to GET /"""
    cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(cookie)
    if cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')

@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """Profile endpoint."""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)

@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Generate a reset password token for the user."""
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "Missing email field"}), 400

    try:
        reset_token = auth.get_reset_password_token(email)
    except ValueError:
        return jsonify({"error": f"User with email {email} does not exist"}), 403

    return jsonify({"email": email, "reset_token": reset_token}), 200

@app.route('/reset_password', methods=['PUT'])
def update_password():
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        auth.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    user = auth._db.find_user_by_email(email)
    response = {"email": user.email, "message": "Password updated"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")