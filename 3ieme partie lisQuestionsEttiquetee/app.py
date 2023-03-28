from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random

app = Flask(__name__)

# Route pour la page d'accueil
# Route pour la page d'accueil
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

    # Récupération du tag saisi dans le champ input
    tag = request.form['addTag']

    # Insertion du tag dans la base de données
    c.execute("INSERT INTO tag_db (text_tag) VALUES (?)", (tag,))

    # Récupération du dernier tag inséré dans la base de données
    c.execute("SELECT * FROM tag_db WHERE id_tag=?", (c.lastrowid,))
    new_tag = c.fetchone()

    # Commit et fermeture de la connexion
    conn.commit()
    c.close()
    conn.close()

    # Redirection vers la page d'accueil avec le nouveau tag ajouté
    return redirect(url_for('index', new_tag=new_tag) + '?rand=' + str(random.randint(1, 100000)))


# Route pour supprimer un tag
@app.route('/delete_tag/<int:tag_id>', methods=['POST'])
def delete_tag(tag_id):
    # Connexion à la base de données
    conn = sqlite3.connect('source.db', check_same_thread=False)
    c = conn.cursor()

    # Suppression du tag dans la base de données
    c.execute("DELETE FROM tag_db WHERE id_tag=?", (tag_id,))

    # Récupération de tous les tags dans la base de données
    c.execute("SELECT * FROM tag_db")
    tags = c.fetchall()

    # Commit et fermeture de la connexion
    conn.commit()
    c.close()
    conn.close()

    # Redirection vers la page d'accueil avec un paramètre aléatoire pour forcer le rafraîchissement
    return redirect(url_for('index') + '?rand=' + str(random.randint(1, 100000)))

# Route pour la page des questions
# Route pour la page des questions
@app.route('/questions')
def question_list():
    # Connexion à la base de données
    conn = sqlite3.connect('source.db', check_same_thread=False)
    c = conn.cursor()

    # Récupération de toutes les questions dans la base de données
    c.execute("SELECT id_qcm, etiquette ,question, choix_1, choix_2, choix_3, choix_4 FROM qcm")
    questions = c.fetchall()

    # Fermeture de la connexion
    c.close()
    conn.close()

    # Renvoi de la page avec les questions récupérées
    return render_template('listQuestion.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)