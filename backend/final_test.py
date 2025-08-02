#!/usr/bin/env python3
"""
Quick test to verify the Flask app works with our new parser
"""

import json
import sys
import os
sys.path.append(os.path.dirname(__file__))

# Import our modules to test
from parser import parse_expression, parse_vector, parse_limits
from calc3 import solve_multiple_integral

def test_integration():
    print("Testing end-to-end integration...")
    
    # Test 1: Simple double integral
    print("\n1. Testing double integral:")
    expression = "x*y"
    variables = ["x", "y"]
    limits = [("x", "0", "1"), ("y", "0", "1")]
    
    try:
        result = solve_multiple_integral(expression, limits)
        print(f"  ∫∫ x*y dx dy from 0 to 1 = {result}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test 2: LaTeX expression parsing
    print("\n2. Testing LaTeX expression parsing:")
    latex_expr = r"\sin(x) + \cos(y)"
    try:
        parsed = parse_expression(latex_expr)
        print(f"  '{latex_expr}' -> {parsed}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test 3: Vector parsing
    print("\n3. Testing vector parsing:")
    vector_str = "sin(t), cos(t), t"
    try:
        parsed_vector = parse_vector(vector_str)
        print(f"  '{vector_str}' -> {parsed_vector}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\nEnd-to-end tests completed!")

if __name__ == "__main__":
    test_integration()
