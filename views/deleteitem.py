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


# deletes an existing item if the logged-in user is the creator
@app.route(
    '/catalog/<int:category_id>/item/<int:item_id>/delete/',
    methods=[
        'GET',
        'POST'])
@user_logged_in
@item_exists
@user_owns_item
def deleteItem(item_id):
    if request.method == 'GET':
        item = session.query(Item).filter_by(
            id=item_id).one()
        return render_template("deleteitem.html", item=item)

    elif request.method == 'POST':
        item = session.query(Item).filter_by(
            id=item_id).one()
        item_name = item.name
        category_id = item.category_id
        session.delete(item)
        session.commit()
        flash('%s Item deleted successfully' % item_name)
        return redirect(url_for('categoryItems', category_id=category_id))
