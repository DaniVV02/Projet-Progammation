from flask import Blueprint, request, render_template, url_for, flash, make_response, redirect

from flask_login import current_user
from flask_security import login_required

import hashlib
import json

from dbTable import *
import dbOP
import login

profile_blueprint = Blueprint("profile", __name__, template_folder = "templates")

@profile_blueprint.route("/profile/")
@login_required
def profile():
	return redirect(url_for("profile.profile") + "/" + str(current_user.id))
	
@profile_blueprint.route("/profile/<usrId>", methods=['POST'])
@login_required
def diffusionQuestions():
    user_type = request.form['user_type']
    if user_type == 'student':
        return redirect(url_for('diffusion.diffusion'))
    elif user_type == 'professor':
        return redirect(url_for('index.index'))
    else:
        return redirect('/profile/<usrId>')


@profile_blueprint.route("/profile/<usrId>")
def seeProfile(usrId):
	v_usr = db.session.query(DB_USR).filter_by(id = usrId).first()
	if v_usr == None:
		return render_template("access_denied.html")

	if current_user.is_authenticated:
		if (usrId == str(current_user.id)):
			tmp_on_profile = "true"
		else:
			tmp_on_profile = "false"

		return render_template("profile.html", visit_name = v_usr.name, visit_surname = v_usr.surname, visit_id = usrId,
			on_profile = tmp_on_profile, is_connected = True,
			usr_name = current_user.name, usr_surname = current_user.surname, usr_email = current_user.email, usr_id = current_user.id)
	
	return render_template("profile.html", visit_name = v_usr.name, visit_surname = v_usr.surname, visit_id = usrId, on_profile = "false", is_connected = False)

#Route por créer un nouveau mot de passe
@profile_blueprint.route("/newPassword/", methods=["POST"])
@login_required
def newPassword():
	f_password = login.hashPassword(request.json["password"])
	f_newpassword = login.hashPassword(request.json["newpassword"])

	obj = db.session.query(DB_USR).filter_by(id = current_user.id, password = f_password).first()
	if obj == None:
		return make_response("invalid password", 400)
	
	obj.password = f_newpassword
	db.session.commit()
	return make_response("password changed", 200)

# TAG (étiquettes)
@profile_blueprint.route("/profileTag/<usrId>")
def profileTag(usrId):
	return json.dumps([i.tag for i in db.session.query(DB_TAG).filter_by(id_usr = usrId).all()])

#Route pour ajouter un tag
@profile_blueprint.route("/newProfileTag/", methods = ["POST"])
@login_required
def newProfileTag():
	f_tag = request.json["tag"]
	if f_tag != "" and len(f_tag) < 20:
		print(db.session.query(DB_TAG).filter_by(id_usr = current_user.id, tag = f_tag).first() == None)
		if db.session.query(DB_TAG).filter_by(id_usr = current_user.id, tag = f_tag).first() == None:
			dbOP.addTag_USR(db, current_user.id, f_tag)
			return make_response("ok", 200)
		return make_response("already existing Tag", 400)
	return make_response("invalid tag", 400)

#Route pour supprimer un tag
@profile_blueprint.route("/deleteProfileTag/", methods = ["POST"])
@login_required
def deleteProfileTag():
	f_tag = request.json["tag"]
	if db.session.query(DB_TAG).filter_by(id_usr = current_user.id, tag = f_tag).first() != None:
		dbOP.deleteTag_USR(db, current_user.id, f_tag)
		return make_response("ok", 200)
	return make_response("tag not found", 400)


