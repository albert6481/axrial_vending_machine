from django.urls import path
from .views import vending_machine_view, ItemListAPIView, ItemPurchaseAPIView

urlpatterns = [
    # Frontend
    path('', vending_machine_view, name='vending-machine'),

    # Backend
    path('api/v1/items/', ItemListAPIView.as_view(), name='item-list'),
    path('api/v1/items/purchase/', ItemPurchaseAPIView.as_view(), name='item-purchase'),
]