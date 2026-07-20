from rest_framework import serializers
from .models import Author

class AuthorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']

    def validate_name(self, value):
        """
        Check: Trims extra spaces
        """
        cleaned_name = value.strip()
        if not cleaned_name:
            raise serializers.ValidationError("The author name cannot be empty.")
        return cleaned_name

class AuthorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'created_at', 'updated_at']
