from flask import (
    Blueprint, render_template, request, session, redirect, url_for
)
from deplacity.models.city import get_city_list, get_street, get_years, get_months
from deplacity.models.requete import search_trafic_city, get_traffic_by_street
from deplacity.models.full_moon_ratio import get_velo_full_moon

bp = Blueprint('requete', __name__)

list_months = {"Janvier": 1, "Fevrier": 2, "Mars": 3, "Avril": 4, "Mai": 5,
               "Juin": 6, "Juillet": 7, "Aout": 8, "Septembre": 9,
               "Octobre": 10, "Novembre": 11, "Decembre":12}

logos = {
    "Bruxelles": "https://www.bruxelles.be/sites/default/files/logo_vbx.png",
    "Grobbendonk": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Grobbendonk_wapen1.svg/473px-Grobbendonk_wapen1.svg.png",
    "Liege": "https://www.liege.be/cpskinlogo.png/@@images/3689dd3d-cd48-4a74-998d-53c35594d7d1.png",
    "Namur": "https://upload.wikimedia.org/wikipedia/commons/1/18/Logo_Ville_de_Namur.png",
    "Jambes": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Namur_Arms.svg/800px-Namur_Arms.svg.png",
    "Charleroi": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Charleroi_-_logo_2015_-_noir.png/519px-Charleroi_-_logo_2015_-_noir.png",
    "Courtrai": "https://www.kortrijk.be/themes/custom/ocp_theme_kortrijk/assets/dist/img/logo.svg", 
    "beveren": "https://www.beveren.be/themes/custom/calibr8_easytheme/logo.png",
    "Herzele": "https://asset.brandfetch.io/idUuK7wlBb/id8baPFzmu.jpeg?updated=1706661877967"
}

@bp.route('/requetes')
def search():
    return render_template("requetes.html", cities=get_city_list())

@bp.route('/requetes/by_city/general', methods=["POST"])
def request_by_city():
    chosen_city = request.form["ville"]
    session['chosen_city'] = chosen_city
    session['proportions'] = search_trafic_city(chosen_city)
    session['year'] = None
    return redirect(url_for('requete.request_by_city_render'))

@bp.route('/requetes/by_city/by_year', methods=["POST"])
def request_by_city_year():
    chosen_city = session.get('chosen_city')
    if not chosen_city:
        return "City not selected", 400
    year = request.form["year"]
    session['year'] = year
    session['proportions'] = search_trafic_city(chosen_city, year)
    return redirect(url_for('requete.request_by_city_render'))

@bp.route('/requetes/by_city/by_year/by_month', methods=["POST"])
def request_by_city_month():
    chosen_city = session.get('chosen_city')
    if not chosen_city:
        return "City not selected", 400
    month = list_months[request.form["month"]]
    year = session['year']
    session['proportions'] = search_trafic_city(chosen_city, year, month)
    return redirect(url_for('requete.request_by_city_render'))

@bp.route('/requetes/by_city')
def request_by_city_render():
    chosen_city = session.get('chosen_city')
    if session.get("year"):
        session["months"] = get_months(session.get("year"), chosen_city)
    else:
        session["months"] = None

    for city in get_city_list():
        if city["nom_de_ville"] == chosen_city:
            info_city = city
    return render_template(
        "requetes.html",
        cities=get_city_list(),
        proportions=session.get('proportions'),
        streets=get_street(chosen_city),
        info_city=info_city,
        logos=logos,
        list_years=get_years(chosen_city),
        months=session.get('months'),
        moons=get_velo_full_moon(chosen_city)
    )


@bp.route('/requetes/by_street', methods=["POST"])
def request_by_street():
    chosen_city = session.get('chosen_city')
    chosen_street = request.form["rue"]

    for city in get_city_list():
        if city["nom_de_ville"] == chosen_city:
            info_city = city

    return render_template(
        "requetes.html", 
        chosen_street=chosen_street, 
        streets=get_street(chosen_city),
        info_city=info_city,
        days=get_traffic_by_street(chosen_street),
        cities=get_city_list(),
        logos=logos,
        )