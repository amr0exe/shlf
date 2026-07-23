from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from rest_framework.generics import CreateAPIView
from rest_framework import status
from utils.responses import StdResponse

from .models import Borrowing
from .serializers import BorrowCheckoutSerializer, BorrowingReadSerializer


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
