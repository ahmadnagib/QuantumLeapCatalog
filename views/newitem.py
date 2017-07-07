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


# a logged-in user can add a new item
@app.route('/catalog/item/new/', methods=['GET', 'POST'])
@user_logged_in
def newItem():
    if request.method == 'GET':
        categories = session.query(Category).all()
        return render_template("additem.html", categories=categories)

    elif request.method == 'POST':
        categories = session.query(Category).all()
        name = request.form['name']
        description = request.form['description']
        category_id = request.form['category_id']
        user_id = login_session['user_id']

        # checks if the entered item name already exists
        # for the same category
        if name:
            try:
                existing_item = session.query(Item).filter_by(
                    name=name, category_id=category_id).one().name
                if (existing_item):
                    error_message = """Such an item already exists
                     for this category!"""
                    flash(error_message)
                    return render_template(
                        "additem.html",
                        categories=categories,
                        name=name,
                        cat=category_id,
                        description=description)

            except:
                print "Could not find an existing item"

        # checks if any of the entries is absent
        if (not description or not description.strip() or
                not name or not name.strip() or not category_id):
            error_message = """Please enter a name, a description
             and a category for your item!"""
            flash(error_message)
            return render_template(
                "additem.html",
                categories=categories,
                name=name,
                cat=category_id,
                description=description)

        # adds the new item to the database if everything is ok
        newItem = Item(
            name=name,
            description=description,
            category_id=category_id,
            user_id=user_id)
        session.add(newItem)
        session.commit()
        print category_id
        flash('Category item added successfully')
        return redirect(url_for('categoryItems', category_id=category_id))
