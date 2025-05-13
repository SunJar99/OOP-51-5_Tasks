from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from .models import Category, Product, Review
from .serializers import (CategoryWithProductCountSerializer, ProductWithReviewsSerializer,
                          ReviewSerializer)

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