#!/usr/bin/env python3
"""
Manual script to fix the topics table grade_level column type migration
"""

from app import create_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

def fix_topics_migration():
    app = create_app()
    with app.app_context():
        from app import db
        
        try:
            print("Starting manual migration fix...")
            
            # Step 1: Check if grade_level_temp exists and has data
            result = db.session.execute(text("SELECT COUNT(*) as count FROM topics WHERE grade_level_temp IS NOT NULL"))
            temp_count = result.fetchone()[0]
            print(f"Found {temp_count} rows with grade_level_temp data")
            
            if temp_count == 0:
                # If grade_level_temp is empty, populate it
                print("Populating grade_level_temp from grade_level...")
                db.session.execute(text("UPDATE topics SET grade_level_temp = CAST(grade_level AS CHAR(50))"))
                db.session.commit()
            
            # Step 2: Drop constraints if they exist
            try:
                print("Dropping unique constraint...")
                db.session.execute(text("ALTER TABLE topics DROP INDEX unique_topic_grade"))
                db.session.commit()
            except Exception as e:
                print(f"Constraint drop failed (may not exist): {e}")
            
            # Step 3: Drop old grade_level column
            print("Dropping old grade_level column...")
            db.session.execute(text("ALTER TABLE topics DROP COLUMN grade_level"))
            db.session.commit()
            
            # Step 4: Rename temp column
            print("Renaming grade_level_temp to grade_level...")
            db.session.execute(text("ALTER TABLE topics CHANGE grade_level_temp grade_level VARCHAR(50) NOT NULL"))
            db.session.commit()
            
            # Step 5: Recreate unique constraint
            print("Recreating unique constraint...")
            db.session.execute(text("ALTER TABLE topics ADD CONSTRAINT unique_topic_grade UNIQUE (name, grade_level)"))
            db.session.commit()
            
            # Step 6: Mark migration as complete
            print("Marking migration as complete...")
            db.session.execute(text("UPDATE alembic_version SET version_num = '8c471b49145b'"))
            db.session.commit()
            
            print("Migration fix completed successfully!")
            
            # Verify the result
            result = db.session.execute(text('DESCRIBE topics'))
            print("\nFinal table structure:")
            for row in result:
                print(f"  {row}")
                
        except Exception as e:
            print(f"Error during migration fix: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    fix_topics_migration()
