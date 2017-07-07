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


# gets all the items under a given category
@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items')
@category_exists
def categoryItems(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).order_by(
        desc(
            Item.updated))

    return render_template(
        'categoryitems_public.html',
        categories=categories,
        category=category,
        items=items)


# gets all the items under a given category in json format
@app.route('/catalog/<int:category_id>/json')
@app.route('/catalog/<int:category_id>/items/json')
@category_exists
def categoryItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id)
    return jsonify(Items=[item.serialize() for item in items])
