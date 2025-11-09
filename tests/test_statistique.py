import os
import tempfile
import unittest

import sys
from deplacity import create_app
from deplacity.utils.db import get_db, close_db
from deplacity.models.statistique import entrees,get_number_of_rue,top_ville_cyclabe
from deplacity.models.city import get_city_list
class TestUser(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = get_db()
        self.client = self.app.test_client()
        self.db.execute("INSERT INTO ville(code_postal, nom_de_ville, population)\
                        VALUES(4000, 'Liége',250000), (5000,'Namur',100000)")
       
        with open(os.path.join(os.path.dirname(__file__), "schema_test.sql"), "rb") as f:
            self.db.executescript(f.read().decode("utf8"))

    def tearDown(self):
        close_db()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_get_number_of_rue(self):
        self.db.execute(
            "INSERT INTO ville(code_postal, nom_de_ville, population)\
                VALUES(4000, 'Liége',250000), (5000,'Namur',100000)")
        self.db.execute(
            "INSERT INTO rue(rue_id, nom_de_rue, code_postal)\
                VALUES (5, 'Avenue Rogier', 4000), (2, 'Rue Godefroid', 5000);")
        self.db.commit()
        self.assertIs(type(get_number_of_rue()),list)
        self.assertEqual(get_number_of_rue(),[1,1])
    
    def test_entrees(self):
        self.db.execute(
            """INSERT INTO ville(code_postal, nom_de_ville, population)
            VALUES(4000, 'Liége',250000), (5000,'Namur',100000) """)
        self.db.execute(
            """INSERT INTO rue(rue_id, nom_de_rue, code_postal)
            VALUES (9000003524, 'Avenue Rogier', 4000), (2, 'Rue Godefroid', 5000);""")
        self.db.execute(
            """INSERT INTO v85(rue_id, date, v85)
            VALUES (2, 2024-5-9, 15.3)"""
        )
        
        nbr = entrees()
        self.assertEqual(len(nbr), 5)
        self.assertIsInstance(nbr, dict)
        self.assertEqual(nbr['ville'], nbr['rue'], 2)
        self.assertEqual(nbr['v85'], 1)
        self.assertEqual(nbr['trafic'], nbr['vitesse'], 0)
    
    def test_top_ville_cyclabe(self):
        self.db.execute(
            """INSERT INTO ville(code_postal, nom_de_ville, population)
            VALUES(4000, 'Liége',250000), (5000,'Namur',100000),
             (1000, 'Bruxelle', 25410), (9470, 'Denderleeuw', 4510); """)
        self.db.execute(
            """INSERT INTO rue(rue_id, nom_de_rue, code_postal)
            VALUES (5, 'Avenue Rogier', 4000), (2, 'Rue Godefroid', 5000),
            (3, 'Sim', 1000), (4, 'je', 9470);""")
        self.db.execute(
            """INSERT INTO trafic(rue_id, date, type_vehicule, nb_vehicules)
            VALUES (5, 2024-5-6, 'velo', 25), (3, 2023-6-2, 'velo', 85),
            (4, 2012-9-5, 'velo', 15), (2, 2032-5-4, 'velo', 100);""")
        
        top_3 = top_ville_cyclabe()
        ville = []
        for i in top_3:
            ville.append(i['nom_de_ville'])
        
        self.assertEqual(len(ville), 3)
        self.assertNotIn('Denderleeuw', ville)
        self.assertEqual(ville[0], "Namur")
        self.assertEqual(ville[2], "Liége")
    
    def test_statistique_route(self):
        response = self.client.get('/statistique')
        self.assertEqual(response.status_code, 200)

        titre = "<title>Statistiques</title>"
        self.assertIn(titre, response.text)

if __name__ == '__main__':
    unittest.main(verbosity=2)