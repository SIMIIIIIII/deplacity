from flask import (Blueprint, render_template)
from ..models.statistique import (
    get_number_of_rue,top_ville_cyclabe, entrees)
from ..models.city import get_city_list

bp = Blueprint('statistique', __name__)

@bp.route('/statistique')
def rue_liste():

    cities = get_city_list()
    numbers = get_number_of_rue()
    datas = zip(cities, numbers)
    entree = entrees()
    top3 = top_ville_cyclabe()
    return render_template(
        "statistique.html", datas = datas, entree = entree, top3 = top3)