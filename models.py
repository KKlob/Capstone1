from flask_sqlalchemy import SQLAlchemy
import time

from eth_stat_funcs import update_db_eth_stats

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app"""

    db.app = app
    db.init_app(app)

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

class Users(db.Model):
    """Stores username/password"""

    __tablename__ = "users"

    def __repr__(self):
        return f"<User id: {self.id} | username: {self.username}>"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    username = db.Column(db.String(length=30),
                    nullable=False,
                    unique=True)
    password = db.Column(db.Text,
                    nullable=False)

class Wallets(db.Model):
    """Stores info on wallets"""

    __tablename__ = "wallets"

    def __repr__(self):
        return f"<Wallet id: {self.id} | wallet_address: {self.wallet_address} | group_id: {self.group_id} | owner: {self.owner}>"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    wallet_address = db.Column(db.Text,
                        nullable=False,
                        unique=True)
    eth_total = db.Column(db.Float)
    tokens = db.Column(db.Text)
    group_id = db.Column(db.Integer,
                        db.ForeignKey('wallet_groups.id'))
    owner = db.Column(db.Text,
                        db.ForeignKey('users.username'))

class Wallet_Groups(db.Model):
    """Links wallets.group_id and users.username. Each user can create groups of wallets they own to pool total eth/tokens + value of all wallets"""
    
    __tablename__ = "wallet_groups"

    def __repr__(self):
        return f"<Wallet_Groups id: {self.id} | Group Name: {self.group_name} | Owner: {self.owner}>"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    group_name = db.Column(db.Text,
                        unique=True,
                        nullable=False)
    owner = db.Column(db.Text,
                    db.ForeignKey('users.username'))