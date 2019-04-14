from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('<int:pk>/create', views.PageCreateView.as_view(), name='page_create'),
    path('<int:pk>/renew', views.BookRenewView.as_view(), name='book_renew'),
    path('create', views.BookCreateView.as_view(), name='book_create'),
]
