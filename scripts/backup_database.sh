#!/bin/bash

# Mathopedia Database Backup Script
# This script creates a backup of the MySQL database

set -e  # Exit on any error

# Configuration
DB_NAME="${MYSQL_DB:-mathopedia}"
DB_USER="${MYSQL_USER:-root}"
DB_PASSWORD="${MYSQL_PASSWORD:-}"
DB_HOST="${MYSQL_HOST:-localhost}"
DB_PORT="${MYSQL_PORT:-3306}"

# Backup directory
BACKUP_DIR="$(dirname "$0")/../backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/mathopedia_backup_${TIMESTAMP}.sql"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "🔄 Starting database backup..."
echo "Database: $DB_NAME"
echo "Host: $DB_HOST:$DB_PORT"
echo "Backup file: $BACKUP_FILE"

# Create the backup
if [ -n "$DB_PASSWORD" ]; then
    mysqldump -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" \
        --single-transaction \
        --routines \
        --triggers \
        --add-drop-table \
        --create-options \
        --quick \
        --lock-tables=false \
        "$DB_NAME" > "$BACKUP_FILE"
else
    mysqldump -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" \
        --single-transaction \
        --routines \
        --triggers \
        --add-drop-table \
        --create-options \
        --quick \
        --lock-tables=false \
        "$DB_NAME" > "$BACKUP_FILE"
fi

# Compress the backup
echo "🗜️  Compressing backup..."
gzip "$BACKUP_FILE"
COMPRESSED_BACKUP="${BACKUP_FILE}.gz"

# Get file size
BACKUP_SIZE=$(du -h "$COMPRESSED_BACKUP" | cut -f1)

echo "✅ Database backup completed successfully!"
echo "📁 Backup location: $COMPRESSED_BACKUP"
echo "📊 Backup size: $BACKUP_SIZE"

# Optional: Keep only last 7 backups to save space
echo "🧹 Cleaning up old backups (keeping last 7)..."
cd "$BACKUP_DIR"
ls -t mathopedia_backup_*.sql.gz | tail -n +8 | xargs -r rm --

echo "🎉 Backup process completed!"
