DROP TABLE IF EXISTS ville;
CREATE TABLE IF NOT EXISTS ville(
    code_postal INTEGER PRIMARY KEY NOT NULL,
    nom_de_ville TEXT,
    population INTEGER
);

DROP TABLE IF EXISTS rue;
CREATE TABLE IF NOT EXISTS rue(
    rue_id INTEGER PRIMARY KEY NOT NULL,
    nom_de_rue TEXT NOT NULL,
    code_postal INTEGER NOT NULL,
    FOREIGN KEY("code_postal") REFERENCES "ville"("code_postal")
);

DROP TABLE IF EXISTS vitesse;
CREATE TABLE IF NOT EXISTS vitesse(
    rue_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    tranche_de_vitesse INTEGER NOT NULL,
    proportion REAL NOT NULL ,
    FOREIGN KEY("rue_id") REFERENCES "rue" ("rue_id"),
    PRIMARY KEY (rue_id, date, tranche_de_vitesse)
);

DROP TABLE IF EXISTS v85;
CREATE TABLE IF NOT EXISTS v85(
    rue_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    v85 REAL,
    PRIMARY KEY ("rue_id", "date"),
    FOREIGN KEY ("rue_id") REFERENCES rue("rue_id")
);

DROP TABLE IF EXISTS trafic;
CREATE TABLE IF NOT EXISTS trafic (
    rue_id INTEGER NOT NULL,
    date TEXT  NOT NULL,
    type_vehicule TEXT  NOT NULL,
    nb_vehicules INTEGER  NOT NULL,
    PRIMARY KEY (rue_id, date, type_vehicule),
    FOREIGN KEY (rue_id) REFERENCES rue(rue_id)
);

DROP TABLE IF EXISTS proportion;
CREATE TABLE IF NOT EXISTS proportion (
    rue_id INTEGER NOT NULL,
    date TEXT  NOT NULL,
    pieton REAL,
    velo REAL,
    voiture REAL,
    lourd REAL,
    PRIMARY KEY (rue_id, date),
    FOREIGN KEY (rue_id) REFERENCES rue(rue_id)
);

