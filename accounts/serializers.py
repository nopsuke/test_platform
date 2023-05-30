from rest_framework import serializers
from .models import CustomUser, UserProfile 

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
        fields = ["id", 'balance', 'avatar', 'bio', 'leverage', 'margin_level', 'open_positions', 'referral_code', 'referrer']


# No idea if this works properly, need to test.
