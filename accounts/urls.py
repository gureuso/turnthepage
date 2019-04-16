
from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('verify_email', views.VerifyEmailView.as_view(), name='verify_email'),
]
