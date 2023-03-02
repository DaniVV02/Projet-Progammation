import csv

class Etudiant:
    def __init__(self, nom, prenom, numero_etudiant, mot_de_passe, mail):
        self.nom = nom
        self.prenom = prenom
        self.numero_etudiant = numero_etudiant
        self.mot_de_passe = mot_de_passe
        self.mail = mail

    def modifier_password(self, nouveau_password):
        self.mot_de_passe = nouveau_password
        print("Le mot de passe a été modifié avec succès !")

base_de_donnees = []

# Ouvrir le fichier CSV contenant les informations des étudiants
with open('fichier_etudiants.csv', newline='') as csvfile:
    # Lire le fichier CSV
    reader = csv.DictReader(csvfile)
    # Parcourir chaque ligne du fichier
    for row in reader:
        # Extraire les informations de l'étudiant à partir du fichier CSV
        nom = row['nom']
        prenom = row['prenom']
        numero_etudiant = row['numero_etudiant']
        if not row['mot_de_passe']:
            mot_de_passe = numero_etudiant
            # Utiliser le numéro étudiant par défaut si aucun mot de passe n'est fourni
        else:
            mot_de_passe = row['mot_de_passe']

        if not row['mail'] or row['mail'] != f"{nom.lower()}.{prenom.lower()}@etu.fds.fr" :
            mail = f"{nom.lower()}.{prenom.lower()}@etu.fds.fr"
            #Cela utilise une f-string pour définir l'adresse e-mail par défaut 
            #En convertissant les noms de l'étudiant en minuscules et en les combinant avec le domaine "gmail.com".
        else:
            mail = row['mail']
        
        # Vérifier si l'étudiant existe déjà dans la base de données
        etudiant_existant = False
        for etudiant in base_de_donnees:
            if etudiant.numero_etudiant == numero_etudiant:
                etudiant_existant = True
                break
                
        # Si l'étudiant n'existe pas, le créer avec les informations fournies
        if not etudiant_existant:
            nouvel_etudiant = Etudiant(nom, prenom, numero_etudiant, mot_de_passe, mail)
            base_de_donnees.append(nouvel_etudiant)


        # Demander à l'utilisateur d'entrer son numéro étudiant et son mot de passe actuel
        print("Vous voulez changer votre mot de passe ?")
        reponse = input()
        if reponse == "ui":
            numero_etudiant = input("Entrez votre numéro étudiant : ")
            mot_de_passe_actuel = input("Entrez votre mot de passe actuel : ")

            # Vérifier si les informations sont correctes
            etudiant_trouve = None
            for etudiant in base_de_donnees:
                if etudiant.numero_etudiant == numero_etudiant and etudiant.mot_de_passe == mot_de_passe_actuel:
                    etudiant_trouve = etudiant
                    break

            # Si les informations sont correctes, permettre à l'étudiant de changer son mot de passe
            
            if etudiant_trouve:
                nouveau_password = input("Entrez votre nouveau mot de passe : ")
                etudiant_trouve.modifier_password(nouveau_password)
            else:
                print("Les informations fournies sont incorrectes. Veuillez réessayer.")
        else:
            break
     
# Afficher un message pour confirmer la création des comptes étudiants
print("Les comptes étudiants ont été créés avec succès !")

# Afficher les informations de chaque étudiant dans la base de données
for etudiant in base_de_donnees:
    print(f"Nom : {etudiant.nom}")
    print(f"Prénom : {etudiant.prenom}")
    print(f"Numéro étudiant : {etudiant.numero_etudiant}")
    print(f"Mot de passe : {etudiant.mot_de_passe}")
    print(f"Mail Etudiant : {etudiant.mail}")
    print("-------------------------------")


