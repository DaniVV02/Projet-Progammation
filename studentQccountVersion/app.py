# une application Web qui demande des identifiants de connexion puis affiche un message de bienvenue si elle est dans la base de données et un autre message si elle ne l'est pas
from flask import Flask, render_template, request, redirect, url_for
from csv import DictReader
from cs50 import SQL
 # connexion a la besa de donnee pour stocker les données dans temp_db.db
db = SQL("sqlite:///temp_db.db") 
# commencer la configuration
app = Flask(__name__) 

# se rendre dans la page de login
@app.route("/")
def index():
    return redirect(url_for("login"))

# renvoyer le contenu HTML généré à partir du fichier "index.html"
@app.route("/home") 
def home():
    return render_template("index.html")
#soumettre  données via un formulaire HTTP POST ou afficher simplement le formulaire via HTTP GET.
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # obtenir les données du formulaire
        numero_etudiant = request.form.get("numero_etudiant")
        mot_de_passe = request.form.get("mot_de_passe")
        # récupérer les données de la base de données dont on a fourni le fichier csv
        data = db.execute("SELECT * FROM students WHERE numero_etudiant = :numero_etudiant", numero_etudiant=numero_etudiant)
        # vérifier si les données sont dans la base de données
        if data:
            # vérifier si le mot de passe est le même que le numéro d'étudiant
            if numero_etudiant == mot_de_passe:
                # demander un nouveau mot de passe
                return render_template("new_password.html", numero_etudiant=numero_etudiant)
            # vérifier si le mot de passe est correcte
            elif data[0]["mot_de_passe"] == mot_de_passe:
                # afficher le message de bienvenue
                return redirect(url_for("home"))
        else:
            return render_template("error.html", message="Utilisateur introuvable")
    
    
@app.route("/new_password", methods=["POST", "GET"])
def new_password():
    if request.method == "GET":
        return render_template("new_password.html")
    else:
        # obtenir les données du formulaire
        numero_etudiant = request.form.get("numero_etudiant")
        mot_de_passe = request.form.get("mot_de_passe")
        confirm_password = request.form.get("confirm_password")
        # vérifier si les mots de passe correspondent
        if mot_de_passe != confirm_password:
            return redirect("/new_password")

        # mettre à jour le mot de passe dans la base de données
        updated = db.execute("UPDATE students SET mot_de_passe = ? WHERE numero_etudiant = ?", mot_de_passe, numero_etudiant)
        print(updated)
        if updated:
            # retour à l'index
            return redirect("/home")
        else:
            return render_template("error.html", message="Erreur lors de la mise à jour du mot de passe")



if __name__ == "__main__":
    app.run(debug=True)

