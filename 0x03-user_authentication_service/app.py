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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
