# CRUD Operations Documentation

## Create
from bookshelf.models import Book
Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
# Output: <Book: 1984>

## Retrieve
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
# Output: 1984 George Orwell 1949

## Update
book.title = "Nineteen Eighty-Four"
book.save()
# Output: title updated to Nineteen Eighty-Four

# Delete Operation

**Command:**
```python
book.delete()
Book.objects.all()
(1, {'bookshelf.Book': 1})
<QuerySet []>