import os
from flask import (Blueprint, render_template, redirect, url_for, request)
from ..models.city import get_city_list, City, search_by_postal_code
from dotenv import load_dotenv

load_dotenv()

connected = False
users = os.getenv('ADMIN_USERNAME', 'Deplacity')
pass_word = os.getenv('ADMIN_PASSWORD', 'G19DeplacityUcl')
affichier_city = False
bp = Blueprint('admin', __name__)

# Definir les routes
@bp.route('/admin')
def admin():
    global affichier_city
    msg = "Afficher la liste de villes"
    affichier_city = False
    if connected == False:
        return redirect(url_for('admin.connexion', state = None))
    else:
        return render_template('admin.html', msg = msg)


@bp.route('/admin/connexion')
def connexion():
    state = request.args.get('state')
    if state == None:
        return render_template("connexion.html", state = state)
    else:
        return render_template("connexion.html", state = state)


@bp.route('/admin/connexion_request', methods = ['POST'])
def connexion_request():
    global connected
    user = request.form['user']
    password = request.form['password']

    if user == users and password == pass_word:
        connected = True
        
        return redirect(url_for('admin.admin'))
    else:
        return redirect(url_for('admin.connexion', state = "failed"))


@bp.route('/admin/villes')
def city_list():
    global affichier_city
    
    if affichier_city == False:
        msg = "Cacher la liste de villes"
        affichier_city = True
        cities = get_city_list()
        return render_template(
            'admin.html', cities = cities, villes = affichier_city, msg = msg)
    else:
        msg = "Afficher la liste de villes"
        affichier_city = False
        return render_template('admin.html', msg = msg)


@bp.route('/admin/create', methods=["POST"])
def city_create():
    global affichier_city
    affichier_city = True
    postal_code = request.form["postal_code"]
    if not search_by_postal_code(int(postal_code)):
        name = request.form["name"]
        population = request.form["population"]
        city = City(name, population, postal_code)
        city.save()
    return redirect(url_for("admin.city_list"))


@bp.route('/admin/delete/<int:postal_code>')
def city_delete(postal_code):
    global affichier_city
    affichier_city = True
    city = City.get(postal_code)
    if city:
        city.delete()
    return redirect(url_for("admin.city_list"))