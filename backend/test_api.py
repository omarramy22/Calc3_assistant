#!/usr/bin/env python3

import requests
import json

# Test the Flask API with the fixed expression
url = "http://localhost:5000/solve_partial_derivative"

data = {
    "expr": "x^2\\cdot y+y\\sin\\left(xy\\right)",
    "variables": ["x"],
    "order": 1
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except requests.exceptions.ConnectionError:
    print("Flask server is not running. Let me start it...")
    print("Please run: python app.py")
except Exception as e:
    print(f"Error: {e}")
