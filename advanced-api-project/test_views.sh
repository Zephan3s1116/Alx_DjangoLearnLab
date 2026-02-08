#!/bin/bash

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BASE_URL="http://127.0.0.1:8000/api"

echo -e "${YELLOW}=== Testing API Endpoints ===${NC}\n"

# Test 1: List books (no auth)
echo -e "${YELLOW}Test 1: GET /api/books/ (No auth required)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" $BASE_URL/books/)
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200)${NC}\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 2: Get single book (no auth)
echo -e "${YELLOW}Test 2: GET /api/books/1/ (No auth required)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" $BASE_URL/books/1/)
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ] || [ "$http_status" == "404" ]; then
    echo -e "${GREEN}✓ Success ($http_status)${NC}\n"
else
    echo -e "${RED}✗ Failed (Expected 200 or 404, got $http_status)${NC}\n"
fi

# Test 3: Create book without auth (should fail)
echo -e "${YELLOW}Test 3: POST /api/books/create/ (No auth - should fail)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST $BASE_URL/books/create/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "publication_year": 2023, "author": 1}')
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "401" ]; then
    echo -e "${GREEN}✓ Correctly denied (401)${NC}\n"
else
    echo -e "${RED}✗ Failed (Expected 401, got $http_status)${NC}\n"
fi

echo -e "${YELLOW}=== Tests Complete ===${NC}"
echo -e "Note: To test authenticated endpoints, create a superuser and token first."
echo -e "Run: python manage.py createsuperuser"
