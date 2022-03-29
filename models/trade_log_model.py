from db import db
from datetime import datetime, timezone
import json

class TradeLogModel(db.Model):
    __tablename__ = "trade_log"
    id = db.Column(db.Integer, primary_key=True)
    coin_id = db.Column(db.String(15), nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    purchase_price = db.Column(db.Float(precision=12), nullable=False)
    trade_profit = db.Column(db.Float(precision=12), nullable=False)
    percent_profit = db.Column(db.Float(precision=12), nullable=False)

    def __init__(self, coin_id, transaction_date, purchase_price, trade_profit, percent_profit):
        self.coin_id = coin_id
        self.transaction_date = transaction_date
        self.purchase_price = purchase_price
        self.trade_profit = trade_profit
        self.percent_profit = percent_profit

    def json(self):
        return {
            'coin_id': self.coin_id, 
            'purchase_price': self.purchase_price,
            'transaction_date': json.dumps(self.transaction_date, default=str),
            'trade_profit': self.trade_profit,
            'percent_profit': self.percent_profit
        }

    @classmethod
    def find_all_transactions_by_coin_id(cls, coin_id):
        return cls.query.filter_by(TradeLogModel.coin_id==coin_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()  

