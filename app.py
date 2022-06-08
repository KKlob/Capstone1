import os
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
from secret_keys import APP_SECRET_KEY


app = Flask(__name__)

ES_API_BASE_URL = "https://api.etherscan.io/"

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///mebe'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', APP_SECRET_KEY)
toolbar = DebugToolbarExtension(app)

app.debug = True
connect_db(app)

@app.route("/")
def homepage():
    """Show homepage all users land on"""

    return render_template('main.html')

