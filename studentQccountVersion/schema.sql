-- créer une table pour que les étudiants se connectent à SQLite
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    numero_etudiant TEXT NOT NULL,
    mail TEXT NOT NULL,
    mot_de_passe TEXT NOT NULL
);