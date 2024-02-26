#!/usr/bin/python3

from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city(city_id):
    """Retrieves a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())
