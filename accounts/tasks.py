from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import OpenPositions, UserProfile, ClosedPositions, BattleGame, TradingProfile
from django.db import models, transaction
import logging
import redis
import json
import time
from rest_framework.exceptions import ValidationError
from statistics import mean


logger = logging.getLogger(__name__)

r = redis.Redis(host='localhost', port=6379, db=0)

@shared_task
@transaction.atomic
def close_position_task(open_position_id, trading_profile_id):
    try:
        trading_profile = TradingProfile.objects.get(id=trading_profile_id)
        open_position = OpenPositions.objects.get(id=open_position_id)
        
    except (UserProfile.DoesNotExist, OpenPositions.DoesNotExist):
        logger.error(f"No UserProfile with id={trading_profile_id} or OpenPositions with id={open_position_id}")
        return
    
    if open_position.direction.upper() == "LONG":
        close_price = fetch_current_price(open_position.symbol, "SHORT")
    elif open_position.direction.upper() == "SHORT":
        close_price = fetch_current_price(open_position.symbol, "LONG")
    if not close_price:
        logger.error(f"Could not fetch current price for {open_position.symbol}")
        return

    if open_position.direction == "LONG":
        profit_or_loss = (float(close_price) - float(open_position.open_price)) * float(open_position.quantity)
    else: # SHORT
        profit_or_loss = (float(open_position.open_price) - float(close_price)) * float(open_position.quantity)

    fund_cost = float(open_position.funding_cost) + float(open_position.funding_cost)
    
    trading_profile.balance += (profit_or_loss - fund_cost) + open_position.margin_used
    print(f"New balance: {trading_profile.balance}")
    trading_profile.save()

    closed_position = ClosedPositions.objects.create(
        trading_profile=trading_profile,
        symbol=open_position.symbol,
        direction=open_position.direction,
        quantity=open_position.quantity,
        open_price=open_position.open_price,
        close_price=float(close_price),
        open_time=open_position.open_time,
        profit_or_loss=profit_or_loss,
        leverage=open_position.leverage,
        fund_cost=fund_cost,


    )

    open_position.delete()

    return {"symbol": closed_position.symbol,
            "quantity": closed_position.quantity,
            "open_price": closed_position.open_price,
            "close_price": closed_position.close_price,
            "profit_or_loss": closed_position.profit_or_loss,
            "fund_cost": fund_cost,
            }




@shared_task
def db_update_task():
    trading_profiles = TradingProfile.objects.all()
    symbol_price = {}

    for trading_profile in trading_profiles:
        open_positions = OpenPositions.objects.filter(trading_profile=trading_profile)
        total_pnl = 0
        total_margin_used = 0

        for position in open_positions:
            symbol = position.symbol

            if symbol not in symbol_price:
                symbol_price[symbol] = fetch_current_price(symbol, position.direction)

            current_price = symbol_price[symbol]

            if position.direction == "LONG":
                pnl = (current_price - position.open_price) * position.quantity
            else:   # SHORT
                pnl = (position.open_price - current_price) * position.quantity
    
            position.profit_or_loss = pnl
            total_pnl += pnl
            total_margin_used += position.margin_used

        equity = trading_profile.balance + total_pnl

        for position in open_positions:
            margin_level = (equity / total_margin_used) * 100 if total_margin_used > 0 else float('inf')
            position.equity = equity
            logger.info(f"Current margin level for ")
            if margin_level < 120:
                logger.warning(f"Margin call! Margin level below 120% for ! Please add funds or close positions to avoid liquidation!")
            elif margin_level < 70:
                logger.warning(f"THIS IS WHERE THE LIQUIDATION FUNCTION WILL BE CALLED for !")

        OpenPositions.objects.bulk_update(open_positions, ['profit_or_loss', 'equity'])

    return "Database updated successfully"

