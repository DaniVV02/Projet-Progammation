import json
from flask import Flask, render_template, request, redirect, send_file, url_for, flash
from flask_socketio import SocketIO, emit
import random
import string
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import io


app = Flask(__name__)
socketio = SocketIO(app)
app.jinja_env.globals.update(enumerate=enumerate)
connected_users = set()
quiz_results = {}

# Initialisation de la liste des questions et réponses
questions = []
reponses = []

# Page d'accueil pour le quiz
@app.route('/')
def index():
    return render_template('index.html')

# Page pour la connexion en tant qu'étudiant ou professeur
@app.route('/login', methods=['POST'])
def login():
    user_type = request.form['user_type']
    if user_type == 'student':
        return redirect('/student')
    elif user_type == 'professor':
        return redirect('/teacher')
    else:
        return redirect('/')

# Page d'accueil pour les étudiants
@app.route('/student', methods=['GET'])
def student():
    return render_template('student.html', questions=questions)



def normalize_answer(answer):
    # Convertir la réponse en minuscules
    answer = answer.lower()
    # Supprimer les espaces inutiles
    answer = answer.strip()
    return answer

def compare_answers(answer, expected_answers):
    for expected_answer in expected_answers:
        # Normaliser la réponse attendue
        expected_answer = normalize_answer(expected_answer)
        # Calculer le score de similarité entre la réponse de l'étudiant et la réponse attendue
        ratio = fuzz.token_set_ratio(answer, expected_answer)
        # Si le score est supérieur à 75%, considérer la réponse comme valide
        if ratio >= 75:
            return True
    return False

#page pour que l'étudiant réponde et conserve les réponses dans un fichier json 
# Page pour que l'étudiant réponde et conserve les réponses dans un fichier JSON
@app.route('/student/question/<int:question_index>', methods=['GET', 'POST'])
def answer_question(question_index):
    if request.method == 'POST':
        answer = request.form['reponse']
        # Normaliser la réponse
        answer = normalize_answer(answer)
        with open('./reponses.json', 'r') as f:
            data = json.load(f)
        data.setdefault('reponses', []).append(answer)
        with open('./reponses.json', 'w') as f:
            json.dump(data, f, indent=4)
        return redirect(url_for('reponses'))

    question = questions[question_index]
    return render_template('answer_question.html', question=question)


# Route pour afficher les réponses des étudiants sous forme de nuage de mots
@app.route('/reponses')
def reponses():
    with open('./reponses.json', 'r') as f:
        data = json.load(f)
        reponses = data.get("reponses", [])
    text_str = ' '.join(reponses)
    wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=set(STOPWORDS), min_font_size=10).generate(text_str)

    # Enregistrer le nuage de mots dans un fichier image
    wordcloud.to_file("static/img/wordcloud.png")
    
    # Afficher le nuage de mots dans la page HTML
    return render_template('reponses.html', reponses=reponses)


@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

# Page pour créer des questions et des réponses pour les professeurs
@app.route('/ask_questions', methods=['GET', 'POST'])
def ask_questions():
    if request.method == 'POST':
        question = request.form['question']
        options = request.form.getlist('options')
        questions.append({'question': question, 'options': options})
        return redirect(url_for('ask_questions'))

    return render_template('questions.html')

# Page pour créer une question en tant que professeur
@app.route('/teacher/create', methods=['GET', 'POST'])
def create_question():
    if request.method == 'POST':
        question = request.form['question']
        questions.append(question)
        return redirect('/')
    return render_template('create_question.html')

if __name__ == '__main__':
    # Créer le fichier de stock
    app.run(debug=True)
