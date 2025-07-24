#!/bin/bash

# Mathopedia Database Restore Script
# This script restores a MySQL database from a backup file

set -e  # Exit on any error

# Check if backup file is provided
if [ $# -eq 0 ]; then
    echo "❌ Usage: $0 <backup_file.sql.gz>"
    echo "Example: $0 ../backups/mathopedia_backup_20250723_143022.sql.gz"
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

# Configuration
DB_NAME="${MYSQL_DB:-mathopedia}"
DB_USER="${MYSQL_USER:-root}"
DB_PASSWORD="${MYSQL_PASSWORD:-}"
DB_HOST="${MYSQL_HOST:-localhost}"
DB_PORT="${MYSQL_PORT:-3306}"

echo "🔄 Starting database restore..."
echo "Database: $DB_NAME"
echo "Host: $DB_HOST:$DB_PORT"
echo "Backup file: $BACKUP_FILE"

# Create database if it doesn't exist
echo "📝 Creating database if it doesn't exist..."
if [ -n "$DB_PASSWORD" ]; then
    mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" \
        -e "CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
else
    mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" \
        -e "CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
fi

# Restore the database
echo "📥 Restoring database from backup..."
if [[ "$BACKUP_FILE" == *.gz ]]; then
    # Decompress and restore
    if [ -n "$DB_PASSWORD" ]; then
        gunzip -c "$BACKUP_FILE" | mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME"
    else
        gunzip -c "$BACKUP_FILE" | mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" "$DB_NAME"
    fi
else
    # Direct restore from .sql file
    if [ -n "$DB_PASSWORD" ]; then
        mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "$BACKUP_FILE"
    else
        mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" "$DB_NAME" < "$BACKUP_FILE"
    fi
fi

echo "✅ Database restore completed successfully!"
echo "🎉 Database '$DB_NAME' has been restored from $BACKUP_FILE"
