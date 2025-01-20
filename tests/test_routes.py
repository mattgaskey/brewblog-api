"""
This module contains unit tests for the Brewery API routes.
It tests the functionality of endpoints to get, create, edit, and delete breweries and beers.
"""

import unittest
import json
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import jwt
from brewblog import create_app, db
from brewblog.models import Brewery, Beer, Style

class BreweryTestCase(unittest.TestCase):
    """
    This class represents the Brewery test case.
    """
    def setUp(self):
        # Load environment variables from .env file
        load_dotenv()

        self.app = create_app()
        self.app.config['FLASK_ENV'] = 'Testing'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/test_db'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.seed_data()       
        with open('tests/private_key.pem', 'r', encoding='utf-8') as f:
            self.private_key = f.read()

    def tearDown(self):
        """
        Tear down the database after each test.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def seed_data(self):
        """
        Seed the database with initial data for testing.
        """
        style = Style(name='IPA')
        brewery = Brewery(
            id='1', 
            name='Test Brewery', 
            address='123 Test St', 
            city='Test City', 
            state='ND', 
            phone='123-456-7890', 
            website_link='http://testbrewery.com')
        beer = Beer(
            id=1, 
            name='Test Beer', 
            description='A test beer', 
            brewery_id='abcdefgh-1234567', 
            style_id=1)
        db.session.add(style)
        db.session.add(brewery)
        db.session.add(beer)
        db.session.commit()

    def test_get_breweries_success(self):
        """
        Test getting a list of breweries successfully.
        """
        response = self.client.get(
            '/api/breweries', 
            headers=self.get_auth_headers('get:breweries'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) > 0)

    def test_get_breweries_unauthorized(self):
        """
        Test getting a list of breweries without authorization.
        """
        response = self.client.get('/api/breweries')
        self.assertEqual(response.status_code, 401)

    def test_create_brewery_success(self):
        """
        Test creating a new brewery successfully.
        """
        new_brewery = {
            'id': '2',
            'name': 'New Brewery',
            'address': '456 New St',
            'city': 'New City',
            'state': 'NC',
            'phone': '987-654-3210',
            'website_link': 'http://newbrewery.com'
        }
        response = self.client.post(
            '/api/breweries/create', 
            headers=self.get_auth_headers('create:breweries'), 
            json=new_brewery)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'New Brewery')

    def test_create_brewery_missing_field(self):
        """
        Test creating a new brewery with a missing required field.
        """
        new_brewery = {
            'id': '2',
            'name': 'New Brewery',
            'address': '456 New St',
            'city': 'New City',
            'state': 'NC',
            'phone': '987-654-3210'
            # Missing website_link
        }
        response = self.client.post(
            '/api/breweries/create', 
            headers=self.get_auth_headers('create:breweries'), 
            json=new_brewery)
        self.assertEqual(response.status_code, 400)

    def test_create_brewery_insufficient_permissions(self):
        """
        Test creating a new brewery with insufficient permissions.
        """
        new_brewery = {
            'id': '2',
            'name': 'New Brewery',
            'address': '456 New St',
            'city': 'New City',
            'state': 'NC',
            'phone': '987-654-3210',
            'website_link': 'http://newbrewery.com'
        }
        response = self.client.post(
            '/api/breweries/create', 
            headers=self.get_auth_headers('get:breweries'), 
            json=new_brewery)
        self.assertEqual(response.status_code, 403)

    def test_show_brewery_success(self):
        """
        Test showing details of a specific brewery successfully.
        """
        response = self.client.get(
            '/api/breweries/1', 
            headers=self.get_auth_headers('get:breweries'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test Brewery')

    def test_show_brewery_not_found(self):
        """
        Test showing details of a non-existent brewery.
        """
        response = self.client.get(
            '/api/breweries/999', 
            headers=self.get_auth_headers('get:breweries'))
        self.assertEqual(response.status_code, 404)

    def test_edit_brewery_success(self):
        """
        Test editing an existing brewery successfully.
        """
        updated_brewery = {
            'name': 'Updated Brewery',
            'address': '123 Updated St',
            'city': 'Updated City',
            'state': 'US',
            'phone': '123-456-7890',
            'website_link': 'http://updatedbrewery.com'
        }
        response = self.client.patch(
            '/api/breweries/1/edit', 
            headers=self.get_auth_headers('edit:breweries'), 
            json=updated_brewery)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Updated Brewery')

    def test_edit_brewery_insufficient_permissions(self):
        """
        Test editing an existing brewery with insufficient permissions.
        """
        updated_brewery = {
            'name': 'Updated Brewery',
            'address': '123 Updated St',
            'city': 'Updated City',
            'state': 'US',
            'phone': '123-456-7890',
            'website_link': 'http://updatedbrewery.com'
        }
        response = self.client.patch(
            '/api/breweries/1/edit',
            headers=self.get_auth_headers('get:breweries'), 
            json=updated_brewery)
        self.assertEqual(response.status_code, 403)

    def test_edit_brewery_not_found(self):
        """
        Test editing a non-existent brewery.
        """
        updated_brewery = {
            'name': 'Updated Brewery',
            'address': '123 Updated St',
            'city': 'Updated City',
            'state': 'US',
            'phone': '123-456-7890',
            'website_link': 'http://updatedbrewery.com'
        }
        response = self.client.patch(
            '/api/breweries/999/edit', 
            headers=self.get_auth_headers('edit:breweries'), 
            json=updated_brewery)
        self.assertEqual(response.status_code, 404)

    def test_get_beers_for_brewery_success(self):
        """
        Test getting a list of beers for a specific brewery successfully.
        """
        response = self.client.get(
            '/api/breweries/1/beers', 
            headers=self.get_auth_headers('get:breweries'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) > 0)

    def test_create_beer_success(self):
        """
        Test creating a new beer successfully.
        """
        new_beer = {
            'id': 2,
            'name': 'New Beer',
            'description': 'A new beer',
            'style': 1,
            'brewery_id': '1'
        }
        response = self.client.post(
            '/api/beers/create', 
            headers=self.get_auth_headers('create:beers'), 
            json=new_beer)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'New Beer')

    def test_create_beer_brewery_not_found(self):
        """
        Test creating a new beer for a non-existent brewery.
        """
        new_beer = {
            'name': 'New Beer',
            'description': 'A new beer',
            'style': 1,
            'brewery_id': '999'  # Non-existent brewery
        }
        response = self.client.post(
            '/api/beers/create', 
            headers=self.get_auth_headers('create:beers'), 
            json=new_beer)
        self.assertEqual(response.status_code, 404)

    def test_delete_beer_success(self):
        """
        Test deleting a beer successfully.
        """
        response = self.client.post(
            '/api/beers/1/delete', 
            headers=self.get_auth_headers('delete:beers'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Beer Test Beer deleted successfully.')

    def test_delete_beer_not_found(self):
        """
        Test deleting a non-existent beer.
        """
        response = self.client.post(
            '/api/beers/999/delete', 
            headers=self.get_auth_headers('delete:beers'))
        self.assertEqual(response.status_code, 404)

    def test_get_styles_success(self):
        """
        Test getting a list of beer styles successfully.
        """
        response = self.client.get('/api/styles')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) > 0)

    def get_auth_headers(self, permission):
        """
        Helper method to get authorization headers with a mock JWT token.

        Args:
            permission (str): The permission to include in the JWT token.

        Returns:
            dict: The authorization headers.
        """
        token = self.get_token(permission)
        return {
            'Authorization': f'Bearer {token}'
        }

    def get_token(self, permission):
        """
        Helper method to generate a mock JWT token for testing.

        Args:
            permission (str): The permission to include in the JWT token.

        Returns:
            str: The generated JWT token.
        """
        payload = {
            'permissions': [permission],
            'exp': int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
            'iat': int(datetime.now(timezone.utc).timestamp()),
            'iss': 'test_issuer',
            'sub': 'test_subject'
        }
        return jwt.encode(payload, self.private_key, algorithm='RS256')

if __name__ == '__main__':
    unittest.main()
