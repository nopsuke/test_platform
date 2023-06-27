from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser, UserProfile, OpenPositions,ClosedPositions
from django.db import transaction
from accounts.forms import CustomUserCreationForm, BuyForm, LeverageChangeForm
from django.contrib.auth.decorators import login_required
from trading.models import Trade
import string
import random
import logging
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .serializers import UserSerializer, UserProfileSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib import messages 
from trading.data_feed import ws
from decimal import Decimal
import redis
import json
from .tasks import place_order_task, close_position_task

logger = logging.getLogger(__name__)
# Works as intended after Celery changes.
class MarketBuyOrderView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        symbol = request.data.get("symbol")
        quantity = request.data.get("quantity")
        stop_loss = request.data.get("stop_loss")
        leverage = user_profile.leverage

        if not symbol or not quantity:
            raise ValidationError("Symbol and quantity are required.")
        
        try:
            place_order_task.delay(user_profile.id, symbol, quantity, leverage, stop_loss)
            return Response({"message": "Order is being processed."})
        except Exception as e:
            return Response({"error": str(e)}, status=400)



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



# Works as intended after Celery changes.
class ClosePositionView(APIView):
    authentication_classes = [TokenAuthentication]
    

    def post(self, request):
        open_position_id = request.data.get('id')

        if not open_position_id:
            raise ValidationError("Position id is required.")

        user_profile = UserProfile.objects.get(user=request.user)
        open_position = OpenPositions.objects.filter(id=open_position_id, user_profile=user_profile).first()

        if not open_position:
            raise ValidationError("No open position found for this user with this id.")
        try:
            close_position_task.delay(open_position.id, user_profile.id)
            return Response({"message": "Position is closed."})
        except Exception as e:
            return Response({"error": str(e)}, status=400)




        


        

class UserProfileRetrieveView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


def home(request):
    return render(request, 'accounts/hello.html', {})




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
        



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"detail": "Logout successful."})





# I think this is for changing or resetting the balance.
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
    
