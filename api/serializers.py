from rest_framework import serializers
from accounts.models import CustomUser, UserProfile, OpenPositions, ClosedPositions

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'bio', "balance", "leverage",  "referral_code", "referrer")

class OpenPositionsSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
    class Meta:
        model = OpenPositions
        fields = "__all__"

class ClosedPositionsSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
    class Meta:
        model = ClosedPositions
        fields = "__all__"       
# This wouldn't work. Serializer needs more information to work with. 