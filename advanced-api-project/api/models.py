from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    This model stores information about authors who have written books.
    It has a one-to-many relationship with the Book model, meaning one author
    can write multiple books.
    
    Fields:
        name (CharField): The full name of the author. Maximum length of 100 characters.
    
    Relationships:
        - One-to-Many with Book model (one author can have many books)
    
    String representation returns the author's name for easy identification
    in the Django admin and shell.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """Return the author's name as the string representation."""
        return self.name

    class Meta:
        """Meta options for the Author model."""
        ordering = ['name']  # Order authors alphabetically by name
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    """
    Book model representing a published book.
    
    This model stores information about books including their title, 
    publication year, and the author who wrote them.
    
    Fields:
        title (CharField): The title of the book. Maximum length of 200 characters.
        publication_year (IntegerField): The year the book was published.
        author (ForeignKey): A foreign key relationship to the Author model.
                           Uses CASCADE deletion (if author is deleted, their books are too).
                           Creates a reverse relationship accessible via 'books' on Author instances.
    
    Relationships:
        - Many-to-One with Author model (many books can belong to one author)
        - The related_name='books' allows accessing an author's books via author.books.all()
    
    String representation returns the book title for easy identification.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',  # Allows accessing books via author.books.all()
        help_text="The author who wrote this book"
    )

    def __str__(self):
        """Return the book title as the string representation."""
        return self.title

    class Meta:
        """Meta options for the Book model."""
        ordering = ['-publication_year', 'title']  # Order by year (newest first), then title
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        # Ensure no duplicate book titles by the same author
        unique_together = ['title', 'author']
