"""Crypto Interview Assessment Module."""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from flask import Flask
from flask_restful import Api
from dotenv import find_dotenv, load_dotenv
from flask_sqlalchemy import SQLAlchemy
from resources.coin_resource import SaveTop3CoinsListResource, GetCoinListResource, GetMeanPriceListResource, SaveTenDayPriceMeans
from resources.trade_resource import TradeListResource, CurrentPortfolioResource
import crypto_api
from flask_apscheduler import APScheduler
import requests

load_dotenv(find_dotenv(raise_error_if_not_found=True))

# You can access the environment variables as such, and any variables from the .env file will be loaded in for you to use.
db_url = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_DATABASE')}"

# Start Here
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(SaveTop3CoinsListResource, '/saveTopThreeCoinsByMarketCap')
api.add_resource(SaveTenDayPriceMeans, '/saveTenDayPriceMeans')
api.add_resource(GetMeanPriceListResource, '/getMeanPriceList')
api.add_resource(TradeListResource, '/getTransactionLog')
api.add_resource(CurrentPortfolioResource, '/getCurrentPortfolio')

scheduler = APScheduler()
scheduler.start()

@scheduler.task('interval', id='carry out crypto tasks', seconds=3600, misfire_grace_time=900)
def job1():
    requests.get('http://127.0.0.1:5000/saveTopThreeCoinsByMarketCap')
    requests.get('http://127.0.0.1:5000/saveTenDayPriceMeans')
    requests.get('http://127.0.0.1:5000/getCurrentPortfolio')
    

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True, use_reloader=False)