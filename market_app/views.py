from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import permissions
from rest_framework.generics import DestroyAPIView, UpdateAPIView, CreateAPIView, RetrieveAPIView

from market_app.models import Product
from market_app.pagination import MarketPagination
from market_app.serializers import ProductSerializer


class CardView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(LoginRequiredMixin, CreateAPIView):
    queryset = Product.objects.all()
    pagination_class = MarketPagination
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductUpdateView(LoginRequiredMixin, UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductDeleteView(LoginRequiredMixin, DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
