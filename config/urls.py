from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from apps.users.views import register_view, login_view, dashboard_view,logout_view #import views dari apps.users
from django.urls import include

# fungsi Landing Page
def landing_page(request):
    return render(request, 'landing.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing'), #landing Page View
    path('register/', register_view, name='register'), #register view
    path('login/', login_view, name='login'), #login view
    path('dashboard/', dashboard_view, name='dashboard'), #dashboard view
    path('logout/', logout_view, name='logout'), #logout view
    path('strategy/', include('apps.strategy.urls')), #include urls dari apps.strategy
    ]
