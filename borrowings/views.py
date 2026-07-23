from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView
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

class BorrowListView(ListAPIView):
    """
    List all borrowing records with optional status and member filtering.
    QueryParams:
      - status: borrowed | returned | overdue
      - member_id: <int>
      - overdue: true
    """
    serializer_class = BorrowingReadSerializer

    def get_queryset(self):
        queryset = Borrowing.objects.select_related(
            'member',
            'copy',
            'copy__book'
        ).all().order_by('-borrowed_at')

        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        # Filter by member ID
        member_id = self.request.query_params.get('member_id')
        if member_id:
            queryset = queryset.filter(member_id=member_id)

        # Filter active overdue loans
        is_overdue = self.request.query_params.get('overdue')
        if is_overdue and is_overdue.lower() == 'true':
            queryset = queryset.filter(
                status=Borrowing.BorrowStatus.BORROWED,
                due_at__lt=timezone.now()
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return StdResponse(
            data=serializer.data,
            message="Borrowing records retrieved successfully."
        )


class BorrowDetailView(RetrieveAPIView):
    """
    Fetch details for a specific borrowing transaction record.
    """
    queryset = Borrowing.objects.select_related('member', 'copy', 'copy__book').all()
    serializer_class = BorrowingReadSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return StdResponse(
            data=serializer.data,
            message="Borrowing details retrieved successfully."
        )
