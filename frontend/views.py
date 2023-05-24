from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser, UserProfile
from accounts.forms import CustomUserCreationForm, BuyForm, LeverageChangeForm
from django.contrib.auth.decorators import login_required
from trading.models import Trade
from trading.market_data import buy_order
import string
import random
# Completely unnecessary but will keep as a reference for now

def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')

# Why did I put this here? This whole thing is redundant and pointless I suspect. Created a new index view for the homepage.


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Generate a referral code for the new user
            new_user_referral_code = generate_referral_code()
            # Ensure the referral code is unique
            while UserProfile.objects.filter(referral_code=new_user_referral_code).exists():
                new_user_referral_code = generate_referral_code()

            # The UserProfile should already have been created by the signal
            user_profile = UserProfile.objects.get(user=user)
            user_profile.referral_code = new_user_referral_code

            # If the new user was referred by someone else, set the referrer
            referral_code = request.GET.get('referral_code', None)
            if referral_code:
                try:
                    referrer_profile = UserProfile.objects.get(referral_code=referral_code)
                    user_profile.referrer = referrer_profile.user
                except UserProfile.DoesNotExist:
                    pass

            user_profile.save()

            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def generate_referral_code():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not UserProfile.objects.filter(referral_code=code).exists():
            return code



def home(request):
    return render(request, 'accounts/hello.html', {})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    form = BuyForm()
    margin_used = 0

    if request.method == 'POST':
        form = BuyForm(request.POST)
        if form.is_valid():
            trade_size = form.cleaned_data['trade_size']
            price = form.cleaned_data['price']
            stop_loss = form.cleaned_data['stop_loss']

            buy_order(user_profile, 'EXAMPLE', trade_size, price, user_profile.leverage, stop_loss)
            margin_used = trade_size * price / user_profile.leverage

    return render(request, 'logged_in/dashboard.html', {'user_profile': user_profile, 'form': form, 'margin_used': margin_used})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')



@login_required
def reset_balance(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Set the user's balance to the default value (5000)
        user_profile.balance = 5000.00
        user_profile.save()

        return redirect('dashboard')

    return render(request, 'logged_in/reset_balance.html')





@login_required
def change_leverage(request):
    if request.method == 'POST':
        form = LeverageChangeForm(request.POST)
        if form.is_valid():
            leverage = form.cleaned_data['leverage']
            user_profile = request.user.userprofile
            user_profile.leverage = float(leverage)
            user_profile.save()
            return redirect('dashboard')
    else:
        form = LeverageChangeForm()

    return render(request, 'logged_in/change_leverage.html', {'form': form})



@login_required
def referrals(request):
    user_profile = UserProfile.objects.get(user=request.user)
    referred_profiles = request.user.referrals.all()
    context = {
        'user_profile': user_profile, 
        'referred_profiles': referred_profiles
    }
    return render(request, 'logged_in/referrals.html', context)


