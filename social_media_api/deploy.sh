#!/bin/bash

# Deployment script for Social Media API

echo "Starting deployment..."

# Pull latest code
git pull origin master

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Restart Gunicorn
sudo systemctl restart social_media_api

echo "Deployment complete!"
