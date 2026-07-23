from django.urls import path
from .views import BorrowCheckoutView, BorrowReturnView

urlpatterns = [
    path('checkout/', BorrowCheckoutView.as_view(), name='borrow-checkout'),
    path('return/', BorrowReturnView.as_view(), name='borrow-return'),
]
