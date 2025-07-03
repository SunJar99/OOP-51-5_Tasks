from django.contrib.auth import authenticate
from rest_framework.generics import (ListAPIView, RetrieveAPIView,
                                    CreateAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (CategoryWithProductCountSerializer, ProductWithReviewsSerializer,
                          ReviewSerializer, RegisterSerializer, LoginSerializer, ConfirmSerializer)
from django.contrib.auth import login
from users.models import User
# Category views

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithProductCountSerializer
    
class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithProductCountSerializer
    
class CategoryUpdateDeleteView(UpdateAPIView, DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithProductCountSerializer

class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithProductCountSerializer

# Product views

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer


class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer

class ProductUpdateDeleteView(UpdateAPIView, DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer

# Review views

class ReviewListView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
class ReviewCreateView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewUpdateDeleteView(UpdateAPIView, DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    

# Authentication views
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Пользователь зарегистрирован. Проверьте email для подтверждения."}, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            login(request, serializer.validated_data['user'])
            return Response({"detail": "Успешный вход."})
        return Response(serializer.errors, status=400)

class ConfirmUserView(APIView):
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Пользователь подтвержден."})
        return Response(serializer.errors, status=400)
