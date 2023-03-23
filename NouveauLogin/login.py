from flask import Blueprint, request, render_template, url_for, flash, redirect

from flask_login import LoginManager, login_user, current_user, logout_user
from flask_security import login_required

import hashlib

from dbTable import *

LoginManager.login_view = 'login' # redirect on login when user not connected
login_manager = LoginManager()

login_blueprint = Blueprint("login", __name__, template_folder = "templates")

#On definit une classe utlisateur avec les informations qu'il doit avoir
class LOG_USR:
	#un utilisateur doit avoir un id,name,surname,email et password
	def __init__(self, l_usr):
		self.id = l_usr.id
		self.name = l_usr.name
		self.surname = l_usr.surname
		self.email = l_usr.email
		self.password = l_usr.password

	#fct qui verifie si un usr est authentifié	
	def is_authenticated(self):
		return True
	
	def is_active(self):
		return True
		
	def is_anonymous(self):
		return False
		
	def get_id(self):
		#On recupere l'id de l'usr sous forme de str
		return str(self.id)

#Fonction qui protege le mot de passe
def hashPassword(l_pass):
	return hashlib.md5(l_pass.encode('utf-8')).hexdigest()


@login_manager.user_loader
def load_user(user_id):
    usr = db.session.query(DB_USR).filter_by(id = user_id).first()
    if usr == None:
    	return None
    return LOG_USR(usr)
    

@login_blueprint.route("/signup/", methods = ["POST", "GET"])
def signup(): # SHOULD TEST FORM VALIDITY
	if current_user.is_authenticated:
		return redirect(url_for('profile.profile'))
	
	if not request.method == "POST":
		return render_template('signup.html')
		
	#POST
	f_name = request.form['name']
	f_surname = request.form['surname']
	f_email = request.form['email']
	f_password = request.form["password"]
	
	if len(f_name) > 30 or len(f_surname) > 30 or len(f_email) > 30:
		return render_template("signup.html", alert = "Les champs sont limités à 30 charactères")
			
	f_password = hashPassword(f_password) # HASH PASSWORD
	
	if db.session.query(DB_USR).filter_by(email = f_email).first() != None: # test if email exist
		return render_template("signup.html", alert = "Email déjà existant")
		
	# create account
	db.session.add(DB_USR(name = f_name, surname = f_surname, email = f_email, password = f_password))
	db.session.commit()
	
	flash("Compte créer avec succès") 
	return redirect(url_for("login.login"))
	
	
@login_blueprint.route("/login/", methods = ["POST", "GET"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('profile.profile'))
	
	if not request.method == "POST":
		return render_template('login.html')
		
	#POST
	f_email = request.form['email']
	f_password = request.form['password']
	f_remember = request.form.get('remember') != None
		
	f_password = hashPassword(f_password)  # HASH PASSWORD
	
	q_usr = db.session.query(DB_USR).filter_by(email = f_email, password = f_password).first()
	if q_usr == None: # test if email and password are valid
		return render_template("login.html", alert = "Email ou mot de passe invalide")
	
	# identification
	login_user(LOG_USR(q_usr), remember = f_remember)
	return redirect(url_for("profile.profile"))
	
	
@login_blueprint.route("/logout/")
@login_required
def logout():
	logout_user()
	return redirect(url_for("login.login"))