# DOCUMENT
@profile_blueprint.route("/DocumentInfo/", methods=["POST"])
def DocumentInfo():
	f_documentId = request.json["id"]
	f_id = None
	if current_user.is_authenticated:
		f_id = current_user.id

	if not dbOP.canUsrSeeDoc(db, f_id, f_documentId):
		return make_response("invalid param", 400)
	
	q = db.session.query(DB_DOC).filter_by(id=f_documentId).first()

	r = {"id": q.id, "title": q.title, "visibility": q.visibility, "author": q.author, "questions": [], "usr": []}

	for i in db.session.query(DB_DOC_QUESTION.id_question).filter_by(id_doc=f_documentId).all():
		if dbOP.getUsrPermQUESTION(db, f_id, i.id_question)["read"]:
			t_obj = db.session.query(DB_QUESTION.id, DB_QUESTION.visibility, DB_QUESTION.title).filter_by(id=i.id_question).first()
			r["questions"].append({"title":t_obj.title, "id": t_obj.id, "visibility": t_obj.visibility})
	
	if r["visibility"] == "restricted":
		for i in db.session.query(DB_USR_DOC).filter_by(id_doc=f_documentId, id_usr=f_id).all():
			t_obj = db.session.query(DB_USR).filter_by(id=i.id_usr).first()
			f["usr"].append({"id":t_obj.id, "name":t_obj.name, "surname":t_obj.surname})
	
	return json.dumps(r)
	
	


@profile_blueprint.route("/profileDocumentInfo/<usrId>")
def profileDocumentInfo(usrId):
	if db.session.query(DB_USR).filter_by(id = usrId) == None:
		return make_response("invalid id", 400)

	r = []

	if current_user.is_authenticated:
		if str(current_user.id) == usrId:
			r = [{"id": i.id, "title": i.title, "visibility": i.visibility} for i in db.session.query(DB_DOC).filter_by(author = current_user.id).all()]
		else:
			for d in db.session.query(DB_DOC).filter_by(author = usrId).all():
				if d.visibility == "public" or db.session.query(DB_USR_DOC).filter_by(id_doc=d.id, id_usr=current_user.id).first() != None:
					r.append({"id": d.id, "title": d.title, "visibility": d.visibility})
	else:
		r = [{"id": i.id, "title": i.title, "visibility": i.visibility} for i in db.session.query(DB_DOC).filter_by(author = usrId, visibility = "public").all()]

	return json.dumps(r)


@profile_blueprint.route("/newDocument/", methods = ["POST"])
@login_required
def newDocument():
	f_visibility = request.json["visibility"]
	f_title = request.json["title"]
	
	if len(f_title) >= 150:
		return make_response("invalid param size", 400)
	
	if f_visibility != "public" and f_visibility != "private" and f_visibility != "restricted":
		f_visibility = "private"
	
	db.session.add(DB_DOC(author = current_user.id, visibility = f_visibility, title = f_title))
	db.session.commit()
	return make_response("ok", 200)


@profile_blueprint.route("/deleteDocument/", methods = ["POST"])
@login_required
def deleteDocument():
	f_id = request.json["id"]
	if db.session.query(DB_DOC).filter_by(id=f_id).first() != None:
		dbOP.deleteDOC(db, f_id)
		return make_response("ok", 200)
	return make_response("id invalid", 400)

#Route pour l'ajout de questions
@profile_blueprint.route("/addQuestionToDocument/", methods = ["POST"])
@login_required
def addQuestionToDocument():
	f_questId = request.json["idQuestion"]
	f_docId = request.json["idDocument"]

	obj = db.session.query(DB_DOC).filter_by(id=f_docId).first()
	if obj == None or obj.author != current_user.id:
		return make_response("invalid document id", 400)
	
	obj = db.session.query(DB_QUESTION).filter_by(id=f_questId).first()
	if obj == None or obj.author != current_user.id:
		return make_response("invalid question id", 400)
	
	db.session.add(DB_DOC_QUESTION(id_doc=f_docId, id_question=f_questId))
	db.session.commit()
	return make_response("ok", 200)

#Route pour la supression de questions
@profile_blueprint.route("/removeQuestionFromDocument/", methods = ["POST"])
@login_required
def removeQuestionFromDocument():
	f_questId = request.json["idQuestion"]
	f_docId = request.json["idDocument"]

	obj = db.session.query(DB_DOC).filter_by(id=f_docId).first()
	if obj == None or obj.author != current_user.id:
		return make_response("invalid document id", 400)
	
	obj = db.session.query(DB_QUESTION).filter_by(id=f_questId).first()
	if obj == None or obj.author != current_user.id:
		return make_response("invalid question id", 400)

	db.session.query(DB_DOC_QUESTION).filter_by(id_doc=f_docId, id_question=f_questId).delete()
	db.session.commit()
	return make_response("ok", 200)


