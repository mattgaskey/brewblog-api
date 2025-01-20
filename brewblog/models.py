from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from brewblog import db

class Brewery(db.Model):
    __tablename__ = 'Brewery'

    id = sa.Column(sa.String(36), primary_key=True)
    name = sa.Column(sa.String(120), index=True)
    address = sa.Column(sa.String(120))
    phone = sa.Column(sa.String(120))
    website_link = sa.Column(sa.String(120))
    city = sa.Column(sa.String(120))
    state = sa.Column(sa.String(120))

    beers = relationship('Beer', back_populates='brewery')

    def __repr__(self) -> str:
        return f'<Brewery {self.name}>'

    def add_beer(self, beer):
        self.beers.append(beer)

    def get_beers(self):
        return list(db.session.scalars(sa.select(Beer).filter(Beer.brewery_id == self.id)))

    def get_beers_count(self):
        return len(self.get_beers())

    def serialize(self):
        beers = db.session.execute(
            sa.select(Beer, Style.name)
            .join(Style, Beer.style_id == Style.id)
            .filter(Beer.brewery_id == self.id)
        ).all()

        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website_link": self.website_link,
            "beers": [{
                "beer_id": beer.id,
                "beer_name": beer.name,
                "beer_style": style_name,
                "beer_description": beer.description,
            } for beer, style_name in beers],
            "beers_count": self.get_beers_count()
        }

class Beer(db.Model):
    __tablename__ = 'Beer'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, index=True)
    description = sa.Column(sa.String(500))
    brewery_id = sa.Column(sa.String(36), sa.ForeignKey('Brewery.id'))
    style_id = sa.Column(sa.Integer, sa.ForeignKey('Style.id'))

    brewery = relationship('Brewery', back_populates='beers')
    style = relationship('Style')

    def __repr__(self) -> str:
        return f'<Beer {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "style": self.style.name,
            "description": self.description,
            "brewery_id": self.brewery_id
        }

class Style(db.Model):
    __tablename__ = 'Style'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)

    def __repr__(self) -> str:
        return f'<Style {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }