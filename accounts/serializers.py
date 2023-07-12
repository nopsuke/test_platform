from rest_framework import serializers
from .models import CustomUser, UserProfile, TradingProfile
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']

        # Ensure passwords are set correctly
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            }
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use")
        return value
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", 'avatar', 'bio', 'referral_code', 'referrer']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if user is None:
                raise serializers.ValidationError("Incorrect Credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        data['user'] = user
        return data

# No idea if this works properly, need to test.


class MarketOrderSerializer(serializers.Serializer):
    profile_id = serializers.IntegerField(required=True)
    symbol = serializers.CharField(max_length=100, required=True)
    quantity = serializers.FloatField(required=True)
    stop_loss = serializers.FloatField(required=False, allow_null=True)
    direction = serializers.ChoiceField(choices=["LONG", "SHORT"], required=True)


class TradingProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingProfile
        fields = ["id", "user_profile", "name", "balance", "leverage"]