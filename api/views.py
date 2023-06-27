from django.shortcuts import render
from rest_framework import generics
from accounts.models import CustomUser, UserProfile, OpenPositions
from .serializers import UserSerializer, UserProfileSerializer, OpenPositionsSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view



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


class OpenPositionsView(generics.ListAPIView):
    queryset = OpenPositions.objects.all()
    serializer_class = OpenPositionsSerializer
    
    


