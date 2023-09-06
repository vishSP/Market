from django.contrib import admin

from market_app.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price',)
    list_filter = ('name',)
    search_fields = ('name',)

