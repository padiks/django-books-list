# apps/books/models.py
from django.db import models
from apps.categories.models import Categories


class Books(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name="books"
    )
    published_date = models.DateField()
    title = models.CharField(max_length=255)
    hepburn = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    release = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    summary = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "books"
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title
