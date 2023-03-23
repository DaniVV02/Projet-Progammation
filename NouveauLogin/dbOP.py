from dbTable import *

# def operation
def addTag_USR(l_db, l_id, l_tag):
	if l_db.session.query(DB_USR.id).filter_by(id = l_id).first() != None and l_db.session.query(DB_TAG).filter_by(id_usr = l_id, tag = l_tag).first() == None:
		l_db.session.add(DB_TAG(id_usr = l_id, tag = l_tag))
		l_db.session.commit()
	
	
def deleteTag_USR(l_db, l_id, l_tag):
	l_db.session.query(DB_TAG).filter_by(id_usr = l_id, tag = l_tag).delete()
	l_db.session.query(DB_TAG_QUESTION).filter_by(id_tag = l_id, tag = l_tag).delete()
	l_db.session.commit()
	
	
def addTag_QUESTION(l_db, l_id, l_tag):
	author = l_db.session.query(BD_QUESTION.author).filter_by(id = l_id).first()
	
	if author == None:
		return
	
	author = author.author
	addTag_USR(l_db, author, l_tag)
	
	if l_db.session.query(DB_TAG_QUESTION).filter_by(id_tag = author, tag = l_tag, id_question = l_id).first() == None:
		l_db.session.add(DB_TAG_QUESTION(id_tag = author, tag = l_tag, id_question = l_id))
		l_db.session.commit()
		
		
def deleteTag_QUESTION(l_db, l_id, l_tag):
	author = l_db.session.query(BD_QUESTION.author).filter_by(id = l_id).first().author
	
	if author != None:
		l_db.session.remove(DB_TAG_QUESTION(id_tag = author, tag = l_tag, id_question = l_id))
		l_db.session.commit()
		

def deleteQUESTION(l_db, l_id):
	l_db.session.query(DB_DOC_QUESTION).filter_by(id_question = l_id).delete()
	l_db.session.query(DB_USR_QUESTION).filter_by(id_question = l_id).delete()
	l_db.session.query(DB_TAG_QUESTION).filter_by(id_question = l_id).delete()
	l_db.session.query(DB_QUESTION).filter_by(id = l_id).delete()
	l_db.session.commit()
	

def deleteDOC(l_db, l_id):
	l_db.session.query(DB_DOC_QUESTION).filter_by(id_doc = l_id).delete()
	l_db.session.query(DB_DOC).filter_by(id = l_id).delete()
	l_db.session.commit()
	
	
def deleteUSR(l_db, l_id):
	for q in l_db.session.query(DB_QUESTION.id).filter_by(author = l_id).all():
		deleteQUESTION(l_db, q.id)
	
	for d in l_db.session.query(DB_DOC.id).filter_by(author = l_id).all():
		deleteDOC(l_db, d.id)
			
	l_db.session.query(DB_TAG).filter_by(id_usr = l_id).delete()
	l_db.session.commit()
	

def getUsrPermQUESTION(l_db, l_usrId, l_questionId):
	r = {"read": False, "writing": False}

	q = l_db.session.query(DB_QUESTION.author, DB_QUESTION.visibility).filter_by(id = l_questionId).first()
	if q == None:
		return r
	
	if q.author == l_usrId: # user is author
		r["read"] = True
		r["writing"] = True
		return r
	
	if q.visibility == "private":
		return r
	
	if q.visibility == "public":
		r["read"] = True
	
	t_r = l_db.session.query(DB_USR_QUESTION).filter_by(id_usr = l_usrId, id_question = l_questionId).first()
	if t_r != None: # direct link
		r["read"] = True
		r["writing"] = t_r.writing
	
	return r

def canUsrSeeDoc(l_db, l_usrId, l_docId):
	l_doc = l_db.session.query(DB_DOC).filter_by(id=l_docId).first()
	if l_doc == None:
		return False
	
	if l_doc.author == l_usrId:
		return True
	
	if l_doc.visibility == "public":
		return True
	
	if l_db.session.query(DB_USR_DOC).filter_by(id_doc=l_docId, id_usr=l_usrId).first() != None:
		return True
	
	return False


def getTagsQuestion(l_db, l_questionId):
	return [i.tag for i in l_db.session.query(DB_TAG_QUESTION).filter_by(id_question = l_questionId).all()]