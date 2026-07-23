from django.urls import path
from .views import BorrowCheckoutView

urlpatterns = [
    path('checkout/', BorrowCheckoutView.as_view(), name='borrow-checkout'),
]
