#!/bin/bash

# Database backup script

BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="social_media_db"

mkdir -p $BACKUP_DIR

# Backup PostgreSQL database
pg_dump $DB_NAME > $BACKUP_DIR/backup_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete

echo "Database backed up to $BACKUP_DIR/backup_$DATE.sql"
