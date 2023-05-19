from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class BuyForm(forms.Form):
    trade_size = forms.FloatField(label='Trade size', required=True)
    price = forms.FloatField(label='Price', required=True)
    stop_loss = forms.FloatField(label='Stop-loss (optional)', required=False)


class LeverageChangeForm(forms.Form):
    LEVERAGE_CHOICES = (
        (20, '1:20'),
        (50, '1:50'),
        (100, '1:100'),
    )

    leverage = forms.ChoiceField(choices=LEVERAGE_CHOICES, required=True)
    
class SellForm(forms.Form):
    trade_size = forms.FloatField(label='Trade size', required=True)
    price = forms.FloatField(label='Price', required=True)
    stop_loss = forms.FloatField(label='Stop-loss (optional)', required=False)


