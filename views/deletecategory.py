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


# deletes an existing category if the logged-in user is the creator
@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
@user_logged_in
@category_exists
@user_owns_category
def deleteCategory(category_id):
    if request.method == 'GET':
        category = session.query(Category).filter_by(id=category_id).one()
        return render_template("deletecategory.html", category=category)

    elif request.method == 'POST':
        category = session.query(Category).filter_by(id=category_id).one()
        category_name = category.name
        session.delete(category)
        session.commit()
        flash('%s Category deleted successfully' % category_name)
        return redirect(url_for('getCategories'))
