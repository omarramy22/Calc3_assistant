#!/usr/bin/env python3
"""
Test Flask app startup and basic endpoint
"""

import requests
import json
import time
import subprocess
import sys

def test_flask_app():
    print("Testing Flask app functionality...")
    
    # Test data for double integral
    test_data = {
        "operation": "double_integral",
        "function": "x*y",
        "variables": "x,y", 
        "limits": "0,1,0,1"
    }
    
    try:
        # Try to make a request (assuming server is running)
        response = requests.post('http://localhost:5000/calculate', 
                               json=test_data, 
                               timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Double integral test successful: {result}")
        else:
            print(f"❌ Request failed with status {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask server. Is it running on port 5000?")
    except Exception as e:
        print(f"❌ Request error: {e}")
    
    # Test LaTeX parsing
    latex_test_data = {
        "operation": "gradient", 
        "function": r"\sin(x) + \cos(y)",
        "variables": "x,y"
    }
    
    try:
        response = requests.post('http://localhost:5000/calculate',
                               json=latex_test_data,
                               timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ LaTeX gradient test successful: {result}")
        else:
            print(f"❌ LaTeX test failed with status {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask server for LaTeX test.")
    except Exception as e:
        print(f"❌ LaTeX test error: {e}")

if __name__ == "__main__":
    print("To run this test:")
    print("1. Start the Flask server: python app.py")
    print("2. In another terminal, run: python test_flask.py")
    print("")
    test_flask_app()
