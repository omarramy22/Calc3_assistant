#!/usr/bin/env python3
"""
Simple test script for the new simplified parser and app
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from parser import parse_expression, parse_integral_latex, parse_vector, parse_limits

def test_parser():
    print("Testing simplified parser...")
    
    # Test basic expression parsing
    print("\n1. Basic expressions:")
    print(f"  'x^2 + y' -> {parse_expression('x^2 + y')}")
    print(f"  'sin(x)' -> {parse_expression('sin(x)')}")
    print(f"  'x*y + z' -> {parse_expression('x*y + z')}")
    
    # Test LaTeX expressions
    print("\n2. LaTeX expressions:")
    print(f"  '\\sin(x)' -> {parse_expression(r'\sin(x)')}")
    print(f"  'x^2 + y^2' -> {parse_expression('x^2 + y^2')}")
    print(f"  '\\cos(\\pi x)' -> {parse_expression(r'\cos(\pi x)')}")
    print(f"  '\\frac{{x^2}}{{y}}' -> {parse_expression(r'\frac{x^2}{y}')}")
    print(f"  'e^{{x \\cdot y}}' -> {parse_expression(r'e^{x \cdot y}')}")
    
    # Test vector parsing
    print("\n3. Vector parsing:")
    print(f"  'x, y, z' -> {parse_vector('x, y, z')}")
    print(f"  '[sin(t), cos(t)]' -> {parse_vector('[sin(t), cos(t)]')}")
    
    # Test limits
    print("\n4. Limits parsing:")
    print(f"  '0, 1' -> {parse_limits('0, 1')}")
    print(f"  '0 to 2*pi' -> {parse_limits('0 to 2*pi')}")
    
    # Test integral LaTeX (if possible)
    print("\n5. LaTeX integral:")
    try:
        integrand, limits = parse_integral_latex(r'\int_0^1 \int_0^1 x*y \, dx \, dy')
        print(f"  Integrand: {integrand}")
        print(f"  Limits: {limits}")
    except Exception as e:
        print(f"  LaTeX integral test failed: {e}")
    
    print("\nParser tests completed!")

if __name__ == "__main__":
    test_parser()
