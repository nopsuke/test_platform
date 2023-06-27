from django.test import TestCase
import redis

# Create a Redis client
r = redis.Redis(host='localhost', port=6379, db=0)

# Retrieve all items from a list in Redis
data_list = r.lrange('data_queue', 0, -1)

# Retrieve a value from Redis by key
value = r.get('BTC-USD')

# Print the retrieved data
print(data_list)
print(value)

"""
@app.task
def redis_test():
    logger.info("Redis test")
    r = redis.Redis(host='localhost', port=6379, db=0)
    print(r.get('BTC-USD'))
"""
"""
@app.task
def get_current_buy_price(symbol):
    logger.info("Connecting to Redis")
    r = redis.Redis(host='localhost', port=6379, db=0)
    price_data = r.get(symbol)
    if price_data is not None:
        data = json.loads(price_data)
        print("Price:", data['price'])
        return data['price']
    else:
        return "Issue with data feed"
"""
#get_current_buy_price.apply_async(args=["BTC-USD"])

 #   "redis_test": {
  #      "task": "accounts.tasks.redis_test",
 #       "schedule": 15.0,
 #   },

#    "get_current_buy_price": {
 #       "task": "monreal.celery.get_current_buy_price",
  #      "schedule": 30.0,

   # },