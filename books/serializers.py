from rest_framework import serializers
from .models import Book
from authors.models import Author

class BookCreateSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
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
            'author_id'
        ]

    def validate_published_year(self, value):
        """
        Custom validation to keep publish dates realistic
        """
        if value < 1000 or value > 2026:
            raise serializers.ValidationError("Published year must be valid historical year up to the present.")
        return value

class AuthorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class BookReadSerializer(serializers.ModelSerializer):
    author = AuthorInfoSerializer(read_only=True)

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
            'created_at',
            'updated_at'
        ]
