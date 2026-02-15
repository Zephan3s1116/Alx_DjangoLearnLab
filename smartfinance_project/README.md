# SmartFinance API - Capstone Project

## Week 1 Progress (Part 3)

### ✅ Completed This Week:

1. **Project Setup**
   - Created Django project structure
   - Set up 6 Django apps: users, transactions, categories, budgets, goals, analytics
   - Configured Django REST Framework
   - Set up authentication system

2. **User Management**
   - ✅ UserProfile model (extends Django User)
   - ✅ User registration endpoint
   - ✅ User login endpoint (token authentication)
   - ✅ User profile endpoint (view/update)

### 📊 Current Status:

**Working Features:**
- User registration with email and password
- Token-based authentication
- User profile management
- Extended profile with phone, DOB, currency preference

**API Endpoints (Live):**
- POST `/api/auth/register/` - Register new user
- POST `/api/auth/login/` - Login and get token
- GET/PUT `/api/auth/profile/` - View/update profile

### 🎯 Next Week Goals (Week 2):

1. **Category Management**
   - Create Category model
   - Implement CRUD for categories
   - Load default categories

2. **Transaction Management**
   - Create Transaction model
   - Implement CRUD for transactions
   - Add filtering and search

3. **Testing**
   - Write unit tests for users app
   - Test all authentication flows

### 🚧 Challenges Faced:

1. **Challenge:** Setting up the project structure
   **Solution:** Followed Django best practices, separated concerns into multiple apps

2. **Challenge:** Implementing token authentication
   **Solution:** Used DRF's built-in TokenAuthentication

### 📝 Commit History:

- Initial project setup
- Add user registration and authentication
- Create UserProfile model
- Configure REST Framework settings

### 🔧 Tech Stack:

- Django 4.2+
- Django REST Framework 3.14+
- SQLite (development)
- Token Authentication

### 📚 How to Run:
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### 🧪 Testing:
```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# Get profile (with token)
curl http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Project Timeline:

- **Week 1 (Current):** ✅ User Management & Authentication
- **Week 2:** Categories & Transactions
- **Week 3:** Budgets & Goals
- **Week 4:** Analytics & Testing
- **Week 5:** Deployment & Final Polish

---

**Last Updated:** February 9, 2026
**Repository:** https://github.com/Zephan3s1116/Alx_DjangoLearnLab/tree/master/smartfinance_project
