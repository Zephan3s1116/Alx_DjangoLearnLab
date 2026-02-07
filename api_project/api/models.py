from django.db import models

class Book(models.Model):
    """
    Simple Book model for API demonstration.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title
