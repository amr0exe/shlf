from django.urls import path
from .views import BorrowCheckoutView, BorrowDetailView, BorrowReturnView, BorrowListView

urlpatterns = [
    path('', BorrowListView.as_view(), name='borrow-list'),
    path('<int:id>/', BorrowDetailView.as_view(), name='borrow-detail'),
    path('checkout/', BorrowCheckoutView.as_view(), name='borrow-checkout'),
    path('return/', BorrowReturnView.as_view(), name='borrow-return'),
]
