from django.shortcuts import render
from rest_framework import generics
from accounts.models import CustomUser, UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from trading.market_data import fetch_time_series_data, buy_order, sell_order, calculate_equity

# I feel like this is redundant, but maybe it isn't? I don't know. I'll leave it for now.

class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer



@api_view(['GET'])
def time_series_data(request, symbol):
    data = fetch_time_series_data(symbol)
    return JsonResponse(data)


@api_view(['POST'])
def create_buy_order(request):
    symbol = request.data.get('symbol')
    quantity = request.data.get('quantity')

    if not symbol or not quantity:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    user_profile = UserProfile.objects.get(user=request.user)
    trade = buy_order(user_profile, symbol, float(quantity))

    if 'error' in trade:
        return JsonResponse(trade, status=400)

    return JsonResponse(trade)

@api_view(['POST'])
def create_sell_order(request):
    symbol = request.data.get('symbol')
    quantity = request.data.get('quantity')

    if not symbol or not quantity:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    user_profile = UserProfile.objects.get(user=request.user)
    trade = sell_order(user_profile, symbol, float(quantity))

    if 'error' in trade:
        return JsonResponse(trade, status=400)

    return JsonResponse(trade)


@api_view(['GET'])
def get_equity(request):
    user_profile = UserProfile.objects.get(user=request.user)
    equity = calculate_equity(user_profile)
    return JsonResponse({'equity': equity})

