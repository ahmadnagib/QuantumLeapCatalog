from views import app, session
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

# get the client_id from the client secret json file
CLIENT_ID = json.loads(
    open(
        'secrets_of_g_client.json',
        'r').read())['web']['client_id']


# inspired from udacity lessons
# get the login page if the user is not logged-in
@app.route('/login')
def getLoginPage():
    try:
        username = login_session['username']
        flash("You are already logged-in as %s" % username)
        return redirect(url_for('getCategories'))

    except:
        # session_state token for anti-forgery
        session_state = ''.join(
            random.choice(
                string.ascii_uppercase +
                string.digits) for x in xrange(32))
        login_session['session_state'] = session_state
        return render_template('login.html', SESSION_STATE=session_state)


# inspired from udacity lessons
# works on the google auth response to
# log successfully authorized users in
@app.route('/gplus-auth', methods=['POST'])
def googleAuth():
    # check if state token is identical for anti-forgery
    if (request.args.get('state') != login_session['session_state']):
        response = make_response(
            json.dumps('Something is wrong with the session_state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # get authorization code from google+ Auth Response
    one_time_code = request.data

    try:
        # get a credentials object using the authorization code
        gplus_oauth_flow = flow_from_clientsecrets(
            'secrets_of_g_client.json', scope='')
        gplus_oauth_flow.redirect_uri = 'postmessage'
        credentials = gplus_oauth_flow.step2_exchange(one_time_code)

    except FlowExchangeError:
        response = make_response(
            json.dumps('''There was a problem in getting credentials
                        object using the authorization code.'''), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # make sure that the access token exists and valid.
    access_token = credentials.access_token
    token_info_url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    http_object = httplib2.Http()
    result = json.loads(http_object.request(token_info_url, 'GET')[1])

    # exit and respond with the error whenever there is something wrong
    # with the access token info
    if (result.get('error') is not None):
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # make sure that the application can use the access token
    if (result['issued_to'] != CLIENT_ID):
        response = make_response(
            json.dumps('''The application client_id is different from
                       the one stored in the token'''), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # make sure that the user can use the access token
    gplus_id = credentials.id_token['sub']
    if (result['user_id'] != gplus_id):
        response = make_response(
            json.dumps('''The user_id is different from the one
                        stored in the token'''), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    session_credentials = login_session.get('credentials')
    session_gplus_id = login_session.get('gplus_id')

    if (gplus_id == session_gplus_id and session_credentials is not None):
        response = make_response(
            json.dumps('The user is already logged-in'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # If the access token is valid, get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    parameters = {'access_token': credentials.access_token, 'alt': 'json'}
    get_user_info = requests.get(userinfo_url, params=parameters)

    user_info = get_user_info.json()

    # update the login_session with user and login-related info
    login_session['username'] = user_info['name']
    login_session['picture'] = user_info['picture']
    login_session['email'] = user_info['email']
    login_session['auth_provider'] = "google"
    login_session['access_token'] = access_token
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # if the user's email is not found in database create a new user
    # and update login_session info with the new user_id
    if (userIdFromEmail(login_session['email']) is None):
        login_session['user_id'] = newUser()

    # if the user's email is found in database get the user id
    # and update login_session info with the existing user_id
    else:
        login_session['user_id'] = userIdFromEmail(login_session['email'])

    # create a response containing username and picture to be viewed
    # before redirecting to the catalog homepage
    view = ''
    view += '<h3>Welcome to QL Catalog, '
    view += login_session['username']
    view += '!</h3>'
    view += '<img src="'
    view += login_session['picture']
    view += '"> </br></br>'

    flash("""You have been successfully logged-in to
          QL Catalog as %s""" % login_session['username'])
    return view
