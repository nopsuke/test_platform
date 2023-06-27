from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import OpenPositions, UserProfile, ClosedPositions
from django.db import models, transaction
import logging
import redis
import json
from rest_framework.exceptions import ValidationError


logger = logging.getLogger(__name__)

@shared_task
@transaction.atomic
def close_position_task(open_position_id, user_profile_id):
    try:
        user_profile = UserProfile.objects.get(id=user_profile_id)
        open_position = OpenPositions.objects.get(id=open_position_id)
        
    except (UserProfile.DoesNotExist, OpenPositions.DoesNotExist):
        logger.error(f"No UserProfile with id={user_profile_id} or OpenPositions with id={open_position_id}")
        return
    
    close_price = fetch_current_price(open_position.symbol)
    if not close_price:
        logger.error(f"Could not fetch current price for {open_position.symbol}")
        return

    if open_position.direction == "LONG":
        profit_or_loss = (float(close_price) - float(open_position.open_price)) * float(open_position.quantity)
    else: # SHORT
        profit_or_loss = (float(open_position.open_price) - float(close_price)) * float(open_position.quantity)
    print(f"Previous balance: {user_profile.balance}")
    user_profile.balance += profit_or_loss + open_position.margin_used
    print(f"New balance: {user_profile.balance}")
    user_profile.save()

    closed_position = ClosedPositions.objects.create(
        user_profile=user_profile,
        symbol=open_position.symbol,
        direction=open_position.direction,
        quantity=open_position.quantity,
        open_price=open_position.open_price,
        close_price=float(close_price),
        open_time=open_position.open_time,
        profit_or_loss=profit_or_loss,
        leverage=open_position.leverage
    )

    open_position.delete()

    return {"symbol": closed_position.symbol,
            "quantity": closed_position.quantity,
            "open_price": closed_position.open_price,
            "close_price": closed_position.close_price,
            "profit_or_loss": closed_position.profit_or_loss}




@shared_task
def db_update_task():
    user_profiles = UserProfile.objects.all()
    symbol_price = {}

    for user_profile in user_profiles:
        open_positions = OpenPositions.objects.filter(user_profile=user_profile)
        total_pnl = 0
        total_margin_used = 0

        for position in open_positions:
            if not position.symbol in symbol_price:
                symbol_price[position.symbol] = fetch_current_price(position.symbol)

            current_price = symbol_price[position.symbol]

            pnl = ((current_price - position.open_price) * position.quantity) if position.direction == 'LONG' else ((position.open_price - current_price) * position.quantity)
            position.profit_or_loss = pnl
            total_pnl += pnl
            total_margin_used += position.margin_used

        equity = user_profile.balance + total_pnl

        for position in open_positions:
            margin_level = (equity / total_margin_used) * 100 if total_margin_used > 0 else float('inf')
            position.equity = equity
            logger.info(f"Current margin level for {user_profile.user.username} is {margin_level}")
            if margin_level < 120:
                logger.warning(f"Margin call! Margin level below 120% for {user_profile.user.username}! Please add funds or close positions to avoid liquidation!")
            elif margin_level < 70:
                logger.warning(f"THIS IS WHERE THE LIQUIDATION FUNCTION WILL BE CALLED for {user_profile.user.username}!")

        OpenPositions.objects.bulk_update(open_positions, ['profit_or_loss', 'equity'])

    return "Database updated successfully"

@shared_task
@transaction.atomic
def place_order_task(user_profile_id, symbol, quantity, leverage, stop_loss=None):
    user_profile = UserProfile.objects.get(pk=user_profile_id)

    price = fetch_current_price(symbol)
        
    if not price:
        return {"error": "No price found for this symbol"}
    if quantity is None or quantity == "0":
        return {"error": "Quantity is required"}
    
    amount = float(quantity) * float(price)
    if amount > 1000000:
        return {"error": "Order sizes cannot exceed $1,000,000"}
    margin_percentage = get_margin_percentage(amount)
    margin_required = amount * margin_percentage

    available_margin = user_profile.balance

    open_position = OpenPositions.objects.filter(user_profile=user_profile).first()

    if open_position:
        available_margin = open_position.equity 

    if available_margin < margin_required:
        return {"error": "Insufficient available margin to place this order"}
    
    maintenance_amount = get_maintenance_margin_amount(amount)

    equity = available_margin - margin_required

    new_position = OpenPositions.objects.create(
        user_profile=user_profile,
        symbol=symbol,
        direction='LONG',
        quantity=quantity,
        open_price=price,
        stop_loss=stop_loss,
        leverage=leverage,
        margin_used=margin_required,
        maintenance_amount=maintenance_amount,
        equity=equity,
    )

    new_position.save()
    print(user_profile.balance)
    user_profile.balance -= margin_required
    print(f"New balance is {user_profile.balance}")
    user_profile.save()

    return {"symbol": symbol, "quantity": quantity, "price": price, "amount": amount, "stop_loss": stop_loss}


def fetch_current_price(symbol):
    r = redis.Redis(host='localhost', port=6379, db=0)
    current_price = r.get("BTC-USD")
    if current_price is not None:
        data = json.loads(current_price)
        current_price = data["price"]
    else:
        return "Issue with data"
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
    

# Liquidiation price calculation
# https://www.binance.com/en/support/faq/how-to-calculate-liquidation-price-of-usd%E2%93%A2-m-futures-contracts-b3c689c1f50a44cabb3a84e663b81d93