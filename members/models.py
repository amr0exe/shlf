from django.db import models

# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
