from flask import Flask, redirect, render_template, request
import string
import random

app = Flask(__name__)

# Page d'accueil pour l'enseignant
@app.route('/')
def teacher():
    return render_template('teacher.html')

# Page pour diffuser la question
@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        # Générer un identifiant unique pour la question
        question_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        # Récupérer la question depuis le formulaire
        question_text = request.form['question']
        # Afficher la question et l'identifiant unique aux étudiants
        return render_template('question.html', question=question_text, question_id=question_id)
    else:
        # Rediriger vers la page d'accueil si la méthode HTTP n'est pas POST
        return redirect('/')

# Page pour les étudiants pour répondre à la question
@app.route('/answer', methods=['GET', 'POST'])
def answer():
    if request.method == 'POST':
        # Récupérer l'identifiant unique depuis le formulaire
        question_id = request.form['question_id']
        # Récupérer la réponse depuis le formulaire
        answer_text = request.form['answer']
        # Afficher un message de confirmation
        return render_template('confirmation.html', question_id=question_id, answer=answer_text)
    else:
        # Rediriger vers la page d'accueil si la méthode HTTP n'est pas POST
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
