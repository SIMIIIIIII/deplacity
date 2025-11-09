import os
import tempfile
import unittest

import sys
from deplacity import create_app
from deplacity.utils.db import get_db, close_db
from deplacity.models.requete import get_traffic_by_street, search_trafic_city, traffic_proportion, week_days

class TestUser(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = get_db()
        self.client = self.app.test_client()

        with open(os.path.join(os.path.dirname(__file__), "schema_test.sql"), "rb") as f:
            self.db.executescript(f.read().decode("utf8"))

    def tearDown(self):
        close_db()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_search_trafic_city(self):
        self.db.execute(
            """INSERT INTO ville(code_postal, nom_de_ville, population)
            VALUES(4000, 'Liége',250000), (5000,'Namur',100000) """)
        self.db.execute(
            """INSERT INTO rue(rue_id, nom_de_rue, code_postal)
            VALUES (9000003524, 'Avenue Rogier', 4000), (2, 'Rue Godefroid', 5000);""")
        self.db.executemany(
            """INSERT INTO proportion(
                rue_id, date,pieton, velo, voiture, lourd)
                VALUES(?,?,?,?,?,?)""",
                ((9000003524,'2024-01-05T15:00:00.000Z',607.6923076923,
                7.6923076923,46.1538461538,0.0),
                (9000003524,'2024-02-05T16:00:00.000Z',0.0,0.0,0.0,0.0),
                (9000003524,'2023-01-06T07:00:00.000Z',458.3850931677,
                11.1801242236,0.0,0.0),
                (2,'2024-01-05T16:00:00.000Z',0.0,0.0,0.0,0.0)))
        self.assertListEqual(search_trafic_city('Liége'),
                         [1066.08, 18.87, 46.15],
                         "La liste retourner n'est pas bonne")
        
        self.assertNotEqual(search_trafic_city('Liége'),
                         ["0.43%", "0.01%", "0.02%", "0.0%"],
                         "La liste retourner n'est pas bonne")
        
        self.assertListEqual(search_trafic_city('Namur'),
                         [], "La liste retourner n'est pas bonne")
        
        self.assertNotEqual(search_trafic_city('Namur'),
                         [0.0, 0.0, 0.0, 0.0],
                         "La liste retourner n'est pas bonne")
        
        self.assertEqual(search_trafic_city("Liége", 2024),
                         [607.69, 7.69 ,46.15])
        
        self.assertEqual(search_trafic_city("Liége", 2024, 2),
                         [])
        self.assertEqual(search_trafic_city("Liége", 2023, 1),
                         [458.39, 11.18])
        
        
    def test_traffic_proportion(self):
        self.db.execute(
            """INSERT INTO ville(code_postal, nom_de_ville, population)
            VALUES(4000, 'Liége',250000), (5000,'Namur',100000) """)
        self.db.execute(
            """INSERT INTO rue(rue_id, nom_de_rue, code_postal)
            VALUES (5, 'Avenue Rogier', 4000), (2, 'Rue Godefroid', 5000);""")
        self.db.execute(
            """INSERT INTO proportion(
                rue_id, date, lourd, voiture, pieton, velo)
                VALUES(5, 2024-01-10, 0.0, 0.0, 0.0, 0.0),
                (2, 2024-01-13, 0.0,76.7394294328,
                107.5764323763,178.676536905);""")
        self.assertEqual(
            traffic_proportion(5),
            {"2013":{'lourd':0.0, 'pieton':0.0, 'velo':0.0, 'voiture':0.0}},
            "Le dictionnaire retourner n'est pas le bon")
        self.assertEqual(
            traffic_proportion(2),
            {"2010":{'pieton':107.5764323763, 'velo':178.676536905,
                     'voiture':76.7394294328, 'lourd':0.0}},
            "Le dictionnaire retourner n'est pas le bon")
        
    def test_week_days(self):
        self.db.execute(
            """INSERT INTO ville(code_postal, nom_de_ville, population)
            VALUES(4000, 'Liége',250000), (5000,'Namur',100000) """)
        self.db.execute(
            """INSERT INTO rue(rue_id, nom_de_rue, code_postal)
            VALUES (5, 'Avenue Rogier', 4000), (2, 'Rue Godefroid', 5000);""")
        self.db.execute(
            """INSERT INTO proportion(
                rue_id, date, lourd, voiture, pieton, velo)
            VALUES(5, '2024-01-05T22:00:00.000Z', 0.0, 0.0, 0.0, 0.0),
            (2, '2024-01-13T10:00:00.000Z', 0.0,76.7394294328,
            107.5764323763,178.676536905);""")
        self.assertEqual(
            week_days(traffic_proportion(5),250000),
            {'Friday':{"lourd":"0.0%", "pieton":"0.0%",
                       "velo":"0.0%", "voiture":"0.0%"}},
            "Le dictionnaire retourner n'est pas bon")
        self.assertEqual(
            week_days(traffic_proportion(2),100000),
            {'Saturday':{"velo":"0.18%", "pieton":"0.11%",
                         "voiture":"0.08%","lourd":"0.0%"}},
            "Le dictionnaire retourner n'est pas bon")
                        
    def test_get_traffic_by_street(self):
        self.db.execute(
            """INSERT INTO ville(code_postal, nom_de_ville, population)
            VALUES(4000, 'Liége',250000), (5000,'Namur',100000)""")
        self.db.execute(
            """INSERT INTO rue(rue_id, nom_de_rue, code_postal)
            VALUES (5, 'Avenue Rogier', 4000), (2, 'Rue Godefroid', 5000);""")
        self.db.execute(
            """INSERT INTO proportion(
                rue_id, date, lourd, voiture, pieton, velo)
                VALUES(5, '2024-01-05T22:00:00.000Z', 0.0, 0.0, 0.0, 0.0),
                (5, '2024-01-01T22:00:00.000Z', 0.0, 0.0, 0.0, 0.0),
                (5, '2024-01-02T22:00:00.000Z', 0.0, 0.0, 0.0, 0.0),
                (5, '2024-01-03T22:00:00.000Z', 0.0, 0.0, 0.0, 0.0),
                (5, '2024-01-04T22:00:00.000Z', 0.0, 0.0, 0.0, 0.0),
                (5, '2024-01-06T22:00:00.000Z', 0.0, 0.0, 0.0, 0.0),
                (5, '2024-01-07T22:00:00.000Z', 0.0, 0.0, 0.0, 0.0),
                (2, '2024-01-13T10:00:00.000Z', 0.0,76.7394294328,
                107.5764323763,178.676536905);""")
        self.assertEqual(
            get_traffic_by_street('Avenue Rogier'),
            {'Lundi':{ "pieton":"0.0%", "velo":"0.0%",
                      "voiture":"0.0%","lourd":"0.0%"},
            'Mardi':{ "pieton":"0.0%", "velo":"0.0%",
                     "voiture":"0.0%","lourd":"0.0%"},
            'Mercredi':{ "pieton":"0.0%", "velo":"0.0%",
                        "voiture":"0.0%","lourd":"0.0%"},
            'Jeudi':{ "pieton":"0.0%", "velo":"0.0%",
                     "voiture":"0.0%","lourd":"0.0%"},
            'Vendredi':{ "pieton":"0.0%", "velo":"0.0%",
                        "voiture":"0.0%","lourd":"0.0%"},
            'Samedi':{ "pieton":"0.0%", "velo":"0.0%",
                      "voiture":"0.0%","lourd":"0.0%"},
            'Dimanche':{ "pieton":"0.0%", "velo":"0.0%",
                        "voiture":"0.0%","lourd":"0.0%"}},
            "Le dictionnaire retourner n'est pas bon")
    
    def test_requete_routes(self):
        response = self.client.get('/requetes')
        self.assertEqual(response.status_code, 200)
    
    def test_request_by_city(self):
        with self.app.test_client() as client:
            response = client.post('/requetes/by_city/general', data=dict(ville='liege'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/requetes/by_city')

    def test_request_by_city_year(self):
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['chosen_city'] = "Liege"
            response = client.post('/requetes/by_city/by_year', data=dict(year=2024))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/requetes/by_city')
    
    def test_request_by_city_month(self):
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['chosen_city'] = "Liege"
                sess['year'] = 2025
            response = client.post('/requetes/by_city/by_year/by_month', data=dict(month="Janvier"))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/requetes/by_city')
    
    def test_request_by_city_render(self):
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['chosen_city'] = "Liege"
                sess['year'] = 2024
            response = client.get('/requetes/by_city')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)