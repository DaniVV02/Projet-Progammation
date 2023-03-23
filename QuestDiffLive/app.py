from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit

import random
import string

app = Flask(__name__)

socketio = SocketIO(app)

connected_users = set()
quiz_results = {}

# Initialisation de la liste des questions et réponses
questions = []

@app.route('/')
def base():
    return render_template('base.html')

#@app.route('/')
#def index():
  #  return render_template('index.html')

@socketio.on('connected')
def on_connected():
    connected_users.add(request.sid)
    emit('connected_users', len(connected_users), broadcast=True)

@socketio.on('disconnect')
def on_disconnect():
    connected_users.discard(request.sid)
    emit('connected_users', len(connected_users), broadcast=True)

  
@app.route('/login', methods=['POST'])
def login():
    user_type = request.form['user_type']
    if user_type == 'student':
        return redirect('/diffusion')
    elif user_type == 'professor':
        return redirect('/index')
    else:
        return redirect('/')
    

# Page de création des questions et des réponses pour les professeurs

@app.route('/questions', methods=['GET', 'POST'])
def create_questions():
    if request.method == 'POST':
        question = request.form['question']
        options = request.form.getlist('options')
        questions.append({'question': question, 'options': options})
        return redirect(url_for('create_questions'))

    return render_template('questions.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', questions=questions)

# Page de diffusion des questions et des options pour les étudiants
@app.route('/diffusion', methods=['GET'])
def diffusion():
    return render_template('diffusion.html', questions=questions)

# Page de soumission des réponses pour les étudiants
@app.route('/reponses', methods=['POST'])
def reponses():
    reponses = request.form.to_dict()
    return render_template('reponses.html', reponses=reponses)

@socketio.on('quiz_answer')
def on_quiz_answer(answer):
    if answer not in quiz_results:
        quiz_results[answer] = 0
    quiz_results[answer] += 1
    emit('quiz_results', quiz_results, broadcast=True)



if __name__ == '__main__':
    app.run(debug=True)