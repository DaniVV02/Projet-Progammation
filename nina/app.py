import json
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import random
import string

app = Flask(__name__)
socketio = SocketIO(app)

connected_users = set()
quiz_results = {}

app.jinja_env.globals.update(enumerate=enumerate)

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

# Page pour répondre à une question spécifique
# @app.route('/student/question/<int:question_index>', methods=['GET', 'POST'])
# def answer_question(question_index):
#     if request.method == 'POST':
#         answer = request.form['answer']
#         with open(f'answers_{question_index}.txt', 'a') as f:
#             f.write(answer + '\n')
#         return redirect('/')  
#     question = questions[question_index]
#     return render_template('answer_question.html', question=question)

#page pour que letudiant repond et conserve les reponses dans un fichier  json 
@app.route('/student/question/<int:question_index>', methods=['GET', 'POST'])
def answer_question(question_index):
    if request.method == 'POST':
        answer = request.form['reponse']
        objet_= {
            'answer1' : None 
        }
        with open('./base_question.json', 'r') as f:
            data = json.load(f) 
            with open('./base_question.json','w') as file:
                objet_['answer1'] = answer 
                data["answer"] = objet_        
                json.dump(data,file,indent=4)            
        with open('./base_question.json', 'r') as f:
            data = json.load(f)
            
            reponses.append(data["answer"]["answer1"])
            
        return render_template('/reponses.html',reponses=reponses)  
    question = questions[question_index]
    return render_template('answer_question.html', question=question)

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
    app.run(debug=True)
