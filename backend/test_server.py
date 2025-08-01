#!/usr/bin/env python3
"""
CALCULATOR TEST SERVER
======================
Starts the Flask server for frontend testing.

Usage: python test_server.py
Then open: http://localhost:5000
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("="*60)
    print("🚀 STARTING CALCULATOR TEST SERVER")
    print("="*60)
    print("📍 Server will run at: http://localhost:5000")
    print("🧮 Test all calculator functions in your browser")
    print("🔧 Press Ctrl+C to stop the server")
    print("="*60)
    print()
    
    try:
        app.run(debug=True, port=5000, host='127.0.0.1')
    except KeyboardInterrupt:
        print("\n✅ Server stopped gracefully")
    except Exception as e:
        print(f"❌ Server error: {e}")
