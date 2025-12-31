from django.contrib import admin
from django.urls import path
from django.shortcuts import render

# fungsi Landing Page
def landing_page(request):
    return render(request, 'landing.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing') #landing Page View
]
