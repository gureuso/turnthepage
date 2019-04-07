from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('signup', views.SignupView.as_view(), name='signup'),
]
