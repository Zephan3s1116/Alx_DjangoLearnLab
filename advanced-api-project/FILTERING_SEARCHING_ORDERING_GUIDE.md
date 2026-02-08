# Filtering, Searching, and Ordering Guide

## Overview
This guide demonstrates how to use the advanced query capabilities (filtering, searching, and ordering) implemented in the Book API.

---

## Table of Contents
1. [Filtering](#filtering)
2. [Searching](#searching)
3. [Ordering](#ordering)
4. [Combining Features](#combining-features)
5. [Testing Examples](#testing-examples)

---

## Filtering

Filtering allows you to retrieve only books that match specific criteria.

### Available Filters

#### 1. Exact Match Filters

**Filter by Title (exact match):**
```bash
GET /api/books/?title=Harry Potter and the Sorcerer's Stone
```
```bash
curl "http://127.0.0.1:8000/api/books/?title=Harry%20Potter%20and%20the%20Sorcerer's%20Stone"
```

**Filter by Author ID:**
```bash
GET /api/books/?author=1
```
```bash
curl "http://127.0.0.1:8000/api/books/?author=1"
```

**Filter by Publication Year:**
```bash
GET /api/books/?publication_year=2020
```
```bash
curl "http://127.0.0.1:8000/api/books/?publication_year=2020"
```

#### 2. Range Filters

**Books published in or after a specific year:**
```bash
GET /api/books/?publication_year__gte=2000
```
```bash
curl "http://127.0.0.1:8000/api/books/?publication_year__gte=2000"
```

**Books published in or before a specific year:**
```bash
GET /api/books/?publication_year__lte=2020
```
```bash
curl "http://127.0.0.1:8000/api/books/?publication_year__lte=2020"
```

**Books published in a specific range:**
```bash
GET /api/books/?publication_year__gte=2000&publication_year__lte=2020
```
```bash
curl "http://127.0.0.1:8000/api/books/?publication_year__gte=2000&publication_year__lte=2020"
```

#### 3. Case-Insensitive Contains Filter

**Find books with titles containing a specific word (case-insensitive):**
```bash
GET /api/books/?title__icontains=harry
```
```bash
curl "http://127.0.0.1:8000/api/books/?title__icontains=harry"
```

This will match:
- "Harry Potter and the Sorcerer's Stone"
- "The World of Harry Potter"
- "harry's adventure"

---

## Searching

Searching allows you to search across multiple fields simultaneously.

### Search Fields
- `title`: Book title
- `author__name`: Author's name

### Search Examples

**Search for books with "Harry" in title or author name:**
```bash
GET /api/books/?search=Harry
```
```bash
curl "http://127.0.0.1:8000/api/books/?search=Harry"
```

**Search for books related to "Rowling":**
```bash
GET /api/books/?search=Rowling
```
```bash
curl "http://127.0.0.1:8000/api/books/?search=Rowling"
```

**Search for "Potter":**
```bash
GET /api/books/?search=Potter
```
```bash
curl "http://127.0.0.1:8000/api/books/?search=Potter"
```

### How Search Works
- Searches across both `title` and `author__name` fields
- Case-insensitive
- Partial matches are included
- Returns books that match the search term in ANY of the search fields

---

## Ordering

Ordering allows you to sort the results by any field.

### Available Ordering Fields
- `title`: Sort by book title
- `publication_year`: Sort by publication year
- `author`: Sort by author ID

### Ordering Examples

**Sort by title (ascending A-Z):**
```bash
GET /api/books/?ordering=title
```
```bash
curl "http://127.0.0.1:8000/api/books/?ordering=title"
```

**Sort by title (descending Z-A):**
```bash
GET /api/books/?ordering=-title
```
```bash
curl "http://127.0.0.1:8000/api/books/?ordering=-title"
```

**Sort by publication year (oldest first):**
```bash
GET /api/books/?ordering=publication_year
```
```bash
curl "http://127.0.0.1:8000/api/books/?ordering=publication_year"
```

**Sort by publication year (newest first):**
```bash
GET /api/books/?ordering=-publication_year
```
```bash
curl "http://127.0.0.1:8000/api/books/?ordering=-publication_year"
```

**Sort by multiple fields:**
```bash
GET /api/books/?ordering=author,title
```
```bash
curl "http://127.0.0.1:8000/api/books/?ordering=author,title"
```

### Ordering Syntax
- **Ascending:** Use field name directly (e.g., `ordering=title`)
- **Descending:** Prefix with `-` (e.g., `ordering=-title`)
- **Multiple fields:** Separate with commas (e.g., `ordering=author,title`)

---

## Combining Features

You can combine filtering, searching, and ordering in a single request.

### Combination Examples

**Example 1: Filter by year range and sort by title**
```bash
GET /api/books/?publication_year__gte=2000&publication_year__lte=2020&ordering=title
```
```bash
curl "http://127.0.0.1:8000/api/books/?publication_year__gte=2000&publication_year__lte=2020&ordering=title"
```

**Example 2: Search and sort**
```bash
GET /api/books/?search=Harry&ordering=-publication_year
```
```bash
curl "http://127.0.0.1:8000/api/books/?search=Harry&ordering=-publication_year"
```

**Example 3: Filter by author and sort**
```bash
GET /api/books/?author=1&ordering=-publication_year
```
```bash
curl "http://127.0.0.1:8000/api/books/?author=1&ordering=-publication_year"
```

**Example 4: Complex query with all features**
```bash
GET /api/books/?author=1&publication_year__gte=2000&search=Potter&ordering=title
```
```bash
curl "http://127.0.0.1:8000/api/books/?author=1&publication_year__gte=2000&search=Potter&ordering=title"
```

**Example 5: Case-insensitive title search with ordering**
```bash
GET /api/books/?title__icontains=harry&ordering=-publication_year
```
```bash
curl "http://127.0.0.1:8000/api/books/?title__icontains=harry&ordering=-publication_year"
```

---

## Testing Examples

### Using curl

#### Test 1: List all books (default ordering)
```bash
curl http://127.0.0.1:8000/api/books/
```

#### Test 2: Filter by publication year
```bash
curl "http://127.0.0.1:8000/api/books/?publication_year=2020"
```

#### Test 3: Search for books
```bash
curl "http://127.0.0.1:8000/api/books/?search=Harry"
```

#### Test 4: Sort by title
```bash
curl "http://127.0.0.1:8000/api/books/?ordering=title"
```

#### Test 5: Complex query
```bash
curl "http://127.0.0.1:8000/api/books/?publication_year__gte=2000&ordering=-publication_year&search=Potter"
```

### Using Postman

#### Setup
1. Open Postman
2. Create a new request
3. Set method to GET
4. Base URL: `http://127.0.0.1:8000/api/books/`

#### Test Scenarios

**Scenario 1: Basic Filtering**
- URL: `http://127.0.0.1:8000/api/books/`
- Params:
  - Key: `publication_year`, Value: `2020`
- Expected: Books published in 2020

**Scenario 2: Range Filtering**
- URL: `http://127.0.0.1:8000/api/books/`
- Params:
  - Key: `publication_year__gte`, Value: `2000`
  - Key: `publication_year__lte`, Value: `2020`
- Expected: Books published between 2000 and 2020

**Scenario 3: Search**
- URL: `http://127.0.0.1:8000/api/books/`
- Params:
  - Key: `search`, Value: `Harry`
- Expected: Books with "Harry" in title or author name

**Scenario 4: Ordering**
- URL: `http://127.0.0.1:8000/api/books/`
- Params:
  - Key: `ordering`, Value: `-publication_year`
- Expected: Books sorted by publication year (newest first)

**Scenario 5: Combined**
- URL: `http://127.0.0.1:8000/api/books/`
- Params:
  - Key: `author`, Value: `1`
  - Key: `publication_year__gte`, Value: `2000`
  - Key: `ordering`, Value: `title`
- Expected: Books by author 1, published from 2000 onwards, sorted by title

---

## Query Parameter Reference

### Filtering Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `title` | string | Exact title match | `?title=Harry Potter` |
| `author` | integer | Filter by author ID | `?author=1` |
| `publication_year` | integer | Exact year match | `?publication_year=2020` |
| `publication_year__gte` | integer | Year greater than or equal | `?publication_year__gte=2000` |
| `publication_year__lte` | integer | Year less than or equal | `?publication_year__lte=2020` |
| `title__icontains` | string | Case-insensitive title search | `?title__icontains=harry` |

### Searching Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search` | string | Search across title and author name | `?search=Harry` |

### Ordering Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `ordering` | string | Sort by field (prefix with `-` for descending) | `?ordering=title` |
|  |  |  | `?ordering=-publication_year` |
|  |  |  | `?ordering=author,title` |

### Pagination Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `page` | integer | Page number | `?page=2` |

---

## Expected Response Format

All successful queries return a paginated response:

```json
{
    "count": 25,
    "next": "http://127.0.0.1:8000/api/books/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Harry Potter and the Sorcerer's Stone",
            "publication_year": 1997,
            "author": 1
        },
        {
            "id": 2,
            "title": "Harry Potter and the Chamber of Secrets",
            "publication_year": 1998,
            "author": 1
        }
    ]
}
```

---

## Error Responses

### Invalid Filter Value
```json
{
    "detail": "Invalid filter value."
}
```

### Invalid Ordering Field
```json
{
    "detail": "Invalid ordering field."
}
```

---

## Tips and Best Practices

1. **URL Encoding**: Remember to URL-encode special characters in queries
   - Space: `%20`
   - `&`: `%26`
   - Example: `Harry Potter` → `Harry%20Potter`

2. **Combining Filters**: You can use multiple filters together
   - They work as AND conditions
   - Example: `?author=1&publication_year=2020` means "Books by author 1 AND published in 2020"

3. **Search vs Filter**: 
   - Use **search** for fuzzy, multi-field queries
   - Use **filters** for exact matches

4. **Performance**: 
   - Filtering by indexed fields (like `id`, `author`) is faster
   - Ordering large result sets may impact performance

5. **Pagination**: 
   - Results are paginated (10 per page by default)
   - Use `?page=N` to navigate pages

---

## Troubleshooting

### Issue: No results returned
- **Check**: Are your filter values correct?
- **Try**: Remove filters one by one to identify the issue

### Issue: Ordering not working
- **Check**: Is the field name spelled correctly?
- **Try**: Use valid ordering fields: `title`, `publication_year`, `author`

### Issue: Search returning too many results
- **Solution**: Combine search with filters
- **Example**: `?search=Harry&author=1`

---

## Additional Resources

- Django Filter Documentation: https://django-filter.readthedocs.io/
- DRF Filtering Guide: https://www.django-rest-framework.org/api-guide/filtering/
- DRF SearchFilter: https://www.django-rest-framework.org/api-guide/filtering/#searchfilter
- DRF OrderingFilter: https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter
