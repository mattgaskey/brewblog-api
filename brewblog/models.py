"""
This module defines the database models for the Brewery API.
It includes models for Brewery, Beer, and Style, along with 
their relationships and serialization methods.
"""

from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from brewblog import db

class Brewery(db.Model):
    """
    Brewery model representing a brewery entity.

    Attributes:
        id (str): The unique identifier for the brewery.
        name (str): The name of the brewery.
        address (str): The address of the brewery.
        phone (str): The phone number of the brewery.
        website_link (str): The website link of the brewery.
        city (str): The city where the brewery is located.
        state (str): The state where the brewery is located.
        beers (list): The list of beers associated with the brewery.
    """
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
        """
        Adds a beer to the brewery's list of beers.

        Args:
            beer (Beer): The beer to be added.
        """
        self.beers.append(beer)

    def get_beers(self):
        """
        Retrieves the list of beers associated with the brewery.

        Returns:
            list: The list of beers.
        """
        return list(db.session.scalars(sa.select(Beer).filter(Beer.brewery_id == self.id)))

    def get_beers_count(self):
        """
        Retrieves the count of beers associated with the brewery.

        Returns:
            int: The count of beers.
        """
        return len(self.get_beers())

    def serialize(self):
        """
        Serializes the brewery object to a dictionary.

        Returns:
            dict: The serialized brewery object.
        """
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
    """
    Beer model representing a beer entity.

    Attributes:
        id (int): The unique identifier for the beer.
        name (str): The name of the beer.
        description (str): The description of the beer.
        brewery_id (str): The ID of the brewery associated with the beer.
        style_id (int): The ID of the style associated with the beer.
        brewery (Brewery): The brewery associated with the beer.
        style (Style): The style associated with the beer.
    """
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
        """
        Serializes the beer object to a dictionary.

        Returns:
            dict: The serialized beer object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "style": self.style.name,
            "description": self.description,
            "brewery_id": self.brewery_id
        }

class Style(db.Model):
    """
    Style model representing a beer style entity.

    Attributes:
        id (int): The unique identifier for the style.
        name (str): The name of the style.
    """
    __tablename__ = 'Style'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)

    def __repr__(self) -> str:
        return f'<Style {self.name}>'

    def serialize(self):
        """
        Serializes the style object to a dictionary.

        Returns:
            dict: The serialized style object.
        """
        return {
            "id": self.id,
            "name": self.name
        }
