from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Category, Product, Review
from .serializers import CategoryWithProductCountSerializer, ProductWithReviewsSerializer, ReviewSerializer

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithProductCountSerializer

class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithProductCountSerializer

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer

class ReviewListView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer