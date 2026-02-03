from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Book
from django.http import HttpResponseForbidden

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books.
    Requires 'can_view' permission.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book.
    Requires 'can_create' permission.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        isbn = request.POST.get('isbn')
        description = request.POST.get('description', '')
        
        book = Book.objects.create(
            title=title,
            author=author,
            publication_year=publication_year,
            isbn=isbn,
            description=description
        )
        messages.success(request, f'Book "{book.title}" created successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_form.html', {'action': 'Create'})


@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    View to edit an existing book.
    Requires 'can_edit' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        book.isbn = request.POST.get('isbn')
        book.description = request.POST.get('description', '')
        book.save()
        
        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_form.html', {'book': book, 'action': 'Edit'})


@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    View to delete a book.
    Requires 'can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})
