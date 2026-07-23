from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework import status
from utils.responses import StdResponse

from .models import Member
from .serializers import MemberSerializer


class MemberListCreateView(ListCreateAPIView):
    queryset = Member.objects.all().order_by('-created_at')
    serializer_class = MemberSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return StdResponse(
            data=serializer.data,
            message="Members list retrieved successfully."
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        return StdResponse(
            data=MemberSerializer(member).data,
            message="Member registered successfully.",
            status_code=status.HTTP_201_CREATED
        )


class MemberRetrieveView(RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return StdResponse(
            data=serializer.data,
            message="Member details retrieved successfully."
        )


class MemberUpdateView(UpdateAPIView):
    """
    Endpoint to update member information (supports PUT and PATCH).
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        return StdResponse(
            data=MemberSerializer(member).data,
            message="Member details updated successfully."
        )


class MemberDeleteView(DestroyAPIView):
    """
    Endpoint to remove a member record.
    """
    queryset = Member.objects.all()
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        member_name = instance.name
        self.perform_destroy(instance)

        return StdResponse(
            data={"deleted_member_name": member_name},
            message=f"Member '{member_name}' deleted successfully."
        )
