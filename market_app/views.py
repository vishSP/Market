from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from rest_framework import permissions
from rest_framework.generics import DestroyAPIView, UpdateAPIView, CreateAPIView, RetrieveAPIView

from market_app.models import Product
from market_app.pagination import MarketPagination


class CardView(RetrieveAPIView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateAPIView):
    model = Product
    pagination_class = MarketPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class ProductUpdateView(LoginRequiredMixin, UpdateAPIView):
    model = Product
    permission_classes = [permissions.IsAuthenticated]


class ProductDeleteView(LoginRequiredMixin, DestroyAPIView):
    model = Product
    permission_classes = [permissions.IsAuthenticated]
