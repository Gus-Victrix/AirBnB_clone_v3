#!/usr/bin/python3

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
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

@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def rm_city(city_id):
    """Deletes a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})

@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def mk_city(state_id):
    """Creates a City object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    city = City(**request.get_json())
    city.state_id = state_id
    city.save()
    return (make_response(jsonify(city.to_dict()), 201))

@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def upd_city(city_id):
    """Updates a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
