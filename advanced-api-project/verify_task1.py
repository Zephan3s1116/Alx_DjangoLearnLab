"""
Verification script for Task 1 implementation.
Checks that all required components are properly configured.
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {filepath}")
        return False

def check_file_contains(filepath, search_strings, description):
    """Check if file contains all required strings."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        all_found = True
        for search_str in search_strings:
            if search_str in content:
                print(f"  ✅ Contains: {search_str}")
            else:
                print(f"  ❌ Missing: {search_str}")
                all_found = False
        
        if all_found:
            print(f"✅ {description}")
        return all_found
    except Exception as e:
        print(f"❌ Error checking {filepath}: {e}")
        return False

print("=" * 60)
print("Task 1 Verification")
print("=" * 60)
print()

# Check files exist
print("1. Checking required files exist...")
print("-" * 60)
files_ok = True
files_ok &= check_file_exists('api/views.py', 'Views file')
files_ok &= check_file_exists('api/urls.py', 'API URLs file')
files_ok &= check_file_exists('advanced_api_project/urls.py', 'Main URLs file')
files_ok &= check_file_exists('requirements.txt', 'Requirements file')
print()

# Check views.py
print("2. Checking api/views.py...")
print("-" * 60)
views_checks = [
    'BookListView',
    'BookDetailView',
    'BookCreateView',
    'BookUpdateView',
    'BookDeleteView',
    'IsAuthenticatedOrReadOnly',
    'IsAuthenticated',
    'generics.ListAPIView',
    'generics.RetrieveAPIView',
    'generics.CreateAPIView',
    'generics.UpdateAPIView',
    'generics.DestroyAPIView',
]
views_ok = check_file_contains('api/views.py', views_checks, 'Views properly configured')
print()

# Check api/urls.py
print("3. Checking api/urls.py...")
print("-" * 60)
api_urls_checks = [
    'books/',
    'books/<int:pk>/',
    'books/create/',
    'books/<int:pk>/update/',
    'books/update/',
    'books/<int:pk>/delete/',
    'books/delete/',
    'BookListView',
    'BookDetailView',
    'BookCreateView',
    'BookUpdateView',
    'BookDeleteView',
]
api_urls_ok = check_file_contains('api/urls.py', api_urls_checks, 'API URLs properly configured')
print()

# Check main urls.py
print("4. Checking advanced_api_project/urls.py...")
print("-" * 60)
main_urls_checks = [
    "path('api/', include('api.urls'))",
]
main_urls_ok = check_file_contains('advanced_api_project/urls.py', main_urls_checks, 'Main URLs properly configured')
print()

# Check requirements.txt
print("5. Checking requirements.txt...")
print("-" * 60)
requirements_checks = [
    'Django',
    'djangorestframework',
    'django-filter',
]
requirements_ok = check_file_contains('requirements.txt', requirements_checks, 'Requirements properly specified')
print()

# Summary
print("=" * 60)
print("VERIFICATION SUMMARY")
print("=" * 60)
all_ok = files_ok and views_ok and api_urls_ok and main_urls_ok and requirements_ok
if all_ok:
    print("✅ ALL CHECKS PASSED!")
    print("Task 1 is properly configured.")
else:
    print("❌ SOME CHECKS FAILED")
    print("Please review the errors above and fix them.")
    sys.exit(1)