# QUESTION
@profile_blueprint.route("/QuestionInfo/", methods=["POST"])
def QuestionInfo():
	f_questionId = request.json["id"]
	f_id = None
	if current_user.is_authenticated:
		f_id = current_user.id

	permQ = dbOP.getUsrPermQUESTION(db, f_id, f_questionId)
	if not permQ["read"]:
		return make_response("invalid param", 400)
	
	q = db.session.query(DB_QUESTION).filter_by(id=f_questionId).first()

	r = {"id": q.id, "writing":permQ["writing"], "title": q.title, "visibility": q.visibility, "author": q.author, "tags": [], "usr": []}

	for i in db.session.query(DB_TAG_QUESTION.tag).filter_by(id_question=f_questionId).all():
		r["tags"].append(i.tag)
	
	for i in db.session.query(DB_USR_QUESTION).filter_by(id_question=f_questionId, id_usr=f_id).all():
		t_obj = db.session.query(DB_USR).filter_by(id=i.id_usr).first()
		f["usr"].append({"id":t_obj.id, "name":t_obj.name, "surname":t_obj.surname})
	
	return json.dumps(r)


@profile_blueprint.route("/profileQuestionInfo/<usrId>")
def profileQuestionInfo(usrId):
	if db.session.query(DB_USR).filter_by(id = usrId) == None:
		return make_response("invalid id", 400)

	r = []

	if current_user.is_authenticated:
		if str(current_user.id) == usrId:
			r = [{"id": i.id, "title": i.title, "visibility": i.visibility, "type": i.type, "writing": True} for i in db.session.query(DB_QUESTION).filter_by(author = current_user.id).all()]
		else:
			for d in db.session.query(DB_QUESTION).filter_by(author = usrId).all():
				perm = dbOP.getUsrPermQUESTION(db, usrId, d.id)
				if perm["read"] or d.visibility == "public":
					r.append({"id": d.id, "title": d.title, "visibility": d.visibility, "type": d.type, "writing": perm["writing"]})
	else:
		r = [{"id": i.id, "title": i.title, "visibility": i.visibility, "type": i.type, "writing": False} for i in db.session.query(DB_QUESTION).filter_by(author = usrId, visibility = "public").all()]
	
	for i in r:
		i["tags"] = dbOP.getTagsQuestion(db, i["id"])

	return json.dumps(r)
		
	

	
	
@profile_blueprint.route("/newQuestion/", methods = ["POST"])
@login_required
def newQuestion():
	f_visibility = request.json["visibility"]
	f_title = request.json["title"]
	f_type = request.json["type"]
	
	if len(f_title) >= 150 or len(f_type) >= 15:
		return make_response("invalid param size", 400)
	
	if f_visibility != "public" and f_visibility != "private" and f_visibility != "restricted":
		f_visibility = "private"
	
	db.session.add(DB_QUESTION(author = current_user.id, visibility = f_visibility, title = f_title, type = f_type, statement = "", answers = json.dumps([])))
	db.session.commit()

	return make_response("ok", 200)


@profile_blueprint.route("/deleteQuestion/", methods = ["POST"])
@login_required
def deleteQuestion():
	f_id = request.json["id"]
	
	if db.session.query(DB_QUESTION).filter_by(id = f_id).first() == None:
		return make_response("invalid id", 400)
	
	dbOP.deleteQUESTION(db, f_id)
	return make_response("ok", 200)
		
		
@profile_blueprint.route("/setQuestionTags/", methods = ["POST"])
@login_required
def setQuestionTags():
	f_questionId = request.json["id"]
	f_tags = request.json["tags"]
	
	t_obj = db.session.query(DB_QUESTION.id).filter_by(id=f_questionId).first()
	if t_obj == None or t_obj.author != current_user.id:
		return make_response("invalid param", 400)
		
	print(f_tags)
	db.session.query(DB_TAG_QUESTION).filter_by(id_question=f_questionId).delete()
	for l_tag in f_tags:
		if db.session.query(DB_TAG).filter_by(tag=l_tag, id_usr=current_user.id).first() != None:
			db.session.add(DB_TAG_QUESTION(tag=l_tag, id_usr=current_user.id, id_question=f_questionId))
	db.session.commit()
	
	return make_response("ok", 200)
		
