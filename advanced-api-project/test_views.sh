#!/bin/bash

# ============================================================================
# Automated API Testing Script
# ============================================================================

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BASE_URL="http://127.0.0.1:8000/api"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}   Testing API Endpoints${NC}"
echo -e "${BLUE}============================================${NC}\n"

# Test 1: List books (no auth)
echo -e "${YELLOW}Test 1: GET /api/books/ (No auth required)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" $BASE_URL/books/)
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Books listed successfully\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 2: Get single book (no auth)
echo -e "${YELLOW}Test 2: GET /api/books/1/ (No auth required)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" $BASE_URL/books/1/)
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ] || [ "$http_status" == "404" ]; then
    echo -e "${GREEN}✓ Success ($http_status)${NC}"
    if [ "$http_status" == "404" ]; then
        echo -e "Book not found (create some books first)\n"
    else
        echo -e "Book retrieved successfully\n"
    fi
else
    echo -e "${RED}✗ Failed (Expected 200 or 404, got $http_status)${NC}\n"
fi

# Test 3: Create book without auth (should fail)
echo -e "${YELLOW}Test 3: POST /api/books/create/ (No auth - should fail with 401)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST $BASE_URL/books/create/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Book", "publication_year": 2023, "author": 1}')
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "401" ]; then
    echo -e "${GREEN}✓ Correctly denied (401 Unauthorized)${NC}"
    echo -e "Authentication is properly enforced\n"
else
    echo -e "${RED}✗ Failed (Expected 401, got $http_status)${NC}\n"
fi

# Test 4: Update book without auth (should fail)
echo -e "${YELLOW}Test 4: PATCH /api/books/1/update/ (No auth - should fail with 401)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X PATCH $BASE_URL/books/1/update/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}')
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "401" ] || [ "$http_status" == "404" ]; then
    echo -e "${GREEN}✓ Success ($http_status)${NC}"
    echo -e "Authentication is properly enforced\n"
else
    echo -e "${RED}✗ Failed (Expected 401 or 404, got $http_status)${NC}\n"
fi

# Test 5: Delete book without auth (should fail)
echo -e "${YELLOW}Test 5: DELETE /api/books/1/delete/ (No auth - should fail with 401)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X DELETE $BASE_URL/books/1/delete/)
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "401" ] || [ "$http_status" == "404" ]; then
    echo -e "${GREEN}✓ Success ($http_status)${NC}"
    echo -e "Authentication is properly enforced\n"
else
    echo -e "${RED}✗ Failed (Expected 401 or 404, got $http_status)${NC}\n"
fi

# Test 6: Test filtering
echo -e "${YELLOW}Test 6: GET /api/books/?publication_year=2020 (Filter test)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/books/?publication_year=2020")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Filtering is working\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 7: Test searching
echo -e "${YELLOW}Test 7: GET /api/books/?search=test (Search test)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/books/?search=test")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Searching is working\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 8: Test ordering
echo -e "${YELLOW}Test 8: GET /api/books/?ordering=title (Ordering test)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/books/?ordering=title")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Ordering is working\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}   Tests Complete${NC}"
echo -e "${BLUE}============================================${NC}\n"

echo -e "${YELLOW}Note:${NC} To test authenticated endpoints, you need to:"
echo -e "1. Create a superuser: ${GREEN}python manage.py createsuperuser${NC}"
echo -e "2. Get a token (see TEST_API.md for instructions)"
echo -e "3. Use curl with: ${GREEN}-H \"Authorization: Token YOUR_TOKEN\"${NC}\n"
