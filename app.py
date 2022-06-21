import os
from flask import Flask, render_template, request, flash, redirect, session, jsonify, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_apscheduler import APScheduler
from sqlalchemy.exc import IntegrityError
from models import Eth_Stats, Users, Wallets, Wallet_Groups, db, connect_db
from forms import UserForm
from search_funcs import detectSearch, getSearchResult, handleSearch
from secret_keys import APP_SECRET_KEY
import json


app = Flask(__name__)
scheduler = APScheduler()


ES_API_BASE_URL = "https://api.etherscan.io/"

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///mebe'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', APP_SECRET_KEY)
toolbar = DebugToolbarExtension(app)

app.debug = True
connect_db(app)
scheduler.init_app(app)
scheduler.start()

# scheduler will run Eth_stats.update() every 10 seconds. Ensures call limit
scheduler.add_job(id='ETH_STATS_UPDATE', func=Eth_Stats.update, trigger='interval', seconds=20)

#####################################################################################################
# User signup/login/logout

CURR_USER_KEY = "curr_user"


@app.before_request
def add_user_to_g():
    """If we're logged in, add cur user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = Users.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user"""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Log out user"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    
    Create new user and add to DB. Redirect to User page
    If form is not valid, present form

    If there is already a user with that username: flash message and re-present form.
    """

    form = UserForm()

    if form.validate_on_submit():
        try:
            user = Users.signup(
                username = form.username.data,
                password = form.password.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('userform.html', form=form)

        do_login(user)

        return redirect(url_for('homepage'))
    
    else:
        return render_template('userform.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = UserForm()

    if form.validate_on_submit():
        user = Users.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!")
            return redirect(url_for('homepage'))

        flash("Invalid Username / Password")

    return render_template('userform.html', form=form)

@app.route('/logout')
def logout():
    """Handle user logout"""

    do_logout()
    flash('Loggout Successful!')
    return redirect(url_for('homepage'))


#############################################################################
# Main App routes

@app.route("/")
def homepage():
    """Show homepage all users land on"""

    if g.user:
        return render_template('main.html', user=g.user)
    else:
        return render_template('main.html')

@app.route('/<username>')
def userpage(username):
    """Show user page"""
    if g.user:
        return render_template('user.html', user=g.user)
    else:
        flash("Invalid Request: You must be signed in to access that page!")
        return redirect(url_for('login'))


##############################################################################
# App routes that authenticate user

##############################################################################
# API routes for app

@app.route("/api/get_eth_stats", methods=["GET"])
def get_eth_stats():
    """Grabs current eth_stats from db and returns JSON to client"""
    db_stats = Eth_Stats.query.first()
    if db_stats == None:
        db_stats = Eth_Stats.update()
    
    stats = json.loads(db_stats.__repr__())
    return jsonify(stats)

@app.route("/api/search", methods=["GET"])
def search():
    """Based on search input, determines if it's a block#, Tx hash, wallet address, or invalid and handles accordingly.
    block# - returns block# info
    tx hash - return tx hash info
    wallet address - returns wallet address info
    invalid - returns an error
    All returns are JSON
    """
    term = request.args["term"]
    resp = handleSearch(term)
    return jsonify(resp)

@app.route('/api/add_addr', methods=["POST"])
def add_address():
    """Adds address to db with user as owner"""
    addr = request.json['wallet']
    user = g.user
    wallet = Wallets.add_wallet(addr, user.username)
    try:
        if wallet["error"]:
            return jsonify(wallet)
    except TypeError:
        prep_data = json.loads(wallet.__repr__())
        return jsonify(prep_data)