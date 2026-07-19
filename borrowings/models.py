from django.db import models
from members.models import Member
from books.models import BookCopy

# Create your models here.
class Borrowing(models.Model):
    class BorrowStatus(models.TextChoices):
        BORROWED = 'borrowed', 'Borrowed'
        RETURNED = 'returned', 'Returned'
        OVERDUE = 'overdue', "Overdue"
        LOST = 'lost', 'Lost'

    member = models.ForeignKey(
        Member,
        on_delete=models.RESTRICT,
        related_name="borrowings"
    )
    copy = models.ForeignKey(
        BookCopy,
        on_delete=models.RESTRICT,
        related_name="borrowings"
    )

    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=15,
        choices=BorrowStatus.choices,
        default=BorrowStatus.BORROWED
    )

    def __str__(self):
        return f"Borrow {self.pk}: {self.member.name} -> {self.copy.book.title}"


class Fine(models.Model):
    borrowing = models.ForeignKey(
        Borrowing,
        on_delete=models.CASCADE,
        related_name="fines"
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fine {self.amount}"
