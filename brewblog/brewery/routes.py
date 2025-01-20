"""
This module defines the routes for the Brewery API.
It includes endpoints to get a list of breweries, create a new brewery,
show a specific brewery, and edit an existing brewery.
"""

from flask import request, jsonify
import sqlalchemy as sa
from brewblog import db
from brewblog.brewery import bp
from brewblog.models import Brewery
from brewblog.auth import requires_auth
from brewblog.error_handlers import register_error_handlers

register_error_handlers(bp)

@bp.route('/api/breweries')
@requires_auth('get:breweries')
def get_breweries(payload):
    """
    Endpoint to get a list of breweries.

    Args:
        payload (dict): The JWT payload containing user information.

    Returns:
        Response: The JSON response with a list of breweries grouped by city and state.
    """
    breweries = db.session.scalars(sa.select(Brewery)).all()

    areas = {}
    for brewery in breweries:
        area = (brewery.city, brewery.state)
        if area not in areas:
            areas[area] = []
        areas[area].append(brewery)

    areas_list = [
      {'city': city,
       'state': state, 
       'breweries': [brewery.serialize() for brewery in breweries]
      } for (city, state), breweries in areas.items()]

    return jsonify(areas_list)

@bp.route('/api/breweries/create', methods=['POST'])
@requires_auth('create:breweries')
def create_brewery(payload):
    """
    Endpoint to create a new brewery.

    Args:
        payload (dict): The JWT payload containing user information.

    Returns:
        Response: The JSON response with the created brewery details or an error message.
    """
    data = request.json

    if not data:
        return jsonify({'error': 'Request does not contain a valid JSON body'}), 400

    required_fields = ['id', 'name', 'address', 'city', 'state', 'phone', 'website_link']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    brewery_id = data.get('id')

    # Check if the brewery already exists
    existing_brewery = db.session.scalar(sa.select(Brewery).where(Brewery.id == brewery_id))
    if existing_brewery:
        return jsonify({'error': f'Brewery with ID {brewery_id} already exists.'}), 400

    try:
        new_brewery = Brewery(
            id=brewery_id,
            name=data.get('name'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            phone=data.get('phone'),
            website_link=data.get('website_link')
        )
        db.session.add(new_brewery)
        db.session.commit()
        return jsonify(new_brewery.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 422
    finally:
        db.session.close()

@bp.route('/api/breweries/<string:brewery_id>')
@requires_auth('get:breweries')
def show_brewery(brewery_id, payload):
    """
    Endpoint to show details of a specific brewery.

    Args:
        brewery_id (str): The ID of the brewery to be shown.
        payload (dict): The JWT payload containing user information.

    Returns:
        Response: The JSON response with the brewery details or an error message.
    """
    brewery = db.session.scalar(sa.select(Brewery).where(Brewery.id == brewery_id))
    if brewery is None:
        return jsonify({'error': f'Brewery with id {brewery_id} not found.'}), 404

    brewery_data = brewery.serialize()

    return jsonify(brewery_data)

@bp.route('/api/breweries/<string:brewery_id>/edit', methods=['POST', 'PATCH'])
@requires_auth('edit:breweries')
def edit_brewery(brewery_id, payload):
    """
    Endpoint to edit an existing brewery.

    Args:
        brewery_id (str): The ID of the brewery to be edited.
        payload (dict): The JWT payload containing user information.

    Returns:
        Response: The JSON response with the updated brewery details or an error message.
    """
    brewery = db.session.scalar(sa.select(Brewery).where(Brewery.id == brewery_id))
    if brewery is None:
        return jsonify({'error': f'Brewery with id {brewery_id} not found.'}), 404

    data = request.json
    required_fields = ['name', 'address', 'city', 'state', 'phone', 'website_link']

    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    brewery.name = data['name']
    brewery.address = data['address']
    brewery.city = data['city']
    brewery.state = data['state']
    brewery.phone = data['phone']
    brewery.website_link = data['website_link']
    db.session.commit()

    return jsonify(brewery.serialize())