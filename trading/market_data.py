import requests
from trading.data_feed import ws

ALPHA_VANTAGE_API_KEY = 'your_api_key_here'

def fetch_time_series_data(symbol, interval='15min', output_size='compact'):
    base_url = 'https://www.alphavantage.co/query?'
    function = 'TIME_SERIES_INTRADAY'

    url = f"{base_url}function={function}&symbol={symbol}&interval={interval}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize={output_size}"
    response = requests.get(url)
    return response.json()

def fetch_current_price(symbol):
    return ws.get_current_price(symbol)



"""POLYGON_API_KEY = "znfXR7OLa31mT1BPHuSl60vIl_syeOoQ"

def fetch_current_price(symbol):
    base_url = "wss://socket.polygon.io/crypto"
    url = f"{base_url}?apiKey={POLYGON_API_KEY}&symbols={symbol}"
    response = requests.get(url)
    data = response.json()

"""



def buy_order(user_profile, symbol, quantity, price, leverage, stop_loss=None):
    price = fetch_current_price(symbol)
    amount = price * quantity
    leveraged_amount = amount / user_profile.leverage
    

    if not has_enough_balance(user_profile, leveraged_amount):
        return {'error': 'Insufficient balance'}
    # Simulate trade execution (replace this with actual trade execution via a brokerage or exchange API)
    print(f"Executed buy order for {quantity} shares of {symbol} at ${price:.2f} per share. Total: ${amount:.2f}")

    # Update user's balance
    user_profile.balance -= leveraged_amount
    update_open_positions(user_profile, symbol, quantity, price, 'buy', stop_loss)
    margin_level = update_margin_level(user_profile)

    if margin_level < 100:
        # Close all positions if the margin level drops below 100%
        close_all_positions(user_profile)
        return {'error': 'Margin call. All positions closed.'}
    
    user_profile.save()

    return {'symbol': symbol, 'quantity': quantity, 'price': price, 'amount': amount, 'stop_loss': stop_loss}


def has_enough_balance(user_profile, amount):
    return user_profile.balance >= amount

def sell_order(user_profile, symbol, quantity, price, leverage, stop_loss=None):
    price = fetch_current_price(symbol)
    amount = price * quantity
    leveraged_amount = amount / user_profile.leverage

    # Simulate trade execution (replace this with actual trade execution via a brokerage or exchange API)
    print(f"Executed sell order for {quantity} shares of {symbol} at ${price:.2f} per share. Total: ${amount:.2f}")

    # Update user's balance
    user_profile.balance += leveraged_amount
    update_open_positions(user_profile, symbol, quantity, price, 'sell', stop_loss)
    margin_level = update_margin_level(user_profile)

    if margin_level < 100:
        # Close all positions if the margin level drops below 100%
        close_all_positions(user_profile)
        return {'error': 'Margin call. All positions closed.'}

    user_profile.save()

    return {'symbol': symbol, 'quantity': quantity, 'price': price, 'amount': amount, "stop_loss": stop_loss}


def update_open_positions(user_profile, symbol, quantity, price, action, stop_loss=None):
    if action == 'buy':
        user_profile.open_positions[symbol] = {
            'quantity': user_profile.open_positions.get(symbol, {}).get('quantity', 0) + quantity,
            'stop_loss': stop_loss
        }
    elif action == 'sell':
        user_profile.open_positions[symbol] = {
            'quantity': user_profile.open_positions.get(symbol, {}).get('quantity', 0) - quantity,
            'stop_loss': stop_loss
        }

    # Remove the position if the quantity is zero or negative
    if user_profile.open_positions[symbol]['quantity'] <= 0:
        user_profile.open_positions.pop(symbol, None)

    user_profile.save()


def update_margin_level(user_profile):
    total_position_value = 0

    for symbol, quantity in user_profile.open_positions.items():
        price = fetch_current_price(symbol)
        total_position_value += price * quantity

    user_profile.margin_level = user_profile.balance / (total_position_value / user_profile.leverage) * 100
    user_profile.save()

    return user_profile.margin_level

def close_all_positions(user_profile):
    for symbol, quantity in user_profile.open_positions.items():
        price = fetch_current_price(symbol)
        amount = price * quantity
        leveraged_amount = amount / user_profile.leverage

        if quantity > 0:
            user_profile.balance += leveraged_amount
        elif quantity < 0:
            user_profile.balance -= leveraged_amount

    user_profile.open_positions = {}
    user_profile.save()

def calculate_equity(user_profile):
    total_position_value = 0

    for symbol, quantity in user_profile.open_positions.items():
        price = fetch_current_price(symbol)
        total_position_value += price * quantity

    equity = user_profile.balance + total_position_value
    return equity

