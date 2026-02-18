# Quick Deployment Reference

## Heroku (Fastest)

```bash
# 1. Create app
heroku create your-app-name

# 2. Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# 3. Set env vars
heroku config:set SECRET_KEY=your-key DEBUG=False

# 4. Deploy
git push heroku master

# 5. Migrate
heroku run python manage.py migrate
heroku run python manage.py createsuperuser

# 6. Open
heroku open
```

## Ubuntu Server (Full Control)

```bash
# 1. Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv postgresql nginx -y

# 2. Set up PostgreSQL
sudo -u postgres createdb social_media_db
sudo -u postgres createuser social_media_user -P

# 3. Clone and configure
git clone <repo-url>
cd social_media_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configure .env
cp .env.example .env
nano .env

# 5. Migrate and collect static
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# 6. Set up Gunicorn service
sudo cp social_media_api.service /etc/systemd/system/
sudo systemctl start social_media_api
sudo systemctl enable social_media_api

# 7. Configure Nginx
sudo cp nginx.conf.example /etc/nginx/sites-available/social_media_api
sudo ln -s /etc/nginx/sites-available/social_media_api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 8. SSL with Let's Encrypt
sudo certbot --nginx -d yourdomain.com
```

## Environment Variables

```
DEBUG=False
SECRET_KEY=<generate-with-django>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
SECURE_SSL_REDIRECT=True
```

## Useful Commands

```bash
# Restart services
sudo systemctl restart social_media_api
sudo systemctl restart nginx

# View logs
sudo journalctl -u social_media_api -f
tail -f django_errors.log

# Deploy updates
./deploy.sh

# Backup database
./backup_db.sh
```
