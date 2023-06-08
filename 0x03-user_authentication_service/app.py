#!/usr/bin/env python3
"""
Flask app module
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
    message = {"message": "Bienvenue"}
    return jsonify(message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

