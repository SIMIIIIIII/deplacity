from deplacity.utils.db import get_db

def get_city_list():
    """
    pre: -
    post: le dictionnaire contenant les villes dans la base de données
        trié par code postal et toutes leurs informations
    """
    db = get_db()
    return db.execute('SELECT * FROM ville ORDER BY code_postal')

def search_by_postal_code(code_postal: int):
    """
    pre: un entier positif
    post: la ville et toutes ces informations dans un dictionnaire
    """
    db = get_db()
    return db.execute(
        'SELECT * FROM ville WHERE code_postal=?', (code_postal,)).fetchall()

def search_by_city(city: str):
    db = get_db()
    return db.execute("SELECT * FROM ville WHERE nom_de_ville=?", (city,))

def get_street(city: str):
    db = get_db()
    postal_code = db.execute(
        "SELECT code_postal FROM ville WHERE nom_de_ville=?",
        (city,)).fetchone()
    return db.execute(
        "SELECT nom_de_rue FROM rue WHERE code_postal=?",
        (postal_code[0],)).fetchall()

def get_years(city: str):
    db = get_db()
    years = db.execute(
        """SELECT t.date AS date
        FROM trafic t
        JOIN rue r ON t.rue_id=r.rue_id
        JOIN ville v ON r.code_postal=v.code_postal
        WHERE nom_de_ville=?
        """, (city,)).fetchall()
    list_date = []
    for date in years:
        if int(date["date"][0:4]) not in list_date:
            list_date.append(int(date["date"][0:4]))
    return list_date

def get_months(year: int, city:str):
    list_months = {1: "Janvier", 2: "Fevrier", 3: "Mars", 4: "Avril", 5:"Mai",
                   6: "Juin", 7:"Juillet", 8: "Aout", 9: "Septembre",
                   10: "Octobre", 11: "Novembre", 12: "Decembre"}
    db = get_db()
    months = db.execute(
        """SELECT SUBSTR(date, 6, 2) AS date
        FROM trafic t
        JOIN rue r ON t.rue_id=r.rue_id
        JOIN ville v ON r.code_postal=v.code_postal
        WHERE (SUBSTR(t.date, 1, 4)=? AND v.nom_de_ville=?)
        """, (str(year), city,)).fetchall()
    l=[]
    for month in months:
        if list_months[int(month["date"])] not in l:
            l.append(list_months[int(month["date"])])
    return l

class City:
    def __init__(self, name, population, postal_code = None):
        self.name = name
        self.postal_code = postal_code
        self.population = population

    def delete(self):
        db = get_db()
        
        db.execute(
            """DELETE FROM proportion 
            WHERE rue_id IN (
                SELECT rue_id 
                FROM rue r
                WHERE code_postal=?)""",
                (self.postal_code,)
                )
        db.execute(
            """DELETE FROM v85
            WHERE rue_id IN (
                SELECT rue_id 
                FROM rue r
                WHERE code_postal=?)""",
                (self.postal_code,)
                )
        db.execute(
            """DELETE FROM trafic
            WHERE rue_id IN (
                SELECT rue_id 
                FROM rue r
                WHERE code_postal=?)""",
                (self.postal_code,)
                )
        db.execute(
            """DELETE FROM vitesse 
            WHERE rue_id IN (
                SELECT rue_id 
                FROM rue r
                WHERE code_postal=?)""",
                (self.postal_code,)
                )
        db.execute(
            """DELETE FROM rue 
            WHERE code_postal=?""",
                (self.postal_code,)
                )
       
        db.execute(
            """ DELETE FROM ville
            WHERE code_postal=?""",
            (self.postal_code,)
        )
        db.commit()

    def save(self):
      db = get_db()
      db.execute("""INSERT INTO ville(code_postal,nom_de_ville,population )
                 VALUES(?, ?, ?)""",
                 ( self.postal_code,self.name,self.population,))
      db.commit()
    
    @staticmethod
    def get(postal_code: int): 
        db = get_db()
        data = db.execute('SELECT * FROM ville WHERE code_postal=?',
                          (postal_code,)).fetchone()

        if data is None:
            return None
        else:
            return City(data[1], data[2], data[0])