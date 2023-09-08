from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from rest_framework import permissions

from market_app.models import Product
from market_app.pagination import MarketPagination


class CardView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object']
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    pagination_class = MarketPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    permission_classes = [permissions.IsAuthenticated]


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    permission_classes = [permissions.IsAuthenticated]
