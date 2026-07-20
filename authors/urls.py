from django.urls import path
from .views import AuthorCreateView, AuthorDeleteView, AuthorListView, AuthorRetrieveView

urlpatterns = [
    path('create/', AuthorCreateView.as_view(), name='author-create'),
    path('list/', AuthorListView.as_view(), name='author-list'),
    path('<int:id>/', AuthorRetrieveView.as_view(), name='author-detail'),
    path('delete/<int:id>/', AuthorDeleteView.as_view(), name='author-delete')
]