@shared_task
@transaction.atomic
def place_order_task(trading_profile_id, symbol, quantity, leverage, direction, stop_loss=None):
    trading_profile = TradingProfile.objects.get(pk=trading_profile_id)
        
    stop_loss = None if stop_loss is None else float(stop_loss)

    if quantity is None or quantity == "0":
        return {"error": "Quantity is required"}
    
    try:
        price = fetch_current_price(symbol, direction)
    except ValueError as e:
        return {"error": str(e)}
        
    amount = float(quantity) * float(price)
    if amount > 1000000:
        return {"error": "Order sizes cannot exceed $1,000,000"}
    margin_percentage = get_margin_percentage(amount)
    margin_required = amount * margin_percentage

    available_margin = trading_profile.balance

    open_position = OpenPositions.objects.filter(trading_profile=trading_profile).first()

    if open_position:
        available_margin = open_position.equity 

    if available_margin < margin_required:
        return {"error": "Insufficient available margin to place this order"}
    
    maintenance_amount = get_maintenance_margin_amount(amount)
    funding_cost = get_funding_cost(symbol, amount) * amount

    equity = available_margin - margin_required - funding_cost

    new_position = OpenPositions.objects.create(
        trading_profile=trading_profile,
        symbol=symbol.upper(),
        direction=direction.upper(),
        quantity=quantity,
        open_price=price,
        stop_loss=stop_loss,
        leverage=leverage,
        margin_used=margin_required,
        maintenance_amount=maintenance_amount,
        equity=equity,
        funding_cost = funding_cost,
    )

    new_position.save()
    print(trading_profile.balance)
    trading_profile.balance -= margin_required
    print(f"New balance is {trading_profile.balance}")
    trading_profile.save()

    return {"symbol": symbol, "quantity": quantity, "price": price, "amount": amount, "stop_loss": stop_loss}



    


def fetch_current_price(symbol, direction):
    
    if direction == "LONG":
        current_price = buy_price(symbol)
        
    elif direction == "SHORT":
        current_price = sell_price(symbol)

    return current_price

def get_margin_percentage(amount):
    if amount < 10000:
        return 0.005  
    elif 10000 <= amount < 100000:
        return 0.0065  
    elif 100000 <= amount < 500000:
        return 0.01

def get_maintenance_margin_amount(amount):
    if amount < 10000:
        return 0
    elif 10000 <= amount < 100000:
        return 50
    elif 100000 <= amount < 500000:
        return 400
    elif 500000 <= amount < 1000000:
        return 1800
    elif 1000000 <= amount:
        return 5100

def get_funding_cost(symbol, amount):
    if symbol == "BTC-USD":
        if amount < 10000:
            return 0.0001
        elif 10000 <= amount < 100000:
            return 0.0002
        elif 100000 <= amount < 500000:
            return 0.0005
        
    elif symbol == "ETH-USD":
        if amount < 10000:
            return 0.0003

def buy_price(symbol):
    now = str(int(time.time() * 1000)) + "-0"
    timestamp = str(int(time.time() * 1000) - 5000) + "-0"

    stream_key = f"{symbol}: data"
    messages = r.xrange(stream_key, min=timestamp, max=now)

    prices = []
    for message in messages:
        data_str = message[1][b'data'].decode('utf-8')
        data_list = json.loads(data_str)
        for item in data_list:
            price = float(item["price"])
            prices.append(price)
    
    if not prices:
        print("Error: No available pricing data")
        return None
    buy_price = max(prices)
    return buy_price
    
def sell_price(symbol):
    now = str(int(time.time() * 1000)) + "-0"
    timestamp = str(int(time.time() * 1000) - 5000) + "-0"

    stream_key = f"{symbol}: data"
    messages = r.xrange(stream_key, min=timestamp, max=now)

    prices = []
    for message in messages:
        data_str = message[1][b'data'].decode('utf-8')
        data_list = json.loads(data_str)
        for item in data_list:
            price = float(item["price"])
            prices.append(price)
    
    if not prices:
        print("Error: No available pricing data")
        return None
    sell_price = min(prices)
    return sell_price
    
def close_price(symbol, direction):
    now = str(int(time.time() * 1000)) + "-0"
    timestamp = str(int(time.time() * 1000) - 5000) + "-0"

    stream_key = f"{symbol}: data"
    messages = r.xrange(stream_key, min=timestamp, max=now)

    prices = []
    for message in messages:
        data_str = message[1][b'data'].decode('utf-8')
        data_list = json.loads(data_str)
        for item in data_list:
            price = float(item["price"])
            prices.append(price)
    
    if not prices:
        print("Error: No available pricing data")
        return None
    if direction == "LONG":
        close_price = min(prices)
    elif direction == "SHORT":
        close_price = max(prices)
    return close_price
    
def get_game_result():
    now = str(int(time.time() * 1000)) + "-0"
    timestamp = str(int(time.time() * 1000) - 1000) + "-0"

    stream_key = "BTC-USD: data"
    messages = r.xrange(stream_key, min=timestamp, max=now)

    prices = []
    for message in messages:
        data_str = message[1][b'data'].decode('utf-8')
        data_list = json.loads(data_str)
        for item in data_list:
            price = float(item["price"])
            prices.append(price)

    price = mean(prices)

# Liquidiation price calculation
# https://www.binance.com/en/support/faq/how-to-calculate-liquidation-price-of-usd%E2%93%A2-m-futures-contracts-b3c689c1f50a44cabb3a84e663b81d93