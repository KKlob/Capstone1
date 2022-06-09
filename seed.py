"""Seed database with sample data from Etherscan API"""

from app import db, ES_API_BASE_URL
from models import Eth_Stats
from eth_stat_funcs import update_db_eth_stats

db.drop_all()
db.create_all()

Eth_Stats.update()