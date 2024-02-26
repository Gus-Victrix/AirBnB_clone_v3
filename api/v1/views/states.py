#!/usr/bin/python3

from flask import jsonify, redirect, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False)
def states():
    """Return a list of all states"""
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return (jsonify(states))


@app_views.route('/states/<state_id>', strict_slashes=False)
def states_id(state_id):
    """Return a state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return (jsonify(state.to_dict()))


@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def rm_state(state_id):
    """Delete state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify({}))

@app_views.route("/states", methods=['POST'], strict_slashes=False)
def mk_state():
    """Create a new state"""
    if not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.json:
        return (jsonify({"error": "Missing name"}), 400)
    state = State(**request.json)
    state.save()
    return (jsonify(state.to_dict()), 201)

@app_view.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def up_state(state_id):
    """Update a state's details"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return (jsonify(state.to_dict()), 200)
