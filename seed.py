"""Seed database with sample data from Etherscan API"""

import sys
try:
    from app import db 
except AttributeError as err:
    print("You must comment out the 'scheduler.start()' line in app.py before seeding db.")
    print("Line 31 in app.py")
    sys.exit()
from models import Eth_Stats, Users, Wallets, Wallet_Groups

db.drop_all()
db.create_all()


# Create new stat db entry
stats = Eth_Stats.update()
print(stats)


# Create basic user
base_user = Users.signup("base_user", "basepassword")
db.session.commit()


# Create three basic wallet watchers for base_user
w1 = Wallets.add_wallet("0x004f74a8388cE91950F29ea3E37EF604693a6395", "base_user")
w2 = Wallets.add_wallet("0xd820187CAE7dbBfb8e12891bb55b8A352D463E60", "base_user")
w3 = Wallets.add_wallet("0xD7efCbB86eFdD9E8dE014dafA5944AaE36E817e4", "base_user")

# Create group for w1 and w2, w3 will be individual wallet
wg1a = Wallet_Groups(group_name="base_group", wallet_id=w1.id, owner="base_user")
wg1b = Wallet_Groups(group_name="base_group", wallet_id=w2.id, owner="base_user")

db.session.add(wg1a)
db.session.add(wg1b)
db.session.commit()