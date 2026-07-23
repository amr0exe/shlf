from rest_framework import serializers

from members.models import Member
from books.models import Book, BookCopy
from .models import Borrowing


class BorrowCheckoutSerializer(serializers.Serializer):
    member_id = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
        source='member'
    )
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source='book'
    )
    days = serializers.IntegerField(
        required=False,
        default=14,
        min_value=1,
        max_value=60
    )

    def validate(self, attrs):
        book = attrs['book']

        available_copy = BookCopy.objects.filter(book=book, is_available=True).first()

        if not available_copy:
            raise serializers.ValidationError({
                "book_id": f"No available copies for '{book.title}'. All physical copies are currently checked out."
            })

        attrs['available_copy'] = available_copy
        return attrs


class BorrowingReadSerializer(serializers.ModelSerializer):
    """
    Serializer for returning formatted borrow receipts.
    """
    member_name = serializers.CharField(source='member.name', read_only=True)
    member_email = serializers.CharField(source='member.email', read_only=True)
    book_title = serializers.CharField(source='copy.book.title', read_only=True)
    copy_id = serializers.IntegerField(source='copy.id', read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            'id',
            'member_id',
            'member_name',
            'member_email',
            'copy_id',
            'book_title',
            'borrowed_at',
            'due_at',
            'returned_at',
            'status'
        ]
