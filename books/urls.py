from django.urls import path
from .views import BookCreateView, BookListView, BookRetrieveView

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:id>/', BookRetrieveView.as_view(), name='book-detail'),
]
