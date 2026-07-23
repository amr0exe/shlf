from django.urls import path
from .views import BookCreateView, BookDeleteView, BookListView, BookRetrieveView, BookUpdateView

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:id>/', BookRetrieveView.as_view(), name='book-detail'),
    path('<int:id>/update/', BookUpdateView.as_view(), name='book-update'),
    path('<int:id>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
