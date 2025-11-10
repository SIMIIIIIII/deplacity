import csv
from .db import get_db
import os

def read_csv_file():
    """pre: -
        post: liste qui contient chaque ligne du fichier comme élément 
            de la liste
    """
    current_dir = os.path.dirname(__file__)    
    
    csv_file_path = os.path.join(os.path.dirname(current_dir), "Deplacity.csv")
    data = []
    with open(csv_file_path, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for line in csv_reader:
            data.append(line)
    return data


def populations(ville: str):
    """
        pre: str, le nom de la ville
        post: int, la population de la ville passée en argument
    """
    return {"Liege":198098, "Bruxelles":198390, "Namur":115627,
         "Charleroi":205185, "Grobbendonk":11605, "Herzele":18930,
         "Jambes":20125, "Courtrai": 80258, "beveren":51001}[ville]


def fill_ville(postal: int, nom_ville: str, db):
    """pre: - int, le code postal d'une ville
            - str, le nom de la ville
        post:ecrit dans la table ville la ville, son code postal et sa population

    """
    
    liste_postal = db.execute("SELECT * FROM ville WHERE code_postal=?",
                              (postal,)).fetchall()
    #on evite les doublons
    if  liste_postal == []:
        population = populations(nom_ville)
        db.execute(
            """INSERT INTO ville(code_postal,nom_de_ville,population )
            VALUES(?, ?, ?)""", (postal, nom_ville, population,))
        


def fill_rue(rue_id: int, nom_rue: str, postal: int, db):
    """pre: - int, le rue id
            - str, le nom de la rue
            - int, le code postal de la ville
        post: enregiste dans la table rue le nom, le id et code postal
            de la rue
    """
    
    liste_rue = db.execute(
        "SELECT * FROM rue WHERE rue_id=?", (rue_id,)).fetchall()
    
    #on evite les doublons
    if  liste_rue == []:
        db.execute(
            "INSERT INTO rue(rue_id,nom_de_rue,code_postal) VALUES(?, ?, ?)",
            (rue_id, nom_rue, postal,))
        


def fill_vitesse(
        lourd: float, voiture: float, velo: float,
        hist2: str, rue_id: int, date: str, db):
    """pre: - 3 float, le nombre de vehicules lourds, le vehicule normaux
            et les velos observés
            - str, la liste des tranches des vitesses
            - int, le rue_id
            - str, la date de l'observation
        post: enregistre les données passées en arguments dans la table vitesse 
    """
    
    s = hist2[1:-1]
    hist2 = s.split(",") #on traduit la chaine de caractères en liste
    values_to_insert = []

    for i, t in enumerate(hist2):
        if float(t) != 0:
            tranche = i * 10
            proportion = float(t) / (float(lourd)+float(voiture)+float(velo))

            liste_vitesse = db.execute(
                """SELECT * FROM vitesse WHERE rue_id=? AND date=? AND
                tranche_de_vitesse=?""", (rue_id, date, tranche)).fetchall()
            
            #on verifie les doublons
            if not liste_vitesse:
                #on regroupe les données pour les enregistrer en groupe
                values_to_insert.append((rue_id, date, tranche, proportion))

    #on enregistre les données
    if values_to_insert:
        db.executemany(
            """INSERT INTO vitesse(
                rue_id, date, tranche_de_vitesse, proportion)
              VALUES (?, ?, ?, ?)""", values_to_insert)


def fill_v85(rue_id: int, date: str, v85: str, db):
    """pre: - int, le rue_id
            - str, la date de l'observation
            - str, une estimation de la limite de vitesse qui est respectée
            par 85% des usagers de la route
        post: enregistre les données passées en arguments dans la table v85
    """
    if v85 != "":
        v85 = float(v85)
    liste_v85 = db.execute(
        'SELECT * FROM v85 WHERE (rue_id=? AND date=?)',
        (rue_id, date,)).fetchall()
    
    #on verifie les doublons
    if liste_v85 == []:
        db.execute("INSERT INTO v85(rue_id,date,v85) VALUES(?, ?, ?)",
                   (rue_id,date, v85,))


def fill_trafic(
        lourd: float, voiture: float, velo:float, rue_id: str, date:str, db):
    """pre: - 3 float, le nombre de vehicules lourds, le vehicule normaux
            et les velos observés
            - str, le rue_id
            - str, la date de l'observation
        post - enregistre les données passées en arguments dans la table trafic
    """
    list_vehicule = [lourd, voiture, velo]
    list_veu = ["lourd", "voiture", "velo"]
    for i,vehicule in enumerate(list_vehicule):
        if float(vehicule) != 0:
            type_vehicule = list_veu[i]
            nb_vehicules = vehicule
            liste_trafic = db.execute(
                """SELECT * FROM trafic
                WHERE (rue_id=? AND date=? AND type_vehicule=?)
                """, (rue_id, date, type_vehicule,)).fetchall()
            if liste_trafic == []:
                db.execute(
                    """INSERT INTO trafic(
                        rue_id, date, type_vehicule, nb_vehicules)
                    VALUES(?, ?, ?, ?)""",
                    (rue_id, date, type_vehicule, nb_vehicules,))
                


def fill_proportion(
        lourd: float, voiture: float, velo: float,
        pieton: float, rue_id: int, date: str, db):
    """pre: - 4 float, le nombre de vehicules lourds, le vehicule normaux,
            les velos et les pietons observés
            - str, le rue_id
            - str, la date de l'observation
        post - enregistre les données passées en arguments dans la table trafic
    """
   
    liste_proportion = db.execute(
        "SELECT * FROM proportion WHERE (rue_id=? AND date=?)",
        (rue_id, date,)).fetchall()
    
    if liste_proportion == []:
        
        db.execute(
            """INSERT INTO proportion(rue_id,date,pieton,velo, voiture,lourd)
            VALUES(?, ?, ?, ?, ?, ?)""",
            (rue_id, date, pieton, velo, voiture, lourd,))
        


def write_in_db():
    """pre: -
    post: ecrit le contenu du fichier csv dansles tables de la database
    """
    # Lecture des données à partir du fichier CSV
    csv_data = read_csv_file()
    db = get_db()
    for line in csv_data:
        nom_ville = line["nom_de_ville"]
        date = str(line["date"])
        postal = int(line["code_postal"])
        nom_rue = line["nom_de_rue"]
        rue_id = int(line["rue_id"])
        lourd = float(line["lourd"])
        voiture = float(line["voiture"])
        velo = float(line["velo"])
        hist2 = line["histogramme_0_a_120plus"]
        v85 = line["v85"]
        pieton = float(line["pieton"])     
        fill_ville(postal, nom_ville, db)
        fill_rue(rue_id, nom_rue, postal, db)
        fill_vitesse(lourd, voiture, velo, hist2, rue_id, date, db)
        fill_v85(rue_id, date, v85, db)
        fill_trafic(lourd, voiture, velo, rue_id, date, db)
        fill_proportion(lourd, voiture, velo, pieton, rue_id, date, db)
    db.commit()