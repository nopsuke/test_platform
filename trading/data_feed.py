from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage, Market
from typing import List
import logging
import threading
import redis
import json
import time
import os
from celery import shared_task
logger = logging.getLogger(__name__)
ws = None

class MyWebSocketClient(WebSocketClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.latest_prices = {}
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
    


    def handle_message(self, msg: List[WebSocketMessage]):
        for m in msg:
            # 'pair' is the field for symbol and 'close' for latest price
            if hasattr(m, 'pair') and hasattr(m, 'close'):
                self.latest_prices[m.pair] = m.close
                self.redis_client.setex(m.pair, 600, json.dumps({'price': m.close, 'timestamp': time.time()})) # Store data for 10 minutes

    def on_open(self):
        logger.info(f"Websocket connection opened")
        

    def get_current_price(self, symbol):

        if symbol in self.latest_prices:
            return self.latest_prices[symbol]
        else:
            return "Issue with data feed"
        
        return self.latest_prices.get(symbol, None)
    
    def on_close(self):
        logger.info(f"Websocket connection closed")
        
    
    def run(self):
        super().run(handle_msg=self.handle_message)


#ws = MyWebSocketClient(api_key="znfXR7OLa31mT1BPHuSl60vIl_syeOoQ", market=Market.Crypto, subscriptions=["XT.BTC-USD"])

#def start_ws_client():
    #ws.run()

#threading.Thread(target=start_ws_client).start()



# To keep the script running, preventing it from exiting before any data is received.
# NEED TO FIX THIS, SOMETIMES DATA JUST STOPS?
# I'm connecting to the ws via different API calls so it's duplicating the connections and I'm getting disconnected.
# Have Redis take the whole data feed for 10 minutes, have everything else gather data from there. Much more efficient way of accessing the data.
# Made some changes, lets see..


#HAVE TO REDO THE WHOLE THING, THIS A FUCKING MESS.



