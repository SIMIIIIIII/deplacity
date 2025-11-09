from deplacity.utils.moon_utils import (age, phase, MoonPhase)
from deplacity.utils.db import get_db
from datetime import datetime

def biker_in_city(city: str):
    """
    pre: string, le nom de la ville
    on recupère dans la base de données la liste de nombre de velos observés
    dans la ville passée en argument et la date d'observation.
    post: une liste de tuples qui contiennent la date d'observation et
        le nombre de cyclistes
    """
    db = get_db()
    city_date_velo = db.execute(
        """SELECT p.date AS date, p.velo AS nombre_de_velo
        FROM proportion p
        JOIN rue r ON p.rue_id = r.rue_id
        JOIN ville v ON r.code_postal = v.code_postal
        WHERE v.nom_de_ville = ?
        GROUP BY p.date;""", (city,)).fetchall()
    return city_date_velo


def day_per_year(city_date_velo: list):
    """
    pre: une liste de tuples
    post: un dictionnaire, dont les clés sont les années observées et les
        valeurs sont les nombres de jours observés dans l'année
    """
    dates = []
    for d in city_date_velo:
        dates.append(d[0])

    datetime_format = []
    days = []

    #on met la date au format datetime et au format date
    for d in dates:
        d = datetime.fromisoformat(d[:-1])
        datetime_format.append(d)
        day = d.date()
        if day not in days:
            days.append(day)

    #On enregistre le nombre de jour oubservé par année dans le dictionnaire
    days_per_year = {}
    for d in days:
        if d.year in days_per_year:
            days_per_year[d.year] += 1
        else:
            days_per_year[d.year] = 1
    return days_per_year


def get_velo_full_moon(city: str):
    """
    pre: un string, le nom d'une ville
        cherche dans la base de donnée la moyenne de cyclistes observés par
        jour, dans l'année pendant les jour de pleines nuit et les autres jour
    post: un dictionnaire dont les clés sont les années et les valeurs sont
        des dictionnaires contenant le ration pour le jours de pleine lune
        el les autre jours
    """
    city_date_velo = biker_in_city(city)
    days_per_year = day_per_year(city_date_velo)
    
    dic_ratio = {}

    for element in city_date_velo:
        day = datetime.fromisoformat(element[0][:-1])
        year = day.year

        #On cherche la phase de la lune de la date
        #et on verifie si c'est la pleine lune
        #on additionne les nombres des velos les hours de pleine lune entre eux
        #et on regroupe les autres jours entre eux
        if phase(age(day)) == MoonPhase.FULL_MOON:
            try:
                dic_ratio["Full moon"] += element[1]
            except:
                dic_ratio["Full moon"] = element[1]
        else:
            try:
                dic_ratio["Other days"] += element[1]
            except:
                dic_ratio["Other days"] = element[1]

    proportions = []
    proportions.append(round(dic_ratio["Full moon"], 2 ))
    proportions.append(round(dic_ratio["Other days"], 2))

    return proportions