from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

connected_users = set()
quiz_results = {}

@app.route('/')
def index():
    return render_template('index2.html')

@socketio.on('connected')
def on_connected():
    connected_users.add(request.sid)
    emit('connected_users', len(connected_users), broadcast=True)

@socketio.on('disconnect')
def on_disconnect():
    connected_users.discard(request.sid)
    emit('connected_users', len(connected_users), broadcast=True)

@socketio.on('quiz_answer')
def on_quiz_answer(answer):
    if answer not in quiz_results:
        quiz_results[answer] = 0
    quiz_results[answer] += 1
    emit('quiz_results', quiz_results, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)

