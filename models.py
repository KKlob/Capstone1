from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import time
from sqlalchemy import exc

from psycopg2 import IntegrityError

from eth_stat_funcs import update_db_eth_stats
from wallet_funcs import get_eth_bal, update_balances

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app"""

    db.app = app
    db.init_app(app)

################################################################
# Eth_Stats Model. Defines how db will store stats

class Eth_Stats(db.Model):
    """Stores eth blockchain stats"""

    __tablename__ = 'eth_stats'

    def __repr__(self):
        """returns serialized json string. 
        Can be passed into json.loads() -> jsonify() to send info to client. """
        return "{" + f'"total_supply": {self.total_supply}, ' + f'"total_supply_eth2": {self.total_supply_eth2}, ' + f'"last_price": {self.last_price}, ' + f'"safe_gas": {self.safe_gas}, ' + f'"prop_gas": {self.prop_gas}, ' + f'"fast_gas": {self.fast_gas}, ' + f'"base_fee": {self.base_fee}' + "}"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    total_supply = db.Column(db.Text,
                            nullable=False)

    total_supply_eth2 = db.Column(db.Text,
                            nullable=False)

    last_price = db.Column(db.Float,
                            nullable=False)

    safe_gas = db.Column(db.Text,
                        nullable=False)

    prop_gas = db.Column(db.Text,
                        nullable=False)
    
    fast_gas = db.Column(db.Text,
                        nullable=False)

    base_fee = db.Column(db.Float,
                        nullable=False)

    @classmethod
    def update(cls):
        """Collect fresh stats from Etherscan, clean it up, then update db"""
        startTime = time.time()
        stats = update_db_eth_stats()

        curr_data = Eth_Stats.query.first()

        if curr_data == None:
            new_stat = Eth_Stats(**stats)
            db.session.add(new_stat)
            db.session.commit()

            exeTime = (time.time() - startTime)
            print(f'Eth_Stats api calls + cleanup took {str(exeTime)}')

            return new_stat
        else:
            for key, value in stats.items():
                setattr(curr_data, key, value)
            db.session.add(curr_data)
            db.session.commit()

            exeTime = (time.time() - startTime)
            print(f'Eth_Stats api calls + cleanup took {str(exeTime)}')

            return curr_data

#############################################################################
# Users model, defines signup / authenticate class methods. Handles requirements for user storage

class Users(db.Model):
    """Stores username/password"""

    __tablename__ = "users"

    def __repr__(self):
        return "{" + f'"username": "{self.username}"' + "}"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    username = db.Column(db.String(length=30),
                    nullable=False,
                    unique=True)
    password = db.Column(db.Text,
                    nullable=False)

    wallets = db.relationship('Wallets')

    wallet_groups = db.relationship('Wallet_Groups')


    @classmethod
    def signup(cls, username, password):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pw = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = Users(
            username=username,
            password=hashed_pw
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with 'username' and 'password'.
        
        Searches for a user whose password hash matches this password and, if it finds such a user, returns that user object.
        
        If it can't find matching user (or if password is wrong), returns False."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        
        return False
        
    @classmethod
    def remove_user(cls, user):
        """Removes user from db"""
        db.session.delete(user)
        db.session.commit()

###############################################################################
# Wallets class handles storing basic wallet information user choses to save.

class Wallets(db.Model):
    """Stores info on wallets"""

    __tablename__ = "wallets"

    def __repr__(self):
        return "{" + f'"wallet_address": "{self.wallet_address}", ' + f'"eth_total": {self.eth_total}, ' + f'"owner": "{self.owner}"' + "}"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    wallet_address = db.Column(db.Text,
                        nullable=False,
                        unique=True)
    eth_total = db.Column(db.Float)
    owner = db.Column(db.Text,
                        db.ForeignKey('users.username', ondelete="CASCADE"))



    @classmethod
    def add_wallet(cls, wallet_address, owner):
        """Handles adding single wallet with complete info to db"""
        try:
            new_wallet = Wallets(wallet_address=wallet_address, owner=owner)
            eth_bal = get_eth_bal(wallet_address)
            setattr(new_wallet, "eth_total", eth_bal)
            db.session.add(new_wallet)
            db.session.commit()
            return new_wallet
        except exc.IntegrityError:
            db.session.rollback()
            return {"error": "You already have that wallet added to your watchlist!"}
    
    @classmethod
    def update_wallets(cls, owner):
        """Handles updating eth_bal of all wallets owned by owner."""
        # get results of all wallets from db
        wallet_arr = owner.wallets
        # handle updating balances for all wallets gathered
        data = update_balances(wallet_arr)
        # for each updated wallet, update the appropriate wallet object eth_total
        for index, wallet in enumerate(wallet_arr):
            if data[index]['account'] is wallet.wallet_address:
                wallet.eth_total = data[index]['balance']
                db.session.add(wallet)
        db.session.commit()

    @classmethod
    def remove_wallet(cls, address, user):
        """Handles removing wallet from db"""
        wallet = cls.query.filter_by(wallet_address=address)
        if wallet.owner == user.username:
            db.session.delete(wallet)
            db.session.commit()


###############################################################################
# Wallet_Groups handles the link between saved wallets and which users own them.

class Wallet_Groups(db.Model):
    """Links wallets.group_id and users.username. Each user can create groups of wallets they own to pool total eth/tokens + value of all wallets"""
    
    __tablename__ = "wallet_groups"

    def __repr__(self):
        return "{" + f'"id": {self.id}, "group_name": "{self.group_name}", "wallet_id": {self.wallet_id}, "owner": "{self.owner}"' + "}"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    group_name = db.Column(db.Text,
                            default="")
    wallet_id = db.Column(db.Integer,
                        db.ForeignKey('wallets.id', ondelete="CASCADE"),
                        nullable=False)
    owner = db.Column(db.Text,
                    db.ForeignKey('users.username', ondelete="CASCADE"),
                    nullable=False)