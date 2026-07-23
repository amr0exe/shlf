from django.urls import path
from .views import (
    MemberListCreateView,
    MemberRetrieveView,
    MemberUpdateView,
    MemberDeleteView
)

urlpatterns = [
    path('', MemberListCreateView.as_view(), name='member-list-create'),
    path('<int:id>/', MemberRetrieveView.as_view(), name='member-detail'),
    path('<int:id>/update/', MemberUpdateView.as_view(), name='member-update'),
    path('<int:id>/delete/', MemberDeleteView.as_view(), name='member-delete'),
]
