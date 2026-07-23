from rest_framework import serializers
from .models import Book, BookCopy
from authors.models import Author
from django.db import transaction

class BookCreateSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )

    copy_count = serializers.IntegerField(
        write_only=True,
        default=1,
        min_value=1,
        max_value=50
    )

    class Meta:
        model=Book
        fields = [
            'title',
            'isbn',
            'published_year',
            'language',
            'page_count',
            'tag',
            'author_id',
            'copy_count'
        ]

    def validate_published_year(self, value):
        """
        Custom validation to keep publish dates realistic
        """
        if value < 1000 or value > 2026:
            raise serializers.ValidationError("Published year must be valid historical year up to the present.")
        return value

    def create(self, validated_data):
        copy_count = validated_data.pop('copy_count', 1)

        with transaction.atomic():
            book = Book.objects.create(**validated_data)

            copies = [BookCopy(book=book, is_available=True) for _ in range(copy_count)]
            BookCopy.objects.bulk_create(copies)

        return book


class AuthorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class BookReadSerializer(serializers.ModelSerializer):
    author = AuthorInfoSerializer(read_only=True)

    total_copies = serializers.SerializerMethodField()
    available_copies = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'isbn',
            'published_year',
            'language',
            'page_count',
            'author',
            'total_copies',
            'available_copies',
            'created_at',
            'updated_at'
        ]

    def get_total_copies(self, obj):
        return obj.copies.count()

    def get_available_copies(self, obj):
        return obj.copies.filter(is_available=True).count()


class BookUpdateSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        required=False
    )

    class Meta:
        model = Book
        fields = [
            'title',
            'isbn',
            'published_year',
            'language',
            'page_count',
            'tag',
            'author_id'
        ]
        extra_kwargs = {
            'title': {'required': False},
            'isbn': {'required': False},
            'published_year': {'required': False},
            'language': {'required': False},
            'page_count': {'required': False},
            'tag': {'required': False},
        }

    def validate_published_year(self, value):
        if value is not None and (value < 1000 or value > 2026):
            raise serializers.ValidationError("Published year must be a valid historical year up to the present.")
            return value
