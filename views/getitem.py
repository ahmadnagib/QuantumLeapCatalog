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


# gets the details of a certain item of a category
@app.route('/catalog/<int:category_id>/item/<int:item_id>')
@item_exists
def getItem(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if 'username' in login_session:
        return render_template('item.html', item=item)
    else:
        return render_template(
            'item_public.html',
            item=item)


# gets the details of a certain item of a category in json format
@app.route('/catalog/<int:category_id>/item/<int:item_id>/json')
@item_exists
def getItemJSON(item_id):
    item = session.query(Item).filter_by(
        id=item_id).one()
    return jsonify(Item=item.serialize())
