#!/usr/bin/env python3
"""
Simple test script to verify competitive exam questions functionality
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_competitive_questions():
    """Test competitive questions endpoint"""
    
    # First, we need to login to get a token
    # You'll need to replace these with actual test credentials
    login_data = {
        "email": "test@example.com",  # Replace with actual test user
        "password": "password123"     # Replace with actual test password
    }
    
    try:
        # Login
        print("Attempting to login...")
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.text}")
            print("Please make sure you have a test user created")
            return
        
        # Get the token
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test competitive questions endpoint
        print("\nTesting competitive questions endpoint...")
        response = requests.get(f"{BASE_URL}/questions/grade/competitive", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data['questions'])} competitive questions")
            
            if data['questions']:
                first_question = data['questions'][0]
                print(f"\nSample question:")
                print(f"Topic: {first_question.get('topic', 'N/A')}")
                print(f"Complexity: {first_question.get('complexity', 'N/A')}")
                print(f"Question: {first_question.get('question_text', 'N/A')[:100]}...")
            
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            
        # Test competitive stats endpoint
        print("\nTesting competitive stats endpoint...")
        stats_response = requests.get(f"{BASE_URL}/questions/stats/grade/competitive", headers=headers)
        
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print(f"✅ Stats Success!")
            print(f"Total competitive questions: {stats_data.get('total_questions', 0)}")
            print(f"Questions answered: {stats_data.get('answered_questions', 0)}")
            print(f"Remaining questions: {stats_data.get('remaining_questions', 0)}")
        else:
            print(f"❌ Stats Failed: {stats_response.status_code} - {stats_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the backend is running on localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_competitive_questions()
