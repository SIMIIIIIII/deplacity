from flask import (
    Blueprint, render_template, redirect, url_for, request)
import json
from ..models.requete import search_trafic_city

coordonnee = {
    "Bruxelles": [50.8503, 4.3517],
    "Liege": [50.6450944, 5.5736112],
    "Grobbendonk": [51.1919904, 4.7385027],
    "Namur": [50.4665284, 4.8661892],
    "Jambes": [50.4563673, 4.871877],
    "Charleroi": [50.4116233, 4.444528],
    "Courtrai": [50.8276429, 3.2659884], 
    "beveren": [51.212885, 4.2490813],
    "Herzele":[50.8699917, 3.8988564]
    }

info = {}

bp = Blueprint('citymap', __name__)

# Definir les routes
@bp.route('/citymap')
def deplacity():
    for ville in coordonnee:
        info[ville] = search_trafic_city(ville)
    return render_template(
        "citymap.html",
        coordonnee=json.dumps(coordonnee),
        info_cities=json.dumps(info)
        )