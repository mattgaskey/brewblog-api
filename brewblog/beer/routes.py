"""
This module defines the routes for the Beer API.
It includes endpoints to get beers for a specific brewery, create a new beer,
delete a beer, and get a list of beer styles.
"""

from flask import request, jsonify
import sqlalchemy as sa
from brewblog import db
from brewblog.beer import bp
from brewblog.models import Beer, Brewery, Style
from brewblog.auth import requires_auth
from brewblog.error_handlers import register_error_handlers

register_error_handlers(bp)

@bp.route('/api/breweries/<string:brewery_id>/beers', methods=['GET'])
@requires_auth('get:breweries')
def get_beers_for_brewery(brewery_id, payload):
    """
    Endpoint to get a list of beers for a specific brewery.

    Args:
        brewery_id (str): The ID of the brewery.
        payload (dict): The JWT payload containing user information.

    Returns:
        Response: The JSON response with a list of beers for the specified brewery.
    """
    beers = db.session.scalars(sa.select(Beer).where(Beer.brewery_id == brewery_id)).all()
    return jsonify([beer.serialize() for beer in beers]), 200

@bp.route('/api/beers/create', methods=['POST'])
@requires_auth('create:beers')
def create_beer(payload):
    """
    Endpoint to create a new beer.

    Args:
        payload (dict): The JWT payload containing user information.

    Returns:
        Response: The JSON response with the created beer details or an error message.
    """
    data = request.json
    brewery_id = data.get('brewery_id')
    brewery = db.session.scalar(sa.select(Brewery).where(Brewery.id == brewery_id))
    if not brewery:
        return jsonify({'error': f'Brewery with ID {brewery_id} not found.'}), 404

    new_beer = Beer(
        id=data.get('id'),
        name=data.get('name'),
        description=data.get('description'),
        style_id=data.get('style'),
        brewery_id=brewery.id
    )
    db.session.add(new_beer)
    db.session.commit()
    return jsonify(new_beer.serialize()), 201

@bp.route('/api/beers/<int:beer_id>/delete', methods=['POST'])
@requires_auth('delete:beers')
def delete_beer(beer_id, payload):
    """
    Endpoint to delete a beer.

    Args:
        beer_id (int): The ID of the beer to be deleted.
        payload (dict): The JWT payload containing user information.

    Returns:
        Response: The JSON response with a success message or an error message.
    """
    beer = db.session.scalar(sa.select(Beer).where(Beer.id == beer_id))
    if beer is None:
        return jsonify({'error': f'Beer with id {beer_id} not found.'}), 404

    brewery_id = beer.brewery_id
    db.session.delete(beer)
    db.session.commit()
    return jsonify({
      'message': f'Beer {beer.name} deleted successfully.', 
      'brewery_id': brewery_id
    }), 200

@bp.route('/api/styles', methods=['GET'])
def get_styles():
    """
    Endpoint to get a list of beer styles.

    Returns:
        Response: The JSON response with a list of beer styles.
    """
    styles = db.session.scalars(sa.select(Style).distinct()).all()
    return jsonify([style.serialize() for style in styles]), 200
