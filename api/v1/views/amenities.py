#!/usr/bin/python3
"""Amenity objects that handles all default RestFul API actions"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    amenities = [amenity.to_dict() for amenity in amenities]
    return (jsonify(amenities))


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return (jsonify(amenity.to_dict()))


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({}))


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a Amenity"""
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({"error": 'Missing name'}), 400)
    amenity = Amenity(**data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def amenity_put(amenity_id):
    """update a amenities"""
    amenity_dict = storage.get("Amenity", amenity_id)
    if amenity_dict is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attributes, value in request.get_json().items():
        if attributes not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_dict, attributes, value)
    amenity_dict.save()
    return jsonify(amenity_dict.to_dict())
