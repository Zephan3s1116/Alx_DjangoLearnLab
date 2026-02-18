# Production Deployment Checklist

## Critical Settings

### 1. DEBUG Setting
```python
# In production settings:
DEBUG = False
```

### 2. ALLOWED_HOSTS
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'your-app.herokuapp.com']
```

### 3. Database Configuration
```python
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://user:password@localhost:5432/dbname'
    )
}
```

### 4. Security Settings
```python
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 5. Static Files
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Run this command:
python manage.py collectstatic --noinput
```

## Before Deployment

- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up production database
- [ ] Configure security settings
- [ ] Collect static files
- [ ] Set SECRET_KEY from environment
- [ ] Test with production settings locally

## Environment Variables (.env)

```
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECURE_SSL_REDIRECT=True
```

## Deploy Commands

### Heroku
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
git push heroku master
heroku run python manage.py migrate
```

### Ubuntu Server
```bash
# Edit .env file
nano .env

# Collect static files
python manage.py collectstatic --noinput

# Migrate database
python manage.py migrate

# Restart services
sudo systemctl restart social_media_api
sudo systemctl restart nginx
```

## Verification

After deployment, verify:
- [ ] Site loads over HTTPS
- [ ] Admin interface works
- [ ] API endpoints respond correctly
- [ ] Static files load
- [ ] Database connections work
- [ ] No DEBUG information shown in errors

## Files to Review

1. `social_media_api/settings_production.py` - Production settings
2. `.env.example` - Environment template
3. `DEPLOYMENT_GUIDE.md` - Complete deployment guide
4. `requirements.txt` - Dependencies

## Quick Start

1. Copy settings_production.py content
2. Set environment variables
3. Collect static files
4. Run migrations
5. Deploy!
