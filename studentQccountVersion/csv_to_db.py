# ce code pour ajouter le fichier csv à la base de données :
import csv
from cs50 import SQL

file_path = "fichier_etudiants.csv" # recuperer la fichier dont on a fourni 

db = SQL("sqlite:///temp_db.db")

with open(file_path, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # le fichier csv a pour colonnes: nom, prenom, numero_etudiant, mot_de_passe, mail
        # la base de données a des colonnes : id, nom, prenom, numero_etudiant, mot_de_passe, mail
         #vérifie si un étudiant avec le même numéro d'étudiant  existe déjà  dans la base de données.
         #  S'il n'existe pas, alors une nouvelle ligne est insérée dans la table 
        if not db.execute("SELECT * FROM students WHERE numero_etudiant = :numero_etudiant", numero_etudiant=row["numero_etudiant"]):
            db.execute("INSERT INTO students (nom, prenom, numero_etudiant, mot_de_passe, mail) VALUES (:nom, :prenom, :numero_etudiant, :mot_de_passe, :mail)", nom=row["nom"], prenom=row["prenom"], numero_etudiant=row["numero_etudiant"], mot_de_passe=row["mot_de_passe"], mail=row["mail"])
