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
    beers = db.session.scalars(sa.select(Beer).where(Beer.brewery_id == brewery_id)).all()
    return jsonify([beer.serialize() for beer in beers]), 200

@bp.route('/api/beers/create', methods=['POST'])
@requires_auth('create:beers')
def create_beer(payload):
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
    beer = db.session.scalar(sa.select(Beer).where(Beer.id == beer_id))
    if beer is None:
        return jsonify({'error': f'Beer with id {beer_id} not found.'}), 404

    brewery_id = beer.brewery_id
    db.session.delete(beer)
    db.session.commit()
    return jsonify({'message': f'Beer {beer.name} deleted successfully.', 'brewery_id': brewery_id}), 200

@bp.route('/api/styles', methods=['GET'])
def get_styles():
    styles = db.session.scalars(sa.select(Style).distinct()).all()
    return jsonify([style.serialize() for style in styles]), 200