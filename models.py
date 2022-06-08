from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app"""

    db.app = app
    db.init_app(app)

class Eth_Stats(db.Model):
    """Stores eth blockchain stats"""

    __tablename__ = 'eth_stats'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    total_supply = db.Column(db.Float,
                            nullable=False)

    total_supply_eth2 = db.Column(db.Float,
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
    def update(cls, stats):
        """Pass in clean stats to update db with"""

        old_data = Eth_Stats.query.first()
        if old_data != None:
            db.session.delete(old_data)
            db.session.commit()

        data = Eth_Stats(total_supply=stats['total_supply'],
                    total_supply_eth2=stats['total_supply_eth2'],
                    last_price=stats['last_price'],
                    safe_gas=stats['safe_gas'],
                    prop_gas=stats['prop_gas'],
                    fast_gas=stats['fast_gas'],
                    base_fee=stats['base_fee'])
        db.session.add(data)
        db.session.commit()
        return data