from datetime import datetime
from deplacity.utils.db import get_db

def search_trafic_city(city: str, year = None, month = None):
    """
    pre: string, le nom de la ville
    post: liste, de dictionnaires avec les moyens de transport comme clé et
        les proportions par population comme valeur 
    """
    db = get_db()
    if year == None and month == None:
        liste_proportion = db.execute(
            """SELECT SUM(pieton) as pi,
            SUM(velo) as ve, SUM(voiture) as vo, SUM(lourd) as lo
            FROM proportion p
            JOIN rue r ON p.rue_id = r.rue_id
            JOIN ville v ON r.code_postal = v.code_postal
            WHERE nom_de_ville=?""",
            (city,)).fetchone()
    elif year != None and month == None:
        liste_proportion = db.execute(
            """SELECT SUM(pieton) as pi,
            SUM(velo) as ve, SUM(voiture) as vo, SUM(lourd) as lo
            FROM proportion p
            JOIN rue r ON p.rue_id = r.rue_id
            JOIN ville v ON r.code_postal = v.code_postal
            WHERE (nom_de_ville=? AND SUBSTR(p.date,1,4)=?)""",
            (city, str(year))).fetchone()
    else:
        if len(str(month)) == 1:
            month = "0" + str(month)
        liste_proportion = db.execute(
            """SELECT SUM(pieton) as pi,
            SUM(velo) as ve, SUM(voiture) as vo, SUM(lourd) as lo
            FROM proportion p
            JOIN rue r ON p.rue_id = r.rue_id
            JOIN ville v ON r.code_postal = v.code_postal
            WHERE (v.nom_de_ville=? AND SUBSTR(p.date,1,4)=? AND SUBSTR(p.date,6,2)=?)""",
            (city, str(year), str(month))).fetchone()
    
    proportions = []
    if liste_proportion["pi"]:
        proportions.append(round(liste_proportion["pi"], 2))
    
    if liste_proportion["ve"]:
        proportions.append(round(liste_proportion["ve"], 2))
    
    if liste_proportion["vo"]:
        proportions.append(round(liste_proportion["vo"], 2))
    
    if liste_proportion["lo"]:
        proportions.append(round(liste_proportion["lo"], 2))
    return proportions


def traffic_proportion(id_rue: int):
    """
    pre: - int, le rue_id
    post: dictionnaire, avec les dates et heures d'observation comme clé et
          avec comme valeur des dictionnaire contenant les moyens de transports
          avec les proportions.
    """
    db = get_db()
    data = db.execute("""SELECT date FROM proportion WHERE rue_id=?""",
                      (id_rue,)).fetchall()
    traffic_data = {}
    for line in data: 

        # Vérifiez si la date et l'heure sont déjà été traitées
        if line[0] not in traffic_data.keys():
            datas = db.execute(
                """SELECT SUM(pieton) AS pi, SUM(velo) AS ve,
                SUM(voiture) AS vo, SUM(lourd) AS lo
                FROM proportion WHERE rue_id=? AND date=?""",
                (id_rue, line[0])).fetchone()
            
            #on verifie si il y a pas des résultats pour cette rue à cette date et à cette heure
            #on enregistre dans le dictionnaire les proportions à la date et l'heure
            if datas is not None:
                traffic_data[line[0]] = {}
                if datas[0] is not None:
                    pi_proportion = float(datas[0])
                    try:
                        traffic_data[line[0]]['pieton'] += pi_proportion
                    except:
                        traffic_data[line[0]]['pieton'] = pi_proportion
            
                if datas[1] is not None:
                    ve_proportion = float(datas[1])
                    try:
                        traffic_data[line[0]]['velo'] += ve_proportion
                    except:
                        traffic_data[line[0]]['velo'] = ve_proportion

                if datas[2] is not None:
                    vo_proportion = float(datas[2])
                    try:
                        traffic_data[line[0]]['voiture'] += vo_proportion
                    except:
                        traffic_data[line[0]]['voiture'] = vo_proportion

                if datas[3] is not None:
                    lo_proportion = float(datas[3])
                    try:
                        traffic_data[line[0]]['lourd'] += lo_proportion
                    except:
                        traffic_data[line[0]]['lourd'] = lo_proportion
    return traffic_data


def week_days(traffic_data: dict, city_population: int):
    """pre: -dictionnaire, avec les dates et heures d'observation comme clé et
            avec comme valeur des dictionnaire contenant les moyens de
            transports avec les proportions
            - entier positif, la population de la ville
        post: dictionnaire avec comme clés, les jours de la semaine avec comme
            valeur des dictionnaires contenant les moyens des transports et
            leurs proportions
    """
    all_days = {}
    for dates in traffic_data:
        day = datetime.fromisoformat(str(dates)[:-1]) #date format datetime
        day_of_week = day.strftime("%A") #on determine le jour de la semaine

        if day_of_week not in all_days:
            all_days[day_of_week] = {}

        for trans in ['velo', 'pieton', 'voiture', 'lourd']:
            if trans in traffic_data[dates]:
                try:
                    all_days[day_of_week][trans] += traffic_data[dates][trans]
                except:
                    all_days[day_of_week][trans] = traffic_data[dates][trans]
    
    for jour in all_days:
        for trans in ['velo', 'pieton', 'voiture', 'lourd']:
            if trans in all_days[jour]:
                all_days[jour][trans] = str(round(
                    all_days[jour][trans] * (100 / city_population), 2)) + "%"
    return all_days


def get_traffic_by_street(street: str):
    """pre: str, le nom de la rue
    post: dict, un dictionnaire contenant la proportion de tout le moyen de
      transport par jour de la semaine
    """
    db = get_db()
    
    # Obtenez la population de la ville
    rue_population = db.execute(
        """SELECT r.rue_id AS id_rue, v.population AS pop FROM ville v
        JOIN rue r ON v.code_postal = r.code_postal
        WHERE nom_de_rue = ?""", (street,)).fetchone()
    
    city_population = rue_population['pop']
    id_rue = rue_population['id_rue']
    
    traffic_data = traffic_proportion(id_rue)
    all_days = week_days(traffic_data, city_population)
    
    all_days["Lundi"] = all_days.pop("Monday")
    all_days["Mardi"] = all_days.pop("Tuesday")
    all_days["Mercredi"] = all_days.pop("Wednesday")
    all_days["Jeudi"] = all_days.pop("Thursday")
    all_days["Vendredi"] = all_days.pop("Friday")
    all_days["Samedi"] = all_days.pop("Saturday")
    all_days["Dimanche"] = all_days.pop("Sunday")

    return all_days