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


# edits an item if the logged-in user is the creator
@app.route(
    '/catalog/<int:category_id>/item/<int:item_id>/edit/',
    methods=[
        'GET',
        'POST'])
@user_logged_in
@item_exists
@user_owns_item
def editItem(item_id):
    # shows the edit form
    if request.method == 'GET':
        categories = session.query(Category).all()
        item = session.query(Item).filter_by(
            id=item_id).one()
        return render_template(
            "edititem.html",
            item=item,
            categories=categories,
            name=item.name,
            cat=item.category_id,
            description=item.description)

    elif request.method == 'POST':
        categories = session.query(Category).all()
        name = request.form['name']
        description = request.form['description']
        category_id = request.form['category_id']
        # checks if any other item of the same category
        # has the new editted name
        if name:
            try:
                existing_item = session.query(Item).filter_by(
                    name=name, category_id=category_id).filter_by(
                    id != item_id).one().name
                if (existing_item):
                    error_message = """Such an item already exists
                    for this category!"""
                    flash(error_message)
                    return render_template(
                        "edititem.html",
                        categories=categories,
                        name=name,
                        cat=category_id,
                        description=description)

            except:
                print "Could not find an existing item"

        # checks if any of the entries is absent
        if (not description or not description.strip() or
                not name or not name.strip() or not category_id):
            error_message = """Please enter a name, a description and
            a category for your item!"""
            flash(error_message)
            return render_template(
                "edititem.html",
                categories=categories,
                name=name,
                cat=category_id,
                description=description)

        # updates the database if everything is fine
        else:
            item = session.query(Item).filter_by(
                id=item_id).one()
            item.name = name
            item.description = description
            item.category_id = category_id

            session.commit()

            flash('Item edited successfully')
            return redirect(
                url_for(
                    'getItem',
                    category_id=item.category_id,
                    item_id=item_id))
