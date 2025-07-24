# Mathopedia Database Backup & Migration Guide

This guide explains how to backup your Mathopedia database and set up the system on another machine.

## 📋 Prerequisites

- MySQL installed on both source and target systems
- Access to MySQL database
- Bash shell (Linux/macOS) or Git Bash (Windows)

## 🗄️ Database Backup

### 1. Create a Backup

Use the automated backup script:

```bash
# Make script executable
chmod +x scripts/backup_database.sh

# Create backup with default settings
./scripts/backup_database.sh

# Or with custom environment variables
MYSQL_PASSWORD=your_password ./scripts/backup_database.sh
```

The backup will be saved in `backups/mathopedia_backup_TIMESTAMP.sql.gz`

### 2. Manual Backup (Alternative)

If you prefer manual backup:

```bash
# Create backup directory
mkdir -p backups

# Create backup
mysqldump -u root -p \
  --single-transaction \
  --routines \
  --triggers \
  --add-drop-table \
  mathopedia > backups/manual_backup.sql

# Compress backup
gzip backups/manual_backup.sql
```

### 3. Environment Variables for Backup

Set these environment variables if your database uses custom settings:

```bash
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DB=mathopedia
```

## 🚀 Setting Up on New System

### Option 1: Automated Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/achamakura001/mathopedia.git
   cd mathopedia
   ```

2. **Run the setup script:**
   ```bash
   chmod +x scripts/setup_system.sh
   ./scripts/setup_system.sh
   ```

3. **Restore your database backup:**
   ```bash
   chmod +x scripts/restore_database.sh
   ./scripts/restore_database.sh path/to/your/backup.sql.gz
   ```

### Option 2: Manual Setup

1. **Install Prerequisites:**
   - Python 3.8+
   - Node.js 16+
   - MySQL 8.0+

2. **Setup Backend:**
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Setup Environment:**
   ```bash
   # Create backend/.env file
   cp .env.example .env  # Edit with your database credentials
   ```

4. **Setup Database:**
   ```bash
   # Create database
   mysql -u root -p -e "CREATE DATABASE mathopedia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
   
   # Run migrations
   python -m flask db upgrade
   ```

5. **Restore Backup:**
   ```bash
   # Restore from backup
   gunzip -c /path/to/backup.sql.gz | mysql -u root -p mathopedia
   ```

6. **Setup Frontend:**
   ```bash
   cd ../frontend
   npm install
   ```

## 🔄 Database Restore

### Using the Restore Script

```bash
# Make script executable
chmod +x scripts/restore_database.sh

# Restore from compressed backup
./scripts/restore_database.sh backups/mathopedia_backup_20250723_143022.sql.gz

# Or with custom environment variables
MYSQL_PASSWORD=your_password ./scripts/restore_database.sh backup.sql.gz
```

### Manual Restore

```bash
# For compressed backup
gunzip -c backup.sql.gz | mysql -u root -p mathopedia

# For uncompressed backup
mysql -u root -p mathopedia < backup.sql
```

## 🔧 Configuration

### Environment Variables

Create `backend/.env` with these settings:

```env
# Database
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=mathopedia

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Optional: LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

### Database Connection Test

Test your database connection:

```bash
cd backend
source .venv/bin/activate
python -c "
from app import create_app
app = create_app()
with app.app_context():
    from app import db
    db.create_all()
    print('✅ Database connection successful!')
"
```

## 🚀 Running the Application

1. **Start Backend:**
   ```bash
   cd backend
   source .venv/bin/activate
   python run.py
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm start
   ```

3. **Access Application:**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:5000/api/v2/docs/

## 📊 Backup Schedule

For production systems, consider setting up automated backups:

```bash
# Add to crontab for daily backups at 2 AM
0 2 * * * /path/to/mathopedia/scripts/backup_database.sh
```

## 🛠️ Troubleshooting

### Common Issues

1. **MySQL Connection Error:**
   - Check if MySQL service is running
   - Verify credentials in `.env` file
   - Ensure database exists

2. **Permission Denied:**
   - Make scripts executable: `chmod +x scripts/*.sh`
   - Check file ownership and permissions

3. **Import Errors:**
   - Ensure virtual environment is activated
   - Check if all dependencies are installed

4. **Frontend Issues:**
   - Clear npm cache: `npm cache clean --force`
   - Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

### Getting Help

If you encounter issues:
1. Check the logs in `backend/logs/` (if configured)
2. Verify environment variables are set correctly
3. Ensure all services (MySQL) are running
4. Check firewall settings for database connections

## 📁 File Structure

```
mathopedia/
├── scripts/
│   ├── backup_database.sh      # Database backup script
│   ├── restore_database.sh     # Database restore script
│   └── setup_system.sh         # System setup script
├── backups/                    # Backup files (created automatically)
├── backend/
│   ├── .env                    # Environment configuration
│   ├── requirements.txt        # Python dependencies
│   └── ...
└── frontend/
    ├── package.json           # Node.js dependencies
    └── ...
```
