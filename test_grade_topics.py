#!/usr/bin/env python3
"""
Test script to verify the grade-wise topic performance functionality
"""

import requests
import json

# Test configuration
BASE_URL = "http://127.0.0.1:5000/api"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword"

def login_user():
    """Login and get JWT token"""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    })
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return None

def test_profile_grade_performance(token):
    """Test the grade-wise performance in profile"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    
    if response.status_code == 200:
        profile_data = response.json()
        grade_performance = profile_data.get("grade_performance", [])
        
        print("=== Grade-wise Performance ===")
        for grade in grade_performance:
            print(f"Grade: {grade['grade_display']} (Level: {grade['grade_level']})")
            print(f"  Questions: {grade['total_questions']}")
            print(f"  Correct: {grade['correct_answers']}")
            print(f"  Accuracy: {grade['accuracy']}%")
            print()
        
        return grade_performance
    else:
        print(f"Profile request failed: {response.status_code}")
        print(response.text)
        return []

def test_grade_topic_breakdown(token, grade_level):
    """Test the topic-wise breakdown for a specific grade"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/profile/grade/{grade_level}/topics", headers=headers)
    
    if response.status_code == 200:
        topic_data = response.json()
        
        print(f"=== Topic Performance for {topic_data['grade_display']} ===")
        print(f"Total Topics: {topic_data['total_topics']}")
        print(f"Topics Attempted: {topic_data['topics_attempted']}")
        print()
        
        for topic in topic_data['topic_performance']:
            print(f"Topic: {topic['topic_name']}")
            print(f"  Skill: {topic['skill']}")
            print(f"  Questions: {topic['total_questions']}")
            print(f"  Correct: {topic['correct_answers']}")
            print(f"  Accuracy: {topic['accuracy']}%")
            print()
        
        return topic_data
    else:
        print(f"Topic breakdown request failed: {response.status_code}")
        print(response.text)
        return None

def main():
    """Main test function"""
    print("Testing Grade-wise Performance Functionality")
    print("=" * 50)
    
    # Login
    token = login_user()
    if not token:
        print("Cannot proceed without authentication")
        return
    
    # Test profile grade performance
    grade_performance = test_profile_grade_performance(token)
    
    # Test topic breakdown for first available grade
    if grade_performance:
        first_grade = grade_performance[0]['grade_level']
        test_grade_topic_breakdown(token, first_grade)
    
    print("Test completed!")

if __name__ == "__main__":
    main()
