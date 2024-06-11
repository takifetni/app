
CREATE TABLE IF NOT EXISTS etudiant (
    etudiant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    matricule INTEGER NOT NULL UNIQUE,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    date_de_naissance TEXT NOT NULL,
    email TEXT UNIQUE,
    mot_de_passe TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS modules (
    module_id INTEGER PRIMARY KEY AUTOINCREMENT,
    module TEXT NOT NULL,
    coefficient INTEGER  NOT NULL
);

CREATE TABLE IF NOT EXISTS inscription (
    inscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    etudiant_id INTEGER NOT NULL,
    module_id INTEGER NOT NULL,
    note_td REAL NOT NULL,
    note_controle REAL NOT NULL,
    FOREIGN KEY (etudiant_id) REFERENCES etudiant (etudiant_id),
    FOREIGN KEY (module_id) REFERENCES modules (module_id)
);

CREATE TABLE IF NOT EXISTS absences (
    absence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    etudiant_id INTEGER NOT NULL,
    module_id INTEGER NOT NULL,
    absence_count INTEGER NOT NULL,
    FOREIGN KEY (etudiant_id) REFERENCES etudiant (etudiant_id),
    FOREIGN KEY (module_id) REFERENCES modules (module_id)
);

CREATE TABLE IF NOT EXISTS groups (
    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_group TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS etudiant_groups (
    etudiant_group_id INTEGER PRIMARY KEY AUTOINCREMENT,
    etudiant_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (etudiant_id) REFERENCES etudiant (etudiant_id),
    FOREIGN KEY (group_id) REFERENCES groups (group_id)
);

CREATE TABLE IF NOT EXISTS admin (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

