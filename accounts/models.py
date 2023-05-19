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
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    balance = models.FloatField(default=5000.00)
    leverage = models.FloatField(default=1.0)
    margin_level = models.FloatField(default=100.0)
    open_positions = models.JSONField(default=dict)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referrer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True, related_name='referrals')

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


