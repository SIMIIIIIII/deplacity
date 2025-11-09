from enum import Enum
from datetime import datetime
from decimal import Decimal

class MoonPhase(Enum):
    NEW_MOON = 0
    WAXING_CRESCENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL_MOON = 4
    WANING_GIBBOUS = 5
    LAST_QUARTER = 6
    WANING_CRESCENT = 7


def age(date: datetime):
    """
    pre: Une date sous la forme 'datetime(annee,mois,jour)'
    post: retourne une décimal qui représente une phase
           lunaire
    """
    new_moons_ref = datetime(2000, 1, 6)
    years_since_ref = date - new_moons_ref
    days_since_ref = Decimal(years_since_ref.days)
    new_moons = days_since_ref / Decimal(29.530588853)
    phase = new_moons - int(new_moons)
    return phase

def phase(age: Decimal):
    """
    pre: un nombre décimal
    post: retourne la phase lunaire correpondant à la décimale
    """
    if age <  Decimal(0.031):
        return MoonPhase.NEW_MOON
    elif age < Decimal(0.219):
        return MoonPhase.WAXING_CRESCENT
    elif age < Decimal(0.281):
        return MoonPhase.FIRST_QUARTER
    elif age < Decimal(0.469):
        return MoonPhase.WAXING_GIBBOUS
    elif age < Decimal(0.531):
        return MoonPhase.FULL_MOON
    elif age < Decimal(0.719):
        return MoonPhase.WANING_GIBBOUS
    elif age < Decimal(0.781):
        return MoonPhase.LAST_QUARTER
    elif age < Decimal(1):
        return MoonPhase.WANING_CRESCENT
