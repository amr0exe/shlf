from django.db import models
from authors.models import Author

# Defines individual Book as an entity.
class Book(models.Model):
    class TagChoices(models.TextChoices):
        FICTION = 'fiction', 'Fiction'
        NON_FICTION = 'non-fiction', 'Non-Fiction'
        SCI_FI = 'sci-fi', 'Sci-Fi'
        BIOGRAPHY = 'biography', 'Biography'
        HISTORY = 'history', 'History'
        MYSTERY = 'mystery', 'Mystery'

    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    published_year = models.IntegerField()
    language = models.CharField(max_length=50, default='English')
    page_count = models.IntegerField()

    tag = models.CharField(
        max_length=20,
        choices=TagChoices.choices
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        related_name="books"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

# Helps in tracking individual book_copies
class BookCopy(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="copies"
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"(Copy ID: {self.pk})"
