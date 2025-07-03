from django.urls import path
from .views import (
    CategoryListView, CategoryDetailView,
    ProductListView, ProductDetailView,
    ReviewListView, ReviewDetailView,
    CategoryCreateView, CategoryUpdateDeleteView,
    ProductCreateView, ProductUpdateDeleteView,
    ReviewCreateView, ReviewUpdateDeleteView,
    RegisterView, LoginView, ConfirmUserView
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', CategoryUpdateDeleteView.as_view(), name='category-update-delete'),
    
    # Products
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/edit/', ProductUpdateDeleteView.as_view(), name='product-update-delete'),
    
    # Reviews
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/edit/', ReviewUpdateDeleteView.as_view(), name='review-update-delete'),
    
    # Authentication
    path('users/register/', RegisterView.as_view(), name='user-register'),
    path('users/login/', LoginView.as_view(), name='user-login'),
    path('users/confirm/', ConfirmUserView.as_view(), name='user-confirm'),
]
