from rest_framework import serializers
from accounts.models import CustomUser, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'bio', "balance", "leverage", "margin_level", "open_positions", "referral_code", "referrer")


# This wouldn't work. Serializer needs more information to work with. 