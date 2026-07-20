from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework import status

from utils.responses import StdResponse
from authors.serializers import AuthorCreateSerializer, AuthorReadSerializer
from .models import Author

class AuthorCreateView(CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = serializer.save()

        output_data = AuthorReadSerializer(author).data

        return StdResponse(
            data=output_data,
            message="Author profile created successfully",
            status_code=status.HTTP_201_CREATED
        )

class AuthorListView(ListAPIView):
    """
    Fetches every author
    """
    queryset = Author.objects.all().order_by('-created_at')
    serializer_class = AuthorReadSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return StdResponse(
            data=serializer.data,
            message="Authors list retrieved successfully."
        )

class AuthorRetrieveView(RetrieveAPIView):
    """
    Fetches single author
    """
    queryset = Author.objects.all()
    serializer_class = AuthorReadSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return StdResponse(
            data=serializer.data,
            message="Author profile fetched successfully."
        )

class AuthorDeleteView(DestroyAPIView):
    """
    Deletes authors record
    """
    queryset = Author.objects.all()
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        author_name = instance.name
        self.perform_destroy(instance)

        return StdResponse(
            data={"deleted_author_name": author_name},
            message=f"Author '{author_name}' deleted successfully."
        )
