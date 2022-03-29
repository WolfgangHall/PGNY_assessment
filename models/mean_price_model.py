from db import db
from datetime import datetime, timezone
import json

class MeanPriceModel(db.Model):
    __tablename__ = 'mean_price'

    id = db.Column(db.Integer, primary_key=True)
    coin_id = db.Column(db.String(15), nullable=False)
    ten_day_mean = db.Column(db.Float(precision=12), nullable=False)
    last_updated_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __init__(self, coin_id, ten_day_mean, last_updated_date):
        self.coin_id = coin_id
        self.ten_day_mean = ten_day_mean
        self.last_updated_date = last_updated_date

    def json(self):
        return {
            'coin_id': self.coin_id, 
            'ten_day_mean': self.ten_day_mean,
            'last_updated_date': json.dumps(self.last_updated_date, default=str)
        }

    @classmethod
    def find_10_day_mean_by_coin_id(cls, coin_id):
        return cls.query.filter_by(MeanPriceModel.coin_id==coin_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()  