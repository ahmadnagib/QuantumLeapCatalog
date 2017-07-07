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


# gets all the stored categories
# and the latest 10 added items
@app.route('/')
@app.route('/catalog')
def getCategories():
    try:
        categories = session.query(Category).all()
        recently_added_items = session.query(
            Item).order_by(desc(Item.updated)).limit(10)
        return render_template(
            'allcategories_public.html',
            categories=categories,
            recently_added_items=recently_added_items)
    except:
        return render_template('allcategories_public.html')


# gets all the categories stored and put it in json format
@app.route('/json')
@app.route('/catalog/json')
def getCategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[category.serialize() for category in categories])
