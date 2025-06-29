from rest_framework import serializers
from .models import User, ConfirmationCode
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        # Генерация 6-значного кода
        import random
        code = f"{random.randint(100000, 999999)}"
        ConfirmationCode.objects.create(user=user, code=code)
        # Здесь можно отправить код на email
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Неверные учетные данные")
        if not user.is_active:
            raise serializers.ValidationError("Пользователь не подтвержден")
        data['user'] = user
        return data

class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
            if user.is_active:
                raise serializers.ValidationError("Пользователь уже подтвержден")
            if user.confirmation_code.code != data['code']:
                raise serializers.ValidationError("Неверный код подтверждения")
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")
        return data

    def save(self, **kwargs):
        user = User.objects.get(username=self.validated_data['username'])
        user.is_active = True
        user.save()
        user.confirmation_code.delete()
        return user
