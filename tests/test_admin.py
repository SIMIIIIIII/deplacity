import tempfile
import unittest
from unittest.mock import patch

import sys
from deplacity import create_app
from deplacity.utils.db import get_db
from deplacity.blueprints import admin

class TestUser(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = get_db()
        self.client = self.app.test_client()

    def test_admin_route_false(self):
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 302)
        redirected_url = response.headers['Location']
        self.assertEqual(redirected_url, '/admin/connexion')

    @patch('deplacity.blueprints.admin.connected', True)
    def test_admin_route_true(self):
        with self.app.test_client() as client:
            response = client.get('/admin')
            self.assertEqual(response.status_code, 200)
    
    def test_connexion_route(self):
        response = self.client.get('/admin/connexion')
        self.assertEqual(response.status_code, 200)

        with self.app.test_client() as client:
            response = client.get('/admin/connexion', data=dict(state="ok"))
            self.assertEqual(response.status_code, 200)

    def test_city_list_false(self):
        response = self.client.get('/admin/villes')
        self.assertEqual(response.status_code, 200)
    
    @patch('deplacity.blueprints.admin.affichier_city', True)
    def test_city_list_true(self):
        response = self.client.get('/admin/villes')
        self.assertEqual(response.status_code, 200)

    def test_city_delete_route(self):
        response = self.client.get('/admin/delete/1000')
        self.assertEqual(response.status_code, 302)
        redirected_url = response.headers['Location']
        self.assertEqual(redirected_url, '/admin/villes')
    
    def test_city_create_route(self):
        data = {
            'name': 'Bruxelles', 'postal_code': 1000,
            'population': 1541200}
        
        response = self.client.post('/admin/create', data = data)
        self.assertEqual(response.status_code, 302)
        redirected_url = response.headers['Location']
        self.assertEqual(redirected_url, '/admin/villes')
    
    def test_connexion_request(self):
        with self.app.test_client() as client:
            response = client.post(
                '/admin/connexion_request',
                data=dict(user = "Deplacity", password = "G19DeplacityUcl"))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/admin')

            response = client.post(
                '/admin/connexion_request',
                data=dict(user = "Deplacit", password = "G19DeplacityUcl"))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location,
                             '/admin/connexion?state=failed')

if __name__ == '__main__':
    unittest.main(verbosity=2)