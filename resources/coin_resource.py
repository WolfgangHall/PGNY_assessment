from flask_restful import Resource, reqparse
import crypto_api
from models.coin_model import CoinModel
from models.mean_price_model import MeanPriceModel
import json
from dateutil import parser
import datetime
from datetime import datetime, timezone
import numpy as np
import json
from helpers import calculate_percent_difference, write_to_log_file


class SaveTop3CoinsListResource(Resource):
    def get(self):
        # return the top 3 cryptocurrency coins based on current market cap
        top_10_coins_api_response = crypto_api.get_coins()
        json_top_10_coins = json.dumps(top_10_coins_api_response)
        json_load = json.loads(json_top_10_coins)

        # get top 3 crypto values
        trunc =  3 # if len(json_load) > 3 else len(json_load)
        json_load_trunc = json_load[:trunc]

        print("Top 3 coins by market cap: {}".format(set(map(lambda x: x['id'], json_load_trunc))))
        
        for item in json_load_trunc:
            newItem = CoinModel(
                item['id'], 
                item['name'], 
                item['current_price'],
                datetime.now(timezone.utc)
            )

            try:
                newItem.save_to_db()
            except:
                return {"message":"error occurred inserting an item"}, 500

        return {'data': json_load_trunc}, 200
        

class GetCoinListResource(Resource):
    def get(self):
        return {'data': [item.json() for item in CoinModel.query.all()]}
    

class SaveTenDayPriceMeans(Resource):
    def get(self):
        comp_dict = dict()
        three_most_recent_entries = [item.json() for item in CoinModel.get_three_most_recent_entries()]

        for item in three_most_recent_entries:
            ten_day_price = getTenDayPriceMean(item['coin_id'])
            print("Current 10 day mean price for {}: ${}".format(item['coin_id'], ten_day_price))
            adjustPriceMeanAvg(item['coin_id'], ten_day_price)
            triggerPotentialBuyOption(item['coin_id'], item['price'], ten_day_price)

        
class GetMeanPriceListResource(Resource):
    def get(self):
        return {'items': [item.json() for item in MeanPriceModel.query.all()]}


# Coin Resource Helpers 
def getTenDayPriceMean(coin_id: str) -> float:
    response_10_price_history = crypto_api.get_coin_price_history(coin_id)
    # convert to numpy array, isolate second column and calculate mean along column axis
    return np.mean(np.array(response_10_price_history)[:,1], axis=0)

def adjustPriceMeanAvg(coin_id: str, ten_day_price: float):
    item = MeanPriceModel.query.filter_by(coin_id=coin_id).first()
    updatedItem = MeanPriceModel(coin_id, ten_day_price, datetime.now(timezone.utc))
    if item is None:
        updatedItem.save_to_db()
    else:
        item.ten_day_mean = ten_day_price
        item.last_updated = datetime.now(timezone.utc)

def triggerPotentialBuyOption(coin_id: str, coin_price: float, ten_day_price: float):
    if (coin_price < ten_day_price):
        output = "Purchasing 1 order of {} at {} ...".format(coin_id, coin_price)
        print(output)
        write_to_log_file(output)

        profit = ten_day_price - coin_price
        percent_diff = calculate_percent_difference(ten_day_price, coin_price)
        crypto_api.submit_order(coin_id, 1, coin_price, profit, percent_diff)

        output = """Transaction complete. Purchased 1 order of {} for a profit of ${} and a percent difference of {}% compared to the 10 Day Mean!""". \
        format(coin_id, round(profit, 2), round(percent_diff, 2))
        print(output)
        write_to_log_file(output)
    else:
        pass 


