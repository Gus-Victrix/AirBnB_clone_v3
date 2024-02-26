#!/usr/bin/python3

from flask import jsonify, redirect, abort
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
