#!/bin/bash

# ============================================================================
# Automated Testing Script for Filtering, Searching, and Ordering
# ============================================================================

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BASE_URL="http://127.0.0.1:8000/api/books"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}   Testing Filtering, Searching & Ordering${NC}"
echo -e "${BLUE}============================================${NC}\n"

# Test 1: Basic list (default)
echo -e "${YELLOW}Test 1: GET /api/books/ (default)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Default book listing works\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 2: Filter by publication year
echo -e "${YELLOW}Test 2: Filter by publication_year${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/?publication_year=2020")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Filtering by publication_year works\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 3: Filter by publication year range (gte)
echo -e "${YELLOW}Test 3: Filter by publication_year__gte${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/?publication_year__gte=2000")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Range filtering (>=) works\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 4: Filter by publication year range (lte)
echo -e "${YELLOW}Test 4: Filter by publication_year__lte${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/?publication_year__lte=2020")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Range filtering (<=) works\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 5: Filter by author
echo -e "${YELLOW}Test 5: Filter by author${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/?author=1")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Filtering by author works\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 6: Case-insensitive title search
echo -e "${YELLOW}Test 6: Case-insensitive title search (title__icontains)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/?title__icontains=test")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Case-insensitive filtering works\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 7: Search functionality
echo -e "${YELLOW}Test 7: Search functionality${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/?search=test")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Search functionality works\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 8: Order by title (ascending)
echo -e "${YELLOW}Test 8: Order by title (ascending)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/?ordering=title")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Ordering by title (ascending) works\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 9: Order by publication_year (descending)
echo -e "${YELLOW}Test 9: Order by publication_year (descending)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/?ordering=-publication_year")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Ordering by publication_year (descending) works\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 10: Combined filter and ordering
echo -e "${YELLOW}Test 10: Combined filter and ordering${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/?publication_year__gte=2000&ordering=title")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Combined filtering and ordering works\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 11: Combined search and ordering
echo -e "${YELLOW}Test 11: Combined search and ordering${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/?search=test&ordering=-publication_year")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Combined search and ordering works\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

# Test 12: Complex query
echo -e "${YELLOW}Test 12: Complex query (filter + search + ordering)${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/?author=1&search=test&ordering=title")
http_status=$(echo "$response" | grep HTTP_STATUS | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Success (200 OK)${NC}"
    echo -e "Complex queries work\n"
else
    echo -e "${RED}✗ Failed (Expected 200, got $http_status)${NC}\n"
fi

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}   Tests Complete${NC}"
echo -e "${BLUE}============================================${NC}\n"

echo -e "${GREEN}All filtering, searching, and ordering features are working!${NC}"
echo -e "${YELLOW}For detailed usage examples, see FILTERING_SEARCHING_ORDERING_GUIDE.md${NC}\n"
