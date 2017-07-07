from views import app, session
from models import (Base, User, Category, Item)
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    jsonify,
    session as login_session,
    make_response)
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import httplib2
import json
import requests
import random
import string
from functools import wraps
from utils import (
    user_logged_in,
    category_exists,
    item_exists,
    user_owns_category,
    user_owns_item,
    newUser,
    getExistingUser,
    userIdFromEmail)


# a logged-in user can add a new category
@app.route('/catalog/new/', methods=['GET', 'POST'])
@user_logged_in
def newCategory():
    if request.method == 'GET':
        return render_template("addcategory.html")

    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        user_id = login_session['user_id']

    # checks if the entered category name already exists
    if name:
        try:
            existing_category = session.query(
                Category).filter_by(name=name).one().name
            if (existing_category):
                error_message = "A category for '%s' already exists!" % name
                flash(error_message)
                return render_template(
                    "addcategory.html", name=name, description=description)

        except:
            print "Could not find an existing category"

    # checks if any of the entries is absent
    if (not description or not description.strip() or
            not name or not name.strip()):
        error_message = "Please enter a name and a description!"
        flash(error_message)
        return render_template(
            "addcategory.html",
            name=name,
            description=description)

    # adds the new category to the database if everything is ok
    newCategory = Category(name=name, description=description, user_id=user_id)
    session.add(newCategory)
    session.commit()
    flash('Category added successfully')
    return redirect(url_for('getCategories'))
