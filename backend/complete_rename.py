#!/usr/bin/env python3
"""
Manual script to complete the name -> topic column rename migration
"""

from app import create_app
from sqlalchemy import text

def complete_column_rename():
    app = create_app()
    with app.app_context():
        from app import db
        
        try:
            print("Completing the name -> topic column rename...")
            
            # Step 1: Copy data from name to topic (if not already done)
            result = db.session.execute(text("SELECT COUNT(*) as count FROM topics WHERE topic IS NULL"))
            null_count = result.fetchone()[0]
            print(f"Found {null_count} rows with NULL topic values")
            
            if null_count > 0:
                print("Copying data from name to topic...")
                db.session.execute(text("UPDATE topics SET topic = name WHERE topic IS NULL"))
                db.session.commit()
            
            # Step 2: Make topic column non-nullable
            print("Making topic column non-nullable...")
            db.session.execute(text("ALTER TABLE topics MODIFY topic VARCHAR(100) NOT NULL"))
            db.session.commit()
            
            # Step 3: Drop the old unique constraint if it exists
            try:
                print("Dropping old unique constraint...")
                db.session.execute(text("ALTER TABLE topics DROP INDEX unique_topic_grade"))
                db.session.commit()
            except Exception as e:
                print(f"Constraint drop failed (may not exist): {e}")
            
            # Step 4: Create new unique constraint on topic and grade_level
            print("Creating new unique constraint...")
            db.session.execute(text("ALTER TABLE topics ADD CONSTRAINT unique_topic_grade UNIQUE (topic, grade_level)"))
            db.session.commit()
            
            # Step 5: Drop the old name column
            print("Dropping old name column...")
            db.session.execute(text("ALTER TABLE topics DROP COLUMN name"))
            db.session.commit()
            
            # Step 6: Mark migration as complete
            print("Marking migration as complete...")
            db.session.execute(text("UPDATE alembic_version SET version_num = 'e21b3d6cd509'"))
            db.session.commit()
            
            print("Column rename completed successfully!")
            
            # Verify the result
            result = db.session.execute(text('DESCRIBE topics'))
            print("\nFinal table structure:")
            for row in result:
                print(f"  {row}")
                
            # Check some data
            result = db.session.execute(text('SELECT id, topic, grade_level FROM topics LIMIT 5'))
            print("\nSample topics:")
            for row in result:
                print(f"  ID: {row[0]}, Topic: {row[1]}, Grade: {row[2]}")
                
        except Exception as e:
            print(f"Error during column rename: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    complete_column_rename()
