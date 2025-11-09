import os
import tempfile
import unittest

import sys
from deplacity import create_app
from deplacity.utils.db import get_db, close_db
from deplacity.models.city import City, search_by_postal_code

class TestUser(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = get_db()

        with open(os.path.join(os.path.dirname(__file__), "schema_test.sql"), "rb") as f:
            self.db.executescript(f.read().decode("utf8"))

    def tearDown(self):
        close_db()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_search_by_postal_code(self):
        db = get_db()
        db.execute("INSERT INTO ville (code_postal, nom_de_ville, population)\
                   VALUES (4000, 'Liège', 250000), (5000, 'Namur', 100000);")
        db.commit()
        villes = search_by_postal_code(4000)
        self.assertEqual(len(villes), 1)
        self.assertEqual(villes[0]["nom_de_ville"], 'Liège')


if __name__ == '__main__':
    unittest.main(verbosity=2)