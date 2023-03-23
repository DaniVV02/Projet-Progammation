from flask import Blueprint, request, render_template, url_for, flash, redirect

from flask_login import current_user
from flask_security import login_required

import hashlib

from dbTable import *
import dbOP

docEditor_blueprint = Blueprint("docEditor", __name__, template_folder = "templates")


"""
@docEditor_blueprint.route("/edit/", methods = ["POST", "GET"])
@login_required
def editDocument():
	#test access
	access 
	if access:
		return #document
		if request.method == "POST":
	      		user = request.form['nm']
			return redirect(url_for('editor.html',name = user))
		else:
	      		user = request.args.get('nm')
			return redirect(url_for('success',name = user))
	else:
		return render_template("access_denied.html")


@docEditor_blueprint.route("/visualize/<postId>")
def visualize(postId):
	#test access
	if access:
		return #document
		if request.method == "POST":
	      		user = request.form['nm']
			return redirect(url_for('success',name = user))
		else:
	      		user = request.args.get('nm')
			return redirect(url_for('success',name = user))
	else:
		return render_template("access_denied.html")
"""
