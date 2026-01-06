from django.urls import path
from .views import nata_strategi_view, edit_trade_view

urlpatterns = [
    path('', nata_strategi_view, name='nata_strategi'),
    path('edit/<int:pk>/', edit_trade_view, name='edit_trade'),
]