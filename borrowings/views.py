from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import status
from utils.responses import StdResponse

from .models import Borrowing
from .serializers import BorrowCheckoutSerializer, BorrowReturnSerializer, BorrowingReadSerializer


class BorrowCheckoutView(CreateAPIView):
    """
    Endpoint to process a book checkout by book_id for a member.
    """
    queryset = Borrowing.objects.all()
    serializer_class = BorrowCheckoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        member = serializer.validated_data['member']
        copy = serializer.validated_data['available_copy']
        days = serializer.validated_data.get('days', 14)

        with transaction.atomic():
            borrowing = Borrowing.objects.create(
                member=member,
                copy=copy,
                due_at=timezone.now() + timedelta(days=days),
                status=Borrowing.BorrowStatus.BORROWED
            )

            copy.is_available = False
            copy.save(update_fields=['is_available'])

        output_data = BorrowingReadSerializer(borrowing).data

        return StdResponse(
            data=output_data,
            message=f"Book '{copy.book.title}' (Copy #{copy.id}) successfully checked out to {member.name}.",
            status_code=status.HTTP_201_CREATED
        )

class BorrowReturnView(GenericAPIView):
    """
    Endpoint to process returning a borrowed book copy and restoring stock.
    """
    queryset = Borrowing.objects.all()
    serializer_class = BorrowReturnSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        borrowing = serializer.validated_data['borrowing']
        copy = borrowing.copy

        with transaction.atomic():
            borrowing.returned_at = timezone.now()
            borrowing.status = Borrowing.BorrowStatus.RETURNED
            borrowing.save(update_fields=['returned_at', 'status', 'updated_at'])

            copy.is_available = True
            copy.save(update_fields=['is_available'])

        output_data = BorrowingReadSerializer(borrowing).data

        return StdResponse(
            data=output_data,
            message=f"Book '{copy.book.title}' (Copy #{copy.id}) successfully returned by {borrowing.member.name}."
        )
