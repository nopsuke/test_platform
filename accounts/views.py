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
import logging
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer, UserProfileSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib import messages 

logger = logging.getLogger(__name__)



"""def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})///"""


"""def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Generate a referral code for the new user
            referral_code = generate_referral_code()
            # Ensure the referral code is unique
            while UserProfile.objects.filter(referral_code=referral_code).exists():
                referral_code = generate_referral_code()

            # The UserProfile should already have been created by the signal
            user_profile = UserProfile.objects.get(user=user)
            user_profile.referral_code = referral_code
            user_profile.save()

            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})"""

"""def register(request):
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
"""

# User is generated as intended but referral code is not generated. All other data seems to OK as well.
class RegisterView(APIView):

    @staticmethod
    def generate_referral_code():
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not UserProfile.objects.filter(referral_code=code).exists():
                return code

    
    def post(self, request):
        print("RegisterView POST method called")
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            logger.debug("Serializer is valid")
            user = serializer.save()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user) # This should add a new token to the database if the user doesn't have one already.

            # Generate a referral code for the new user
            new_user_referral_code = self.generate_referral_code()
            
            
            try:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.referral_code = new_user_referral_code

            except Exception as e:
                print("UserProfile does not exist", str(e))
                

            # If the new user was referred by someone else, set the referrer
            referring_code = request.data.get('referral_code', None)
            if referring_code:
                try:
                    referrer_profile = UserProfile.objects.get(referral_code=referring_code)
                    user_profile.referrer = referrer_profile.user
                except UserProfile.DoesNotExist:
                    logger.error("Referred UserProfile does not exist")
                    pass

            user_profile.save()
            logger.debug("User profile saved")

            return Response({"token": token.key, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        
        logger.error("Serializer is invalid. Errors: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BuyOrderView(APIView):
    permission_classes = [IsAuthenticated] # Should also check if the user is logged in / verified.
    authentication_classes = [TokenAuthentication] # Added token authentication.

    def post(self, request, format=None):
        user_profile = UserProfile.objects.get(user=request.user)
        trade_size = request.data['trade_size']
        price = request.data['price']
        stop_loss = request.data['stop_loss']

        buy_order(user_profile, 'EXAMPLE', trade_size, price, user_profile.leverage, stop_loss)
        margin_used = trade_size * price / user_profile.leverage

        return Response({'margin_used': margin_used})

class UserProfileRetrieveView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


def home(request):
    return render(request, 'accounts/hello.html', {})


"""def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})"""

"""class LoginView(APIView): # Need to look into rest_framework.authtoken.views.obtain_auth_token and implement here and in a few other places but dont know how to generate tokens etc.
    authentication_classes = [TokenAuthentication]


    def post(self, request, *args, **kwargs):
        print("Starting LoginView")
        form = AuthenticationForm(data=request.data)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "message": "User logged in successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)"""

class LoginView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        print("Starting LoginView")
        serializer = LoginSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "message": "User logged in successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

"""@login_required
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
"""
"""@login_required
def logout_view(request):
    logout(request)
    return redirect('home')"""

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"detail": "Logout successful."})



"""@login_required
def reset_balance(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Set the user's balance to the default value (5000)
        user_profile.balance = 5000.00
        user_profile.save()

        return redirect('dashboard')

    return render(request, 'logged_in/reset_balance.html')"""


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)

        
        user_profile_data = UserProfileSerializer(user_profile).data

        return Response(user_profile_data)

    def post(self, request, *args, **kwargs): # This should reset the balance to 5000. Double check it doesn't add like it did before.
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.balance = 5000.00
        user_profile.save()

        # Returns updated profile data.
        user_profile_data = UserProfileSerializer(user_profile).data
        return Response(user_profile_data)




"""@login_required
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

    return render(request, 'logged_in/change_leverage.html', {'form': form})"""

class LeverageView(APIView):
    permission_classes = [IsAuthenticated] # What the hell is it authenticating? The logged in status? Not sure this would work, can add a token generation to login.
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        
        # Serialize the data into JSON format
        user_profile_data = UserProfileSerializer(user_profile).data

        return Response(user_profile_data)

    def put(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""@login_required
def referrals(request):
    user_profile = UserProfile.objects.get(user=request.user)
    referred_profiles = request.user.referrals.all()
    context = {
        'user_profile': user_profile, 
        'referred_profiles': referred_profiles
    }
    return render(request, 'logged_in/referrals.html', context)
"""

"""
@login_required
def referrals(request):

"""

#class RegisterView(generics.CreateAPIView):
 #   queryset = CustomUser.objects.all()
  #  serializer_class = UserSerializer


class ReferralsView(APIView): # IsAuthenticated is fine here. IsAuthenticated just checks if user is logged in although I'm not sure what it is authenticating currently.
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        referred_profiles = request.user.referrals.all()

        # Serialize the data into JSON format
        user_profile_data = UserProfileSerializer(user_profile).data
        referred_profiles_data = UserProfileSerializer(referred_profiles, many=True).data

        context = {
            'user_profile': user_profile_data,
            'referred_profiles': referred_profiles_data
        }

        return Response(context)
    
