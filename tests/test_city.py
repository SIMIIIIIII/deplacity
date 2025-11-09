import os
import tempfile
import unittest

import sys
from deplacity import create_app
from deplacity.utils.db import get_db, close_db
from deplacity.models.city import (
    get_city_list, search_by_city, get_street,
    City, get_months, get_years)

class TestUser(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = get_db()
        
        with open(
            os.path.join(os.path.dirname(__file__),
                         "schema_test.sql"), "rb") as f:
            self.db.executescript(f.read().decode("utf8"))

    def tearDown(self):
        close_db()
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_get_city_list(self):
        self.db.execute(
            """INSERT INTO ville(code_postal, nom_de_ville, population)
            VALUES (4000, 'Liège', 250000), (5000, 'Namur', 100000);"""
        )

        city_list = get_city_list()
        villes = []
        for i in city_list:
            villes.append(i['nom_de_ville'])
        self.assertEqual(len(villes), 2)
        self.assertIn('Namur', villes)

    def test_search_by_city(self):
        self.db.execute(
            """INSERT INTO ville(code_postal, nom_de_ville, population)
            VALUES (4000, 'Liège', 250000), (5000, 'Namur', 100000);"""
        )
        city = search_by_city('Liège')
        for i in city:
            self.assertEqual(i['nom_de_ville'], 'Liège')
            self.assertEqual(i['population'], 250000)
            self.assertEqual(i['code_postal'], 4000)
    
    def test_get_street(self):
        self.db.execute(
            """INSERT INTO ville(code_postal, nom_de_ville, population)
            VALUES (4000, 'Liège', 250000), (5000, 'Namur', 100000);"""
        )
        self.db.execute(
            """INSERT INTO rue(rue_id, nom_de_rue, code_postal)
            VALUES (5, 'Avenue Rogier', 4000),
            (2, 'Rue Godefroid', 5000),
            (3, 'Simeon', 4000);"""
            )
        street = get_street('Liège')
        self.assertEqual(len(street), 2)
        self.assertIn('nom_de_rue', street[0].keys())
        self.assertNotIn('rue_id', street[0].keys())
        self.assertNotIn('code_postal', street[0].keys())
    
    def test_get_years_months(self):
        self.db.execute(
            """INSERT INTO ville(code_postal, nom_de_ville, population)
            VALUES (4000, 'Liège', 250000), (5000, 'Namur', 100000);"""
        )
        self.db.execute(
            """INSERT INTO rue(rue_id, nom_de_rue, code_postal)
            VALUES (5, 'Avenue Rogier', 4000),
            (2, 'Rue Godefroid', 5000),
            (3, 'Simeon', 4000);""")
        
        self.db.execute("""INSERT INTO trafic(
                rue_id, date, type_vehicule, nb_vehicules)
                VALUES(5, '2024-01-05T22:00:00.000Z', 'velo', 5),
                (2, '2022-01-01T22:00:00.000Z', 'pieton', 52),
                (5, '2024-05-02T22:00:00.000Z', 'voiture', 5),
                (2, '2026-10-03T22:00:00.000Z', "pieton", 2),
                (5, '2020-01-04T22:00:00.000Z', "voiture", 6),
                (3, '2024-12-06T22:00:00.000Z', "lourd", 4),
                (5, '2024-01-07T22:00:00.000Z', "velo", 0),
                (2, '2024-10-13T10:00:00.000Z', "pieton", 1);""")
        
        self.assertEqual(get_years("Liège"), [2024, 2020])
        self.assertEqual(get_years("BX"), [])
        self.assertEqual(get_months(2022,'Namur'), ["Janvier"])
        self.assertEqual(get_months(2024,'Liège'),
                         ["Decembre", "Janvier", "Mai"])
        
    
    def test_city_class(self):
        city1 = City('Denderleeuw', 54000, 9470)
        city2 = City('Liège', 250000, 4000)

        city1.save()
        city2.save()
        
        city_list = get_city_list()
        villes = []
        for i in city_list:
            villes.append(i['nom_de_ville'])
        self.assertEqual(len(villes), 2)
        self.assertIn('Liège', villes)
        self.assertIn('Denderleeuw', villes)
        city3 = City.get(4000)
        self.assertEqual(city2.name, city3.name)
        city1.delete()

        city_list = get_city_list()
        villes = []

        for i in city_list:
            villes.append(i['nom_de_ville'])
        self.assertEqual(len(villes), 1)
        self.assertIn('Liège', villes)
        self.assertNotIn('Denderleeuw', villes)

        city4 = City.get(510)
        self.assertIsNone(city4)


if __name__ == '__main__':
    unittest.main(verbosity=2)