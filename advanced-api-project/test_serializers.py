"""
Manual testing script for Author and Book serializers.

This script demonstrates how to:
1. Create Author and Book instances
2. Serialize single instances
3. Serialize querysets with nested relationships
4. Test custom validation

Run this script with: python manage.py shell < test_serializers.py
"""

from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer
from datetime import date
import json


def print_separator(title):
    """Print a formatted separator for better readability."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


# Test 1: Create Authors and Books
print_separator("TEST 1: Creating Authors and Books")

# Create authors
author1, created = Author.objects.get_or_create(name="J.K. Rowling")
author2, created = Author.objects.get_or_create(name="George R.R. Martin")

print(f"Created/Retrieved: {author1}")
print(f"Created/Retrieved: {author2}")

# Create books
book1, created = Book.objects.get_or_create(
    title="Harry Potter and the Philosopher's Stone",
    defaults={'publication_year': 1997, 'author': author1}
)
book2, created = Book.objects.get_or_create(
    title="Harry Potter and the Chamber of Secrets",
    defaults={'publication_year': 1998, 'author': author1}
)
book3, created = Book.objects.get_or_create(
    title="A Game of Thrones",
    defaults={'publication_year': 1996, 'author': author2}
)

print(f"Created/Retrieved: {book1}")
print(f"Created/Retrieved: {book2}")
print(f"Created/Retrieved: {book3}")


# Test 2: Serialize a single Book
print_separator("TEST 2: Serialize a Single Book")

serializer = BookSerializer(book1)
print("Book Serialized Data:")
print(json.dumps(serializer.data, indent=2))


# Test 3: Serialize an Author with nested Books
print_separator("TEST 3: Serialize Author with Nested Books")

serializer = AuthorSerializer(author1)
print("Author with Nested Books:")
print(json.dumps(serializer.data, indent=2))


# Test 4: Serialize all Authors with their Books
print_separator("TEST 4: Serialize All Authors with Nested Books")

authors = Author.objects.all()
serializer = AuthorSerializer(authors, many=True)
print("All Authors with Books:")
print(json.dumps(serializer.data, indent=2))


# Test 5: Test custom validation - Future year (should fail)
print_separator("TEST 5: Test Validation - Future Publication Year")

future_year = date.today().year + 1
invalid_data = {
    'title': 'Future Book',
    'publication_year': future_year,
    'author': author1.id
}

serializer = BookSerializer(data=invalid_data)
if serializer.is_valid():
    print("ERROR: Validation should have failed!")
else:
    print("✓ Validation correctly failed:")
    print(json.dumps(serializer.errors, indent=2))


# Test 6: Test custom validation - Old year (should fail)
print_separator("TEST 6: Test Validation - Too Old Publication Year")

invalid_data = {
    'title': 'Ancient Book',
    'publication_year': 500,
    'author': author1.id
}

serializer = BookSerializer(data=invalid_data)
if serializer.is_valid():
    print("ERROR: Validation should have failed!")
else:
    print("✓ Validation correctly failed:")
    print(json.dumps(serializer.errors, indent=2))


# Test 7: Test valid book creation
print_separator("TEST 7: Create Valid Book via Serializer")

valid_data = {
    'title': 'A New Book',
    'publication_year': 2020,
    'author': author1.id
}

serializer = BookSerializer(data=valid_data)
if serializer.is_valid():
    book = serializer.save()
    print("✓ Book created successfully:")
    print(json.dumps(serializer.data, indent=2))
else:
    print("ERROR: Valid data was rejected!")
    print(json.dumps(serializer.errors, indent=2))


print_separator("ALL TESTS COMPLETED")
print("Summary:")
print(f"  Total Authors: {Author.objects.count()}")
print(f"  Total Books: {Book.objects.count()}")
print("\nTo view in admin:")
print("  1. Create superuser: python manage.py createsuperuser")
print("  2. Run server: python manage.py runserver")
print("  3. Visit: http://127.0.0.1:8000/admin/")
