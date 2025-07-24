#!/usr/bin/env python3
import os
import click
from flask import Flask
from app import create_app, db
import click

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.cli.command()
def init_db():
    """Initialize the database."""
    try:
        with app.app_context():
            # Import all models to ensure they are registered
            from app.models import User, Question, UserAnswer, DailyProgress
            
            # Create all tables
            db.create_all()
            print("✅ Database initialized successfully!")
            print("📋 Tables created:")
            
            # List created tables
            inspector = db.inspect(db.engine)
            for table in inspector.get_table_names():
                print(f"   - {table}")
                
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        raise

@app.cli.command()
def check_db():
    """Check database connection and list existing tables."""
    try:
        with app.app_context():
            # Test database connection
            with db.engine.connect() as connection:
                connection.execute(db.text("SELECT 1"))
            print("✅ Database connection successful!")
            
            # List existing tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print("📋 Existing tables:")
                for table in tables:
                    print(f"   - {table}")
            else:
                print("⚠️  No tables found. Run 'python run.py init-db' to create tables.")
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("💡 Check your database configuration and ensure the database server is running.")
        raise

@app.cli.command()
def seed_db():
    """Seed the database with sample data."""
    try:
        with app.app_context():
            from app.services.question_seeder import seed_sample_questions
            seed_sample_questions()
            print("✅ Database seeded successfully!")
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        print("💡 Make sure to run 'python run.py init-db' first")
        raise

@app.cli.command()
def seed_topics():
    """Seed topics from topics.json file."""
    try:
        with app.app_context():
            from app.services.topic_seeder import seed_topics_from_json
            success = seed_topics_from_json()
            if success:
                print("✅ Topics seeded successfully!")
            else:
                print("❌ Failed to seed topics")
    except Exception as e:
        print(f"❌ Error seeding topics: {e}")
        raise

@app.cli.command()
def create_admin():
    """Create an admin user."""
    try:
        with app.app_context():
            from app.services.topic_seeder import create_admin_user
            admin_user = create_admin_user(
                email="admin@mathopedia.com",
                password="admin123",
                first_name="Admin",
                last_name="User"
            )
            if admin_user:
                print(f"✅ Admin user created/updated: admin@mathopedia.com")
                print(f"📧 Email: admin@mathopedia.com")
                print(f"🔑 Password: admin123")
            else:
                print("❌ Failed to create admin user")
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        raise

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
