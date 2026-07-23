from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework import status
from utils.responses import StdResponse

from .models import Book
from .serializers import BookCreateSerializer, BookReadSerializer

class BookCreateView(CreateAPIView):
    """
    Endpoint to register a new book entity in the library system.
    """
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()

        output_data = BookReadSerializer(book).data

        return StdResponse(
            data=output_data,
            message="Book recorded registered successfully.",
            status_code=status.HTTP_201_CREATED
        )

class BookListView(ListAPIView):
    """
    Fetches every book in the library system.
    """
    serializer_class = BookReadSerializer
    queryset = Book.objects.all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return StdResponse(
            data=serializer.data,
            message="Book list retrieved successfully"
        )

class BookRetrieveView(RetrieveAPIView):
    """
    Fetches a single book by ID.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookReadSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return StdResponse(
            data=serializer.data,
            message="Book details fetched successfully."
        )
