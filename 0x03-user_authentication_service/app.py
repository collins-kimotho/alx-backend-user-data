#!/usr/bin/env python3
"""
Flask app that returns a simple JSON response.
"""

from flask import Flask, jsonify

# Initialize the Flask app
app = Flask(__name__)


#  Define the route for the home page
@app.route('/', methods=['GET'])
def home():
    """Return a simple JSON response."""
    return jsonify({"message": "Bienvenue"})


# Run the app when the script is executed
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
