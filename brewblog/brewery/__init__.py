"""
This module initializes the Blueprint for the Brewery API routes.
It sets up the blueprint and imports the routes to register them with the blueprint.
"""

from flask import Blueprint

bp = Blueprint('brewery', __name__)

from brewblog.brewery import routes
