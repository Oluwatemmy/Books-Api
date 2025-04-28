from django.urls import path
from .views import CreateBookView, ListAllBookView, ListABookView, DeleteBookView, UpdateAPIView

urlpatterns = [
    path('books/', CreateBookView.as_view(), name='book-list'),
    path('books/<int:pk>/', ListABookView.as_view(), name='book-detail'),
    path('books/all/', ListAllBookView.as_view(), name='book-list-all'),
    path('books/delete/<int:pk>/', DeleteBookView.as_view(), name='book-delete'),
    path('books/update/<int:pk>/', UpdateAPIView.as_view(), name='book-update'),
]
