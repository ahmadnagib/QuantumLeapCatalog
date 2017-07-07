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


# edits a category if the logged-in user is the creator
@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
@user_logged_in
@category_exists
@user_owns_category
def editCategory(category_id):
    # shows the edit form
    if request.method == 'GET':
        category = session.query(Category).filter_by(id=category_id).one()
        return render_template(
            "editcategory.html",
            name=category.name,
            description=category.description)

    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        # checks if any other category has the new editted name
        if name:
            try:
                existing_category = session.query(Category).filter_by(
                    name=name).filter_by(id != category_id).one().name
                if (existing_category):
                    error_message = "A category for '%s' already exists!" % name
                    flash(error_message)
                    return render_template(
                        "editcategory.html",
                        name=name,
                        description=description)

            except:
                print "Could not find an existing category"

        # checks if any of the entries is absent
        if (not description or not description.strip() or not name or
                not name.strip()):
                error_message = "Please enter a name and a description!"
                flash(error_message)
                return render_template(
                    "editcategory.html",
                    name=name,
                    description=description)
        # updates the database if everything is fine
        category = session.query(Category).filter_by(id=category_id).one()
        category.name = request.form['name']
        category.description = request.form['description']
        session.add(category)
        session.commit()

        flash('Category edited successfully')
        return redirect(url_for('getCategories'))
