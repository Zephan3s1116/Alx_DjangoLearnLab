# Social Media API - Deployment Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Production Deployment](#production-deployment)
4. [Heroku Deployment](#heroku-deployment)
5. [DigitalOcean/AWS Deployment](#digitaloceanaws-deployment)
6. [Environment Variables](#environment-variables)
7. [Database Setup](#database-setup)
8. [Static Files](#static-files)
9. [Monitoring & Maintenance](#monitoring--maintenance)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.11+
- PostgreSQL 13+ (production)
- Git
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)

---

## Local Development

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

---

## Production Deployment

### Step 1: Prepare Environment

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and PostgreSQL
sudo apt install python3-pip python3-venv postgresql nginx -y
```

### Step 2: Set Up PostgreSQL

```bash
# Create database and user
sudo -u postgres psql
CREATE DATABASE social_media_db;
CREATE USER social_media_user WITH PASSWORD 'your_password';
ALTER ROLE social_media_user SET client_encoding TO 'utf8';
ALTER ROLE social_media_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE social_media_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE social_media_db TO social_media_user;
\q
```

### Step 3: Clone and Configure

```bash
# Clone repository
cd /var/www
git clone https://github.com/YOUR_USERNAME/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Create .env file
nano .env
```

Add:
```
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://social_media_user:your_password@localhost:5432/social_media_db
SECURE_SSL_REDIRECT=True
```

### Step 5: Collect Static Files and Migrate

```bash
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
```

### Step 6: Configure Gunicorn

```bash
# Test Gunicorn
gunicorn --bind 0.0.0.0:8000 social_media_api.wsgi

# Create systemd service
sudo cp social_media_api.service /etc/systemd/system/
sudo systemctl start social_media_api
sudo systemctl enable social_media_api
```

### Step 7: Configure Nginx

```bash
# Copy nginx configuration
sudo cp nginx.conf.example /etc/nginx/sites-available/social_media_api
sudo ln -s /etc/nginx/sites-available/social_media_api /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### Step 8: Set Up SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Heroku Deployment

### 1. Install Heroku CLI

```bash
# Install Heroku CLI (if not installed)
curl https://cli-assets.heroku.com/install.sh | sh
```

### 2. Login to Heroku

```bash
heroku login
```

### 3. Create Heroku App

```bash
heroku create your-app-name
```

### 4. Add PostgreSQL

```bash
heroku addons:create heroku-postgresql:mini
```

### 5. Set Environment Variables

```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

### 6. Deploy

```bash
git push heroku master
```

### 7. Run Migrations

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### 8. Open App

```bash
heroku open
```

---

## DigitalOcean/AWS Deployment

### DigitalOcean Droplet Setup

1. **Create Droplet**
   - Choose Ubuntu 22.04 LTS
   - Select at least 1GB RAM
   - Add SSH key

2. **Access Droplet**
   ```bash
   ssh root@your-droplet-ip
   ```

3. **Follow Production Deployment steps** above

### AWS EC2 Setup

1. **Launch EC2 Instance**
   - Choose Ubuntu Server 22.04 LTS
   - Select t2.micro (or larger)
   - Configure security groups (ports 80, 443, 22)

2. **Connect to Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Follow Production Deployment steps** above

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Debug mode | `False` |
| `SECRET_KEY` | Django secret key | `your-random-key` |
| `ALLOWED_HOSTS` | Allowed hostnames | `yourdomain.com,www.yourdomain.com` |
| `DATABASE_URL` | Database connection | `postgresql://user:pass@host:5432/db` |
| `SECURE_SSL_REDIRECT` | Force HTTPS | `True` |

### Generating Secret Key

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## Database Setup

### PostgreSQL Production

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb social_media_db

# Create user
sudo -u postgres createuser social_media_user -P

# Grant privileges
sudo -u postgres psql
GRANT ALL PRIVILEGES ON DATABASE social_media_db TO social_media_user;
```

### Database Migrations

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### Database Backup

```bash
# Backup
pg_dump social_media_db > backup.sql

# Restore
psql social_media_db < backup.sql
```

---

## Static Files

### Configuration

```python
# settings_production.py
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Serve with WhiteNoise

WhiteNoise is already configured in `settings_production.py`.

### AWS S3 (Optional)

```bash
pip install django-storages boto3
```

Add to settings:
```python
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

---

## Monitoring & Maintenance

### Logging

Logs are configured in `settings_production.py`:
- Application errors: `django_errors.log`
- Nginx access: `/var/log/nginx/access.log`
- Nginx errors: `/var/log/nginx/error.log`
- Gunicorn logs: Use systemd journal

View Gunicorn logs:
```bash
sudo journalctl -u social_media_api -f
```

### Monitoring Tools

**Recommended:**
- Sentry (error tracking)
- New Relic (performance monitoring)
- Datadog (infrastructure monitoring)
- Uptime Robot (uptime monitoring)

### Regular Maintenance

**Daily:**
- Check error logs
- Monitor server resources

**Weekly:**
- Backup database
- Review and update dependencies

**Monthly:**
- Update packages
- Security audit
- Performance review

### Backup Script

```bash
# Run backup
./backup_db.sh

# Schedule with cron
crontab -e
# Add: 0 2 * * * /path/to/backup_db.sh
```

---

## Troubleshooting

### Common Issues

**Issue: 500 Internal Server Error**
```bash
# Check logs
sudo journalctl -u social_media_api -f
tail -f django_errors.log
```

**Issue: Static files not loading**
```bash
python manage.py collectstatic --noinput
sudo systemctl restart social_media_api
sudo systemctl restart nginx
```

**Issue: Database connection error**
```bash
# Check DATABASE_URL in .env
# Verify PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -h localhost -U social_media_user -d social_media_db
```

**Issue: Permission denied**
```bash
# Fix ownership
sudo chown -R www-data:www-data /path/to/social_media_api

# Fix permissions
chmod -R 755 /path/to/social_media_api
```

### Health Check Endpoint

Add to `urls.py`:
```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})

urlpatterns = [
    path('health/', health_check),
    # ...
]
```

---

## Security Checklist

- [ ] DEBUG = False
- [ ] Strong SECRET_KEY
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled
- [ ] SECURE_SSL_REDIRECT = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] Database password secure
- [ ] Firewall configured
- [ ] SSH key authentication only
- [ ] Regular backups
- [ ] Updated dependencies
- [ ] Error monitoring enabled

---

## Performance Optimization

### Database Optimization

```python
# Use select_related and prefetch_related
Post.objects.select_related('author').prefetch_related('comments')
```

### Caching

```bash
pip install django-redis
```

Add to settings:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### CDN for Static Files

Use CloudFlare, AWS CloudFront, or similar.

---

## Deployment Checklist

- [ ] Code tested locally
- [ ] All tests passing
- [ ] requirements.txt updated
- [ ] Environment variables set
- [ ] Database migrations created
- [ ] Static files collected
- [ ] SSL certificate installed
- [ ] Domain configured
- [ ] Monitoring set up
- [ ] Backups configured
- [ ] Documentation updated

---

## Support

For issues or questions:
- Check logs first
- Review this documentation
- Check Django documentation
- Contact: your-email@example.com

---

**Deployment Date:** {{ DATE }}  
**Version:** 1.0.0  
**Maintainer:** Your Name
