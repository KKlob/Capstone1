import os
import sched
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_apscheduler import APScheduler
from models import Eth_Stats, db, connect_db
from secret_keys import APP_SECRET_KEY
import json


app = Flask(__name__)
scheduler = APScheduler()

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
scheduler.init_app(app)
scheduler.start()

scheduler.add_job(id='ETH_STATS_UPDATE', func=Eth_Stats.update, trigger='interval', seconds=20)

@app.route("/")
def homepage():
    """Show homepage all users land on"""

    return render_template('main.html')

@app.route("/api/get_eth_stats", methods=["GET"])
def get_eth_stats():
    """Grabs current eth_stats from db and returns JSON to client"""
    db_stats = Eth_Stats.query.first()
    if db_stats == None:
        db_stats = Eth_Stats.update()
    
    stats = json.loads(db_stats.__repr__())
    return jsonify(stats)