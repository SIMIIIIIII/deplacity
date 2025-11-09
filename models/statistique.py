from deplacity.utils.db import get_db
from deplacity.models.city import get_city_list

def entrees():
    """pre:: -
        post: un dictionnaire avec le nombre d'entrées par table
    """
    db = get_db()
    ville = db.execute("SELECT COUNT(*) FROM ville").fetchone()[0]
    rue = db.execute("SELECT COUNT(*) FROM rue").fetchone()[0]
    vitesse = db.execute("SELECT COUNT(*) FROM vitesse").fetchone()[0]
    v85 = db.execute("SELECT COUNT(*) FROM v85").fetchone()[0]
    trafic = db.execute("SELECT COUNT(*) FROM trafic").fetchone()[0]
    dic = {}
    dic["ville"] = ville
    dic["rue"] = rue
    dic["vitesse"] = vitesse
    dic["v85"] = v85
    dic["trafic"] = trafic
    return dic


def get_number_of_rue():
    """pre: -
        post: liste de nombre de rues par ville
    """
    db = get_db()
    list_postal = get_city_list()
    liste_rue = []
    for postal in list_postal:
        liste_rue.append(db.execute(
            "SELECT COUNT(rue_id) AS nb_rue FROM rue WHERE code_postal=?",
            (postal[0],)).fetchone()[0])
    return liste_rue


def top_ville_cyclabe():
    """pre: -
        post: un dictionnaire qui contient les 3 villes le plus cyclable,
            leurs populations et le nombres des vehicules observé
    """
    db = get_db()
    return db.execute(
        """SELECT v.nom_de_ville, v.population,
        ROUND(SUM(t.nb_vehicules)) AS total_vehicules FROM ville v
        JOIN rue r ON v.code_postal = r.code_postal
        JOIN trafic t ON r.rue_id = t.rue_id
        WHERE t.type_vehicule = ?
        GROUP BY v.code_postal ORDER BY total_vehicules DESC LIMIT 3""",
        ('velo',))