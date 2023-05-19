from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Market(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    market_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    swap_charge = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

class Trade(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    trade_type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    quantity = models.DecimalField(max_digits=15, decimal_places=8)
    price = models.DecimalField(max_digits=15, decimal_places=8)
    trade_date = models.DateTimeField(auto_now_add=True)
    stop_loss = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=True) # Need to look into this, see if it can be kept nullable.


    def __str__(self):
        return f"{self.user.username} - {self.trade_type} - {self.market.symbol}"


    
# I'm thinking I need a class for each type of market, and then a class for each type of asset. Should I have a class for each type of trade? I think so. Buy/sell directions
# Maybe current classes will do, dont know. Need to think about it.
