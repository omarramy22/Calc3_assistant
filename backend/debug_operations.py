#!/usr/bin/env python3
"""
Debug specific operations that might not be working
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from parser import parse_expression, parse_vector, parse_limits, parse_integral_limits
from calc3 import solve_multiple_integral, solve_gradient, solve_divergence

def test_operations():
    print("Testing specific operations...")
    
    # Test 1: Double integral
    print("\n1. Testing double integral operation:")
    try:
        expression = "x*y"
        variables = ["x", "y"]
        limits = [("x", "0", "1"), ("y", "0", "1")]
        result = solve_multiple_integral(expression, limits)
        print(f"  ∫∫ x*y dx dy = {result}")
    except Exception as e:
        print(f"  ERROR in double integral: {e}")
    
    # Test 2: Gradient
    print("\n2. Testing gradient operation:")
    try:
        function_str = "x^2 + y^2"
        function_expr = parse_expression(function_str)
        variables = ["x", "y"]
        result = solve_gradient(str(function_expr), variables)
        print(f"  ∇(x^2 + y^2) = {result}")
    except Exception as e:
        print(f"  ERROR in gradient: {e}")
    
    # Test 3: Divergence
    print("\n3. Testing divergence operation:")
    try:
        vector_field_str = "x, y, z"
        vector_field = parse_vector(vector_field_str)
        variables = ["x", "y", "z"]
        result = solve_divergence(vector_field, variables)
        print(f"  ∇·(x, y, z) = {result}")
    except Exception as e:
        print(f"  ERROR in divergence: {e}")
    
    # Test 4: Parse LaTeX expression
    print("\n4. Testing LaTeX parsing:")
    try:
        latex_expr = r'\sin(x) + \cos(y)'
        result = parse_expression(latex_expr)
        print(f"  '{latex_expr}' -> {result}")
    except Exception as e:
        print(f"  ERROR in LaTeX: {e}")
    
    print("\nOperation testing completed!")

if __name__ == "__main__":
    test_operations()
