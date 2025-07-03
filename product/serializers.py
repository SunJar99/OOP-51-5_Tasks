from rest_framework import serializers
from .models import Category, Product, Review
from users.models import User, ConfirmationCode  
from django.contrib.auth import authenticate

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название категории не может быть пустым.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True, min_value=0)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название товара не может быть пустым.")
        return value

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Описание товара не может быть пустым.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    stars = serializers.IntegerField(min_value=1, max_value=5, required=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)

    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Текст отзыва не может быть пустым.")
        return value


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'average_rating']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return sum(review.stars for review in reviews) / reviews.count()
        return 0

class CategoryWithProductCountSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.products.count()
    
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            is_active=False
        )
        # Create confirmation code
        ConfirmationCode.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("Неверные учетные данные или пользователь не активирован")

class ConfirmSerializer(serializers.Serializer):
    code = serializers.CharField()
    
    def validate(self, data):
        try:
            confirmation = ConfirmationCode.objects.get(code=data['code'])
            data['confirmation'] = confirmation
            return data
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError("Неверный код подтверждения")
    
    def save(self):
        confirmation = self.validated_data['confirmation']
        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()
        return user


