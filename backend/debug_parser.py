#!/usr/bin/env python3
"""
Test the updated parser with parse_latex
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from parser import parse_expression, parse_integral_latex, parse_vector

def test_parse_latex():
    print("Testing parser with SymPy's parse_latex...")
    
    # Test basic LaTeX expressions
    print("\n1. Basic LaTeX expressions:")
    test_cases = [
        r'\sin(x)',
        r'\cos(x^2)',
        r'x^2 + y^2',
        r'\frac{x}{y}',
        r'e^{x \cdot y}',
        r'\sin^2(x) + \cos^2(x)',
        r'\pi x + \ln(y)'
    ]
    
    for case in test_cases:
        try:
            result = parse_expression(case)
            print(f"  '{case}' -> {result}")
        except Exception as e:
            print(f"  '{case}' -> ERROR: {e}")
    
    # Test regular expressions
    print("\n2. Regular expressions:")
    regular_cases = [
        'x^2 + y',
        'sin(x)*cos(y)', 
        'x*y + z^2',
        'exp(x) + log(y)'
    ]
    
    for case in regular_cases:
        try:
            result = parse_expression(case)
            print(f"  '{case}' -> {result}")
        except Exception as e:
            print(f"  '{case}' -> ERROR: {e}")
    
    # Test integral parsing
    print("\n3. LaTeX integral expressions:")
    integral_cases = [
        r'\int x \, dx',
        r'\int_0^1 x^2 \, dx',
        r'\int_0^1 \int_0^1 x y \, dx \, dy'
    ]
    
    for case in integral_cases:
        try:
            integrand, limits = parse_integral_latex(case)
            print(f"  '{case}' -> integrand: {integrand}, limits: {limits}")
        except Exception as e:
            print(f"  '{case}' -> ERROR: {e}")
    
    # Test vector parsing
    print("\n4. Vector parsing:")
    vector_cases = [
        'x, y, z',
        'sin(t), cos(t)',
        '[x^2, y^2, z^2]'
    ]
    
    for case in vector_cases:
        try:
            result = parse_vector(case)
            print(f"  '{case}' -> {result}")
        except Exception as e:
            print(f"  '{case}' -> ERROR: {e}")
    
    print("\nTesting completed!")

if __name__ == "__main__":
    test_parse_latex()
