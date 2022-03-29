from db import db
import json
from json import JSONEncoder
from datetime import datetime, timezone

class CoinModel(db.Model):
    __tablename__ = 'coins'

    id = db.Column(db.Integer, primary_key=True)
    coin_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float(precision=12), nullable=False)
    date_updated = db.Column(db.DateTime, nullable=False, default = datetime.now(timezone.utc))

    def __init__(self, coin_id, name, price, date_updated):
        self.coin_id = coin_id
        self.name = name
        self.price = price
        self.date_updated = date_updated

    def json(self):
        return {
            'coin_id': self.coin_id,
            'name': self.name,
            'price': self.price,
            'date_updated': json.dumps(self.date_updated, default=str),
        }

    @classmethod
    def get_three_most_recent_entries(cls):
        return cls.query.order_by(CoinModel.date_updated.desc()).limit(3)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()   
        