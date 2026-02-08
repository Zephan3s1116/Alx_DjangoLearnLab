from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Author model.
    
    Provides an enhanced admin interface for managing authors with:
    - List display showing id and name
    - Search functionality by author name
    - Filtering options
    """
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Book model.
    
    Provides an enhanced admin interface for managing books with:
    - List display showing all key fields
    - Filtering by author and publication year
    - Search functionality
    - Organized fieldsets for better UX
    """
    list_display = ['id', 'title', 'author', 'publication_year']
    list_filter = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering = ['-publication_year', 'title']
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'publication_year')
        }),
        ('Author Information', {
            'fields': ('author',)
        }),
    )
