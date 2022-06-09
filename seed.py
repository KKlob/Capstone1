"""Seed database with sample data from Etherscan API"""

from app import db, ES_API_BASE_URL
from models import Eth_Stats

db.drop_all()
db.create_all()

Eth_Stats.update()