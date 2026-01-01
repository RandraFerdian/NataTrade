from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from apps.users.views import register_view, login_view #import views dari apps.users

# fungsi Landing Page
def landing_page(request):
    return render(request, 'landing.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing'), #landing Page View
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    ]
