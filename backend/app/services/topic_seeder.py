import json
import os
from app import db
from app.models import Topic

def seed_topics_from_json():
    """Seed topics from topics.json file"""
    
    # Get the path to the topics.json file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path ="/Users/pranavikasanvi/code/Mathopedia/question-generator/topics.json"
    #json_file_path = os.path.join(current_dir, '..', '..', '..', 'question-generator', 'topics.json')
    
    try:
        print(f"📁 Looking for topics.json at: {json_file_path}")
        print(f"📄 File exists: {os.path.exists(json_file_path)}")
        
        with open(json_file_path, 'r') as file:
            topics_data = json.load(file)
        
        topics_created = 0
        topics_updated = 0
        
        for grade_key, grade_data in topics_data.items():
            # Extract grade level from key (e.g., "grade1" -> "1")
            grade_level = grade_key.replace('grade', '')
            
            for topic_data in grade_data['topics']:
                # Check if topic already exists
                existing_topic = Topic.query.filter_by(
                    topic=topic_data['name'],
                    grade_level=grade_level
                ).first()
                
                if existing_topic:
                    # Update existing topic
                    existing_topic.skill = topic_data['skill']
                    topics_updated += 1
                else:
                    # Create new topic
                    new_topic = Topic(
                        topic=topic_data['name'],
                        skill=topic_data['skill'],
                        grade_level=grade_level
                    )
                    db.session.add(new_topic)
                    topics_created += 1
        
        db.session.commit()
        print(f"✅ Topics seeded successfully!")
        print(f"📊 Created: {topics_created} topics")
        print(f"🔄 Updated: {topics_updated} topics")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: topics.json file not found at {json_file_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format in topics.json")
        print(f"📍 JSON Error details: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error seeding topics: {str(e)}")
        db.session.rollback()
        return False

def create_admin_user(email, password, first_name="Admin", last_name="User"):
    """Create an admin user"""
    from app.models import User
    
    # Check if admin user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        existing_user.is_admin = True
        db.session.commit()
        print(f"✅ Granted admin access to existing user: {email}")
        return existing_user
    
    # Create new admin user
    admin_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_admin=True
    )
    admin_user.set_password(password)
    
    try:
        db.session.add(admin_user)
        db.session.commit()
        print(f"✅ Admin user created successfully: {email}")
        return admin_user
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        db.session.rollback()
        return None
