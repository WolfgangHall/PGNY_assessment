from flask_restful import Resource, reqparse
import crypto_api
from models.coin_model import CoinModel
from models.trade_log_model import TradeLogModel
import json
from dateutil import parser
import datetime
from datetime import datetime, timezone
import numpy as np
import json
from sqlalchemy import func
from helpers import write_to_log_file

class TradeListResource(Resource):
    def get(self):
        return {'items': [item.json() for item in TradeLogModel.query.all()]}

class CurrentPortfolioResource(Resource):
    def get(self):
        response = TradeLogModel.query.with_entities(TradeLogModel.coin_id, func.count(TradeLogModel.coin_id)).group_by(TradeLogModel.coin_id).all()
        for item in response:
            coin = item[0]
            quantity_held = item[1]
            output_string = "Currently holding {} unit(s) of {} coin.".format(quantity_held, coin)
            print(output_string)
            write_to_log_file(output_string)


