from flask import (Blueprint, render_template)

bp = Blueprint('home', __name__)

 # Definir les routes
@bp.route('/')
def home_page():
    return render_template("index.html")