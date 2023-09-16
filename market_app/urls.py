from django.urls import path

from market_app.apps import MarketAppConfig
from market_app.views import CardView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductListAPIView
from users.models import User

app_name = MarketAppConfig.name

urlpatterns = [
    path('admin/auth/user/', User, name='admin'),
    path('index/<int:pk>/', CardView.as_view(), name='card'),
    path('product/create/', ProductCreateView.as_view(), name='prod_create'),
    path('product/list/', ProductListAPIView.as_view(), name='prod_list'),
    path('product/update/<int:pk>', ProductUpdateView.as_view(), name='prod_update'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(), name='prod_delete')
]
