from django.urls import path


from . import views

app_name = 'main'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('favicon.ico', views.FaviconView.as_view(), name='favicon'),
]
