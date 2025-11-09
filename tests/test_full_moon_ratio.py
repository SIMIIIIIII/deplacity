import os
import tempfile
import unittest

import sys
from deplacity import create_app
from deplacity.utils.db import get_db, close_db
from deplacity.utils.csv_file import write_in_db
from deplacity.models.full_moon_ratio import get_velo_full_moon

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

    def test_full_moon_ratio(self):
        #on rempli la database avec les données du fichier csv
        write_in_db()
        full_moon = get_velo_full_moon("Liege")
        self.assertEqual(type(full_moon), list)
        #self.assertEqual(type(full_moon[2023]), list)
        self.assertEqual(len(full_moon), 2)
        self.assertEqual(type(full_moon[0]), float)
        self.assertEqual(type(full_moon[1]), float)
        

if __name__ == '__main__':
    unittest.main(verbosity=2)