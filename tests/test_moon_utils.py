import unittest
from decimal import Decimal
from datetime import datetime
import sys
from deplacity.utils.moon_utils import MoonPhase, age, phase

class MoonUtilsTestCase (unittest.TestCase):

    def test_age(self):
        #self.assertIsNone(age(5),"Vous avez rentré une mauvaise donné")
        self.assertIs(type(age(datetime(2005,6,30))),Decimal,"Le type ressortit n'est pas celui attend")
        self.assertEqual(age(datetime(2000, 1, 6)),float(0),"La fonction ne retourn pas le resultat attendu" )
        self.assertEqual(float(age(datetime(2019, 1, 21, 5, 16, 0))),0.5185003123784384421564326,
                         "La fonction ne retourn pas le resultat attendu" )

    def test_phase(self):
        my_fixture = datetime(2019, 1, 21, 5, 16, 0)
        expected = MoonPhase.FULL_MOON
        self.assertEqual(phase(age(my_fixture)), expected,
                         msg=f'My error message on pl.f({my_fixture}) different than {expected}')
        self.assertIs(type(phase(age(my_fixture))),MoonPhase,"La fonction ne retourne pas le type attendu")
        self.assertEqual(phase(age(datetime(2005,6,30))),MoonPhase.WANING_CRESCENT,
                         "La fonction ne retourne pas la phase lunaire attendu")

if __name__ == '__main__':
    unittest.main(verbosity=2)