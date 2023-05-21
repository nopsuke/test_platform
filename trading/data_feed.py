from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage, Market
from typing import List
from threading import Thread

class MyWebSocketClient(WebSocketClient):
    def __init__(self, api_key, market, subscriptions):
        super().__init__(api_key, market, subscriptions)
        self.current_prices = {}

    def on_open(self):
        print("Websocket connection opened")

    def on_close(self):
        print("Websocket connection closed")

    def on_message(self, msgs: List[WebSocketMessage]):
        for m in msgs:
            if m.subject and m.subject.endswith("BTC-USD"):
                # Extract price information from the message and update the current price
                price = m.message_data['p']#
                print(f"Updated price for {m.subject} to {price}")

    def on_error(self, error):
        print(f"An error occurred: {error}")

    def get_current_price(self, symbol):
        # Returns the most recent price for a given symbol
        return self.current_prices.get(symbol)
    
    
    def handle_msg(msgs: List[WebSocketMessage]):
        for m in msgs:
            print(m)

ws = MyWebSocketClient(api_key="XXXXXXXXXXXXX", market=Market.Crypto, subscriptions=["XA.BTC-USD"])

def start_websocket():
    try:
        ws.run(handle_msg=ws.handle_msg)
    except Exception as e:
        print(f"An error occurred: {e}")

websocket_thread = Thread(target=start_websocket)
websocket_thread.start()

# This is pretty fucked, need to go at this again or change over to virtual dealer for pricefeed. Would make more sense. That's in JS though..
# Don't think this works, but maybe can be adapted to work. The dealer plugin does have the data stream sorted though, so maybe can implement that into this project?