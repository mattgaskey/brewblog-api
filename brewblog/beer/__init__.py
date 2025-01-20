"""
This module initializes the Blueprint for the Beer API routes.
It sets up the blueprint and imports the routes to register them with the blueprint.
"""

from flask import Blueprint

bp = Blueprint('beer', __name__)

from brewblog.beer import routes
