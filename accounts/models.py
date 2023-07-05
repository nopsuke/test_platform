from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import random, string


class CustomUser(AbstractUser):
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    balance = models.FloatField(default=5000.00)
    leverage = models.FloatField(default=20.0)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referrer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True, related_name='referrals')

    def __str__(self):
        return self.user.username


POSITION_DIRECTIONS = [
   ('LONG', 'Long'),
   ('SHORT', 'Short'),
]

class OpenPositions(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=15)
    direction = models.CharField(max_length=5, choices=POSITION_DIRECTIONS)
    quantity = models.FloatField()
    open_price = models.FloatField()
    open_time = models.DateTimeField(auto_now_add=True)
    stop_loss = models.FloatField(null=True, blank=True)
    leverage = models.FloatField(default=20.0)
    liquidation_price = models.FloatField(null=True, blank=True)
    margin_used = models.FloatField(default=0.0)
    maintenance_amount = models.FloatField(default=0.0)
    equity = models.FloatField(default=0.0)
    profit_or_loss = models.FloatField(default=0.00)
    funding_cost = models.FloatField(default=0.00)
    funding_rate = models.FloatField(default=0.00)



class ClosedPositions(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=15)
    direction = models.CharField(max_length=5, choices=POSITION_DIRECTIONS)
    quantity = models.FloatField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    open_time = models.DateTimeField()
    close_time = models.DateTimeField(auto_now_add=True)
    stop_loss = models.FloatField(null=True, blank=True)
    profit_or_loss = models.FloatField(default=0.00)
    leverage = models.FloatField(default=20.0)
    fund_cost = models.FloatField(default=0.00)



class BattleGame(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    points = models.IntegerField(default=1000)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)

    def record_win(self):
        self.wins += 1
        self.streak += 1
        self.points += 3
        if self.streak == 3:
            self.points += 5
        self.save()

    def record_loss(self):
        self.losses += 1
        self.streak = 0
        self.points -= 2
        self.save()




@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


