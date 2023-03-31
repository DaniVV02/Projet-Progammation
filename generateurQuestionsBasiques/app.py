from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random

app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/')
def index():
    # Connexion à la base de données
    conn = sqlite3.connect('source.db', check_same_thread=False)
    c = conn.cursor()
    
    # Récupération de tous les tags dans la base de données
    c.execute("SELECT * FROM tag_db")
    tags = c.fetchall()
    
    # Fermeture de la connexion
    c.close()
    conn.close()
    
    # Renvoi de la page avec les tags récupérés
    return render_template('index.html', tags=tags)


# Route pour ajouter un tag
@app.route('/add_tag', methods=['POST'])
def add_tag():
    # Connexion à la base de données
    conn = sqlite3.connect('source.db', check_same_thread=False)
    c = conn.cursor()

    # Récupération de la valeur saisie pour le tag
    tag_name = request.form['tag_name']

    # Ajout du tag dans la base de données
    c.execute("INSERT INTO tag_db (tag_name) VALUES (?)", (tag_name,))
    conn.commit()

    # Fermeture de la connexion
    c.close()
    conn.close()

    # Redirection vers la page d'accueil
    return redirect(url_for('index'))

# Route pour la liste des questions
@app.route('/question_list')
def question_list():
    # Connexion à la base de données
    conn = sqlite3.connect('source.db', check_same_thread=False)
    c = conn.cursor()

    # Récupération de toutes les questions dans la base de données
    c.execute("SELECT * FROM qcm")
    questions = c.fetchall()

    # Fermeture de la connexion
    c.close()
    conn.close()

    # Renvoi de la page avec les questions récupérées
    return render_template('listQuestion.html', questions=questions)

# Route pour générer des sujets
@app.route('/generer_sujets', methods=['GET', 'POST'])
def generer_sujets():
    nb_sujets = 0
    if request.method == 'POST':
        nb_sujets = int(request.form['GQ'])
        nb_questions_java = int(request.form['inp_JAVA'])
        nb_questions_compilation = int(request.form['inp_compilation'])
        nb_questions_php = int(request.form['inp_PHP'])
        nb_questions_python = int(request.form['inp_python'])

        # Connexion à la base de données
        conn = sqlite3.connect('source.db', check_same_thread=False)
        c = conn.cursor()

        # Récupération des questions dans la base de données
        c.execute("SELECT id_qcm, etiquette, question, choix_1, choix_2, choix_3, choix_4 FROM qcm")
        questions = c.fetchall()

        # Fermeture de la connexion
        c.close()
        conn.close()

        # Génération des sujets
        sujets = []
        while len(sujets) < nb_sujets:
            sujet = {}
            sujet["JAVA"] = random.sample(questions, nb_questions_java)
            sujet["id_compilation"] = random.sample(questions, nb_questions_compilation)
            sujet["PHP"] = random.sample(questions, nb_questions_php)
            sujet["python"] = random.sample(questions, nb_questions_python)
            if all(sujet != s for s in sujets):
                sujets.append(sujet)

        # Renvoi de la page avec les sujets générés
        return render_template('sujetsGeneres.html', sujets=sujets)

    #
if __name__ == '__main__':
    app.run(debug=True)