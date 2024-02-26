#!/usr/bin/python3

"""
Version 1 of the AirBnB clone Flask app
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """
    Closes the storage on teardown
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """
    404 error handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'),
            threaded=True)
