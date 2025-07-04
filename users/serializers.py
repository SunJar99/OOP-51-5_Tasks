from rest_framework import serializers
from .models import User, ConfirmationCode
from django.contrib.auth import authenticate
import random
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add birth_date and is_adult claims to token
        token['birth_date'] = user.birth_date.isoformat() if user.birth_date else None
        token['is_adult'] = user.is_adult
        
        return token

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'birth_date']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        # Generate 6-digit code
        code = f"{random.randint(100000, 999999)}"
        ConfirmationCode.objects.create(user=user, code=code)
        
        # Use Celery task to send OTP email asynchronously
        from .tasks import send_otp_email
        send_otp_email.delay(user.id, code)
        
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("User is not confirmed")
        data['user'] = user
        return data

class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
            if user.is_active:
                raise serializers.ValidationError("User is already confirmed")
            if user.confirmation_code.code != data['code']:
                raise serializers.ValidationError("Invalid confirmation code")
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        return data

    def save(self, **kwargs):
        user = User.objects.get(username=self.validated_data['username'])
        user.is_active = True
        user.save()
        user.confirmation_code.delete()
        return user