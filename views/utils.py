from views import session
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


# check if there is a logged-in user
# redirect to login page if no signed-in user
def user_logged_in(function):
    @wraps(function)
    def wrapper(**kw):
        if 'username' in login_session:
            return function(**kw)
        else:
            return redirect("/login")
    return wrapper


# check if there is a category with the given id
# redirect to main page if not found
def category_exists(function):
    @wraps(function)
    def wrapper(category_id, **kw):
        try:
            session.query(Category).filter_by(id=category_id).one()
            return function(category_id=category_id, **kw)

        except:
            flash('Category does not exist')
            return redirect(url_for('getCategories'))
    return wrapper


# check if there is an item with the given id
# redirect to main category page if item not found
def item_exists(function):
    @wraps(function)
    def wrapper(item_id, **kw):
        try:
            session.query(Item).filter_by(
                id=item_id).one()
            return function(item_id=item_id)

        except:
            flash('Item does not exist')
            return redirect(url_for('getCategories'))
    return wrapper


# check if logged-in user is the category's creator
# redirect to main category page if item not found
def user_owns_category(function):
    @wraps(function)
    def wrapper(category_id, **kw):
        try:
            print category_id
            print login_session['user_id']
            session.query(Category).filter_by(
                id=category_id, user_id=login_session['user_id']).one()
            return function(category_id=category_id, **kw)

        except:
            flash('Only creator can modify this category')
            return redirect(url_for('categoryItems', category_id=category_id))
    return wrapper


# check if logged-in user is the item's creator
# redirect to main category page if item not found
def user_owns_item(function):
    @wraps(function)
    def wrapper(item_id):
        try:
            item = session.query(Item).filter_by(
                id=item_id, user_id=login_session['user_id']).one()
            return function(item_id=item_id)

        except:
            flash('Only creator can modify this item')
            return redirect(url_for('getCategories'))
    return wrapper


# adds a new user info to the database
def newUser():
    new_user = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    new_user = session.query(User).filter_by(
        email=login_session['email']).one()
    return new_user.id


# get user object from database by id
def getExistingUser(user_id):
    existing_user = session.query(User).filter_by(id=user_id).one()
    return existing_user


# get user's id from database by email
def userIdFromEmail(email):
    try:
        existing_user = session.query(User).filter_by(email=email).one()
        return existing_user.id

    except:
        return None
