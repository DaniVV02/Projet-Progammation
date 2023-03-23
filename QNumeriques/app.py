from flask import Flask, jsonify, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('questions.html')


@app.route('/questions', methods=['POST'])
def get_questions():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT question, reponse FROM questions")
    rows = cursor.fetchall()
    questions = []
    for row in rows:
        question = {"question": row[0], "reponse": row[1]}
        questions.append(question)
    conn.close()
    return jsonify(questions)

if __name__ == "__main__":
    app.run()
