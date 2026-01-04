from django.urls import path
from .views import nata_strategi_view

urlpatterns = [
    path('', nata_strategi_view, name='nata_strategi'),
]