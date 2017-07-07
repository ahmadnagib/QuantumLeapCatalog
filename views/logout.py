from views import app
from models import (Base, User, Category, Item)
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    jsonify,
    session as login_session)
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


# logout user if logged-in
@app.route('/logout')
@user_logged_in
def logout():
    if login_session['auth_provider'] == "google":
        # check if the user has an access token
        # revoke it if true
        try:
            access_token = login_session['access_token']
            revoke_url ='https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token

            http_object = httplib2.Http()
            response = http_object.request(revoke_url, 'GET')[0]

        except:
            flash("This user is not logged-in")
            return redirect(url_for('getCategories'))

        # delete user and login-related info from the login_session
        if response['status'] == '200':
            del login_session['access_token']
            del login_session['gplus_id']
            del login_session['email']
            del login_session['username']
            del login_session['picture']
            flash("You have been logged-out successfully")
            return redirect(url_for('getCategories'))

        else:
            flash("Something went wrong while disconnecting from google!")
            return redirect(url_for('getCategories'))
