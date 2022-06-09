from flask_sqlalchemy import SQLAlchemy

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

        stats = update_db_eth_stats()

        curr_data = Eth_Stats.query.first()

        if curr_data == None:
            new_stat = Eth_Stats(**stats)
            db.session.add(new_stat)
            db.session.commit()
            print("Eth_Stats updated: ", new_stat)
            return new_stat
        else:
            for key, value in stats.items():
                setattr(curr_data, key, value)
            db.session.add(curr_data)
            db.session.commit()
            print("Eth_Stats updated: ", curr_data)
            return curr_data
