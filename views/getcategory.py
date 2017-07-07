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


# get a certain category of interest
@app.route('/catalog/<int:category_id>/')
@category_exists
def getCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' in login_session:
        return render_template('category.html', category=category)
    else:
        return render_template(
            'category_public.html',
            category=category)


# get details of a certain category of interest in json format
@app.route('/catalog/<int:category_id>/json')
@category_exists
def getCategoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return jsonify(Category=category.serialize())
