from flask import Flask, request, render_template

app = Flask(__name__ ,template_folder="templates")

questions = []

def add_question(question, options, rep_correcte):
    questions[question]=  {"options": options, "correct_answer": correct_answer}
    

def erase_question(index):
    if index in questions:
        del questions[index]

def save_questions(file_name):
    with open(file_name, "w") as file:
        for question in questions:
            file.write(question + "\n")

@app.route("/")
def main_page():
    return render_template("questions.html")

@app.route("/add", methods=["POST"])
def add():
    question = request.form(question)
    options = request.form.getlist(options)
    rep_correcte = request(rep_correcte)
    add_question(question, options, rep_correcte)

    return render_template("questions.html")


@app.route("/erase", methods=["POST"])
def erase():
    index = int(request.form["index"])
    erase_question(index)
    return render_template("questions.html")

@app.route("/save", methods=["POST"])
def save():
    file_name = request.form["file_name"]
    save_questions(file_name)
    return render_template("questions.html")

if __name__ == "__main__":
    app.run()
