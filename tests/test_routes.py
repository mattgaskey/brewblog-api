import unittest
import json
import os
from datetime import datetime, timedelta, timezone
import jwt
from brewblog import create_app, db
from brewblog.models import Brewery, Beer, Style

class BreweryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:postgres@localhost/test_db')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.seed_data()
        
        with open('tests/private_key.pem', 'r') as f:
            self.private_key = f.read()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def seed_data(self):
        style = Style(name='IPA')
        brewery = Brewery(id='1', name='Test Brewery', address='123 Test St', city='Test City', state='TS', phone='123-456-7890', website_link='http://testbrewery.com')
        beer = Beer(id=1, name='Test Beer', description='A test beer', brewery_id='1', style_id=1)
        db.session.add(style)
        db.session.add(brewery)
        db.session.add(beer)
        db.session.commit()

    def test_get_breweries_success(self):
        response = self.client.get('/api/breweries', headers=self.get_auth_headers('get:breweries'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) > 0)

    def test_get_breweries_unauthorized(self):
        response = self.client.get('/api/breweries')
        self.assertEqual(response.status_code, 401)

    def test_create_brewery_success(self):
        new_brewery = {
            'id': '2',
            'name': 'New Brewery',
            'address': '456 New St',
            'city': 'New City',
            'state': 'NC',
            'phone': '987-654-3210',
            'website_link': 'http://newbrewery.com'
        }
        response = self.client.post('/api/breweries/create', headers=self.get_auth_headers('create:breweries'), json=new_brewery)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'New Brewery')

    def test_create_brewery_missing_field(self):
        new_brewery = {
            'id': '2',
            'name': 'New Brewery',
            'address': '456 New St',
            'city': 'New City',
            'state': 'NC',
            'phone': '987-654-3210'
            # Missing website_link
        }
        response = self.client.post('/api/breweries/create', headers=self.get_auth_headers('create:breweries'), json=new_brewery)
        self.assertEqual(response.status_code, 400)

    def test_create_brewery_insufficient_permissions(self):
        new_brewery = {
            'id': '2',
            'name': 'New Brewery',
            'address': '456 New St',
            'city': 'New City',
            'state': 'NC',
            'phone': '987-654-3210',
            'website_link': 'http://newbrewery.com'
        }
        response = self.client.post('/api/breweries/create', headers=self.get_auth_headers('get:breweries'), json=new_brewery)
        self.assertEqual(response.status_code, 403)

    def test_show_brewery_success(self):
        response = self.client.get('/api/breweries/1', headers=self.get_auth_headers('get:breweries'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test Brewery')

    def test_show_brewery_not_found(self):
        response = self.client.get('/api/breweries/999', headers=self.get_auth_headers('get:breweries'))
        self.assertEqual(response.status_code, 404)

    def test_edit_brewery_success(self):
        updated_brewery = {
            'name': 'Updated Brewery',
            'address': '123 Updated St',
            'city': 'Updated City',
            'state': 'US',
            'phone': '123-456-7890',
            'website_link': 'http://updatedbrewery.com'
        }
        response = self.client.patch('/api/breweries/1/edit', headers=self.get_auth_headers('edit:breweries'), json=updated_brewery)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Updated Brewery')

    def test_edit_brewery_insufficient_permissions(self):
        updated_brewery = {
            'name': 'Updated Brewery',
            'address': '123 Updated St',
            'city': 'Updated City',
            'state': 'US',
            'phone': '123-456-7890',
            'website_link': 'http://updatedbrewery.com'
        }
        response = self.client.patch('/api/breweries/1/edit', headers=self.get_auth_headers('get:breweries'), json=updated_brewery)
        self.assertEqual(response.status_code, 403)

    def test_edit_brewery_not_found(self):
        updated_brewery = {
            'name': 'Updated Brewery',
            'address': '123 Updated St',
            'city': 'Updated City',
            'state': 'US',
            'phone': '123-456-7890',
            'website_link': 'http://updatedbrewery.com'
        }
        response = self.client.patch('/api/breweries/999/edit', headers=self.get_auth_headers('edit:breweries'), json=updated_brewery)
        self.assertEqual(response.status_code, 404)

    def test_get_beers_for_brewery_success(self):
        response = self.client.get('/api/breweries/1/beers', headers=self.get_auth_headers('get:breweries'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) > 0)

    def test_create_beer_success(self):
        new_beer = {
            'id': 2,
            'name': 'New Beer',
            'description': 'A new beer',
            'style': 1,
            'brewery_id': '1'
        }
        response = self.client.post('/api/beers/create', headers=self.get_auth_headers('create:beers'), json=new_beer)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'New Beer')

    def test_create_beer_brewery_not_found(self):
        new_beer = {
            'name': 'New Beer',
            'description': 'A new beer',
            'style': 1,
            'brewery_id': '999'  # Non-existent brewery
        }
        response = self.client.post('/api/beers/create', headers=self.get_auth_headers('create:beers'), json=new_beer)
        self.assertEqual(response.status_code, 404)

    def test_delete_beer_success(self):
        response = self.client.post('/api/beers/1/delete', headers=self.get_auth_headers('delete:beers'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Beer Test Beer deleted successfully.')

    def test_delete_beer_not_found(self):
        response = self.client.post('/api/beers/999/delete', headers=self.get_auth_headers('delete:beers'))
        self.assertEqual(response.status_code, 404)

    def test_get_styles_success(self):
        response = self.client.get('/api/styles')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) > 0)

    def get_auth_headers(self, permission):
        token = self.get_token(permission)
        return {
            'Authorization': f'Bearer {token}'
        }

    def get_token(self, permission):
        # Mock token generation for testing
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