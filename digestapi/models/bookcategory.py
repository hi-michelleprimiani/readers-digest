from django.db import models


class BookCategory(models.Model):
    book = models.ForeignKey(
        "Book", on_delete=models.CASCADE, related_name='book_reference')
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name='category_reference')
    datetime = models.DateTimeField(auto_now_add=True)
