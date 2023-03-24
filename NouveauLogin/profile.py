from flask import Blueprint, request, render_template, url_for, flash, make_response, redirect

from flask_login import current_user
from flask_security import login_required

import hashlib
import json

from dbTable import *
import dbOP

profile_blueprint = Blueprint("profile", __name__, template_folder = "templates")

@profile_blueprint.route("/profile/")
@login_required
def profile():
	return render_template("profile.html", name = current_user.name) # NEED CHANGE PARAM


# TAG
@profile_blueprint.route("/profileTag/")
@login_required
def profileTag():
	return json.dumps([i.tag for i in db.session.query(DB_TAG).filter_by(id_usr = current_user.id).all()])


@profile_blueprint.route("/newProfileTag/", methods = ["POST"])
@login_required
def newProfileTag():
	print(make_response("ok", 200))
	tag = request.json["tag"]
	if tag != None and len(tag) < 20:
		dbOP.addTag_USR(db, current_user.id, tag)
		return make_response("ok", 200)
	return make_response("invalid tag size", 400)


# QUESTION
@profile_blueprint.route("/QuestionInfo/<questionId>")
def QuestionInfo(questionId):
	q = db.session.query(DB_QUESTION).filter_by(id = questionId).first()
	if q == None:
		return json.dumps({"status":400})
	r = json.dumps({"id": q.id, "title": q.title, "visibility": q.visibility, "type": q.type, "status":200})
	
	if q.visibility == "public":
		return r
	
	if not current_user.is_authenticated:
		return json.dumps({"status": 400})
	
	#if dbOP.
	return json.dumps({"status": 400})

@profile_blueprint.route("/profileQuestionInfo/")
@login_required
def profileQuestionInfo():
	return json.dumps([{"id": i.id, "title": i.title, "visibility": i.visibility, "type": i.type} for i in db.session.query(DB_QUESTION).filter_by(author = current_user.id).all()])
	

@profile_blueprint.route("/profileQuestionInfo/<usrId>")
def profileQuestionInfoUsr(usrId):
	return json.dumps([i.tag for i in db.session.query(DB_TAG).filter_by(author = usrId).all()])
	
	
@profile_blueprint.route("/newQuestion/", methods = ["POST"])
@login_required
def newQuestion():
	f_visibility = request.json["visibility"]
	f_title = request.json["title"]
	f_type = request.json["type"]
	
	# DEFAULT VALUES
	if f_visibility == None:
		f_visibility = "private"
	
	if f_title == None:
		f_title = "No title"
	
	if f_type == None:
		f_type = "QUIZZ"
	
	if len(f_title) >= 100 or len(f_type) >= 15:
		return make_response("invalid param size", 400)
	
	if f_visibility != "public" and f_visibility != "private" and f_visibility != "restricted":
		return make_response("invalid visibility param", 400)
	
	db.session.add(DB_QUESTION(author = current_user.id, visibility = f_visibility, title = f_title, type = f_type, statement = "", answers = json.dumps([])))
	db.session.commit()
	return make_response("ok", 200)
	
	
@profile_blueprint.route("/newQuestionTag/<questionId>", methods = ["POST"])
@login_required
def newQuestionTag(questionId):
	if l_db.session.query(DB_QUESTION.author).filter_by(id = l_questionId).first().author != current_user.id: # test if user is author
		return make_response("author of question should be user", 400)
		
	tag = request.form['tag']
	if tag != None or len(tag) < 20:
		dbOP.addTag_QUESTION(db, questionId, request.form['tag'])
		return make_response("ok", 200)
	return make_response("invalid tag size", 400)
		
		
		
		
