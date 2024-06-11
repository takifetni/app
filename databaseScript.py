import sqlite3
import bcrypt
# connecting to the database
conn = sqlite3.connect('c:\\Users\\taki\\Desktop\\app\\instance\\flaskr.sqlite')
cursor = conn.cursor()
# Sample data to insert into the tables
etudiants = [
    (12345, 'fares', 'wassim', '20/04/2004' ,'wassim.fares@example.com', 'password1'),
    (12346, 'gati', 'akram', '15/07/2004' ,'gati.akram@example.com', 'password2')
]

modules = [
    ('POO', 6),
    ('THL', 3),
    ('Projet', 6),
    ("System d'information", 3),
    ('Theorie des graphes', 3),
    ("Introduction au systéme d'éxploitation", 3),
    ('Anglais',1)
]

inscriptions = [
    (1, 1, 15.3, 14.7),
    (1, 2, 12.0, 16.5),
    (1, 3, 18.4, 17.2),
    (1, 4, 10.6, 13.1),
    (1, 5, 14.3, 12.4),
    (1, 6, 11.7, 15.9),
    (1, 7, 19.0, 16.3),
    (2, 1, 10.5, 14.8),
    (2, 2, 16.2, 15.6),
    (2, 3, 13.9, 11.4),
    (2, 4, 17.3, 18.5),
    (2, 5, 19.7, 12.8),
    (2, 6, 14.1, 10.7),
    (2, 7, 11.8, 13.3)
]

absences = [
    (1, 1, 2),
    (2, 2, 0)
]

groups = [
    ('Group A',),
    ('Group B',)
]

etudiant_groups = [
    (1, 1),
    (2, 2)
]

admins = [
    ('admin1', 'adminpassword1', 'admin1@example.com'),
    ('admin2', 'adminpassword2', 'admin2@example.com')
]

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Insert data into etudiant table with hashed passwords
for matricule, nom, prenom, email, password in etudiants:
    hashed_password = hash_password(password)
    cursor.execute('INSERT INTO etudiant (matricule, nom, prenom, email, mot_de_passe) VALUES (?, ?, ?, ?, ?)', 
                   (matricule, nom, prenom, email, hashed_password))

# Insert data into other tables
cursor.executemany('INSERT INTO modules (module, coefficient) VALUES (?, ?)', modules)

cursor.executemany('INSERT INTO inscription (etudiant_id, module_id, note_td, note_controle) VALUES (?, ?, ?, ?)', inscriptions)

cursor.executemany('INSERT INTO absences (etudiant_id, module_id, absence_count) VALUES (?, ?, ?)', absences)
cursor.executemany('INSERT INTO groups (nom_group) VALUES (?)', groups)
cursor.executemany('INSERT INTO etudiant_groups (etudiant_id, group_id) VALUES (?, ?)', etudiant_groups)

# Insert data into admin table with hashed passwords
for username, password, email in admins:
    hashed_password = hash_password(password)
    cursor.execute('INSERT INTO admin (username, password, email) VALUES (?, ?, ?)', 
                   (username, hashed_password, email))

# Commit the changes and close the connection
conn.commit()
conn.close()
