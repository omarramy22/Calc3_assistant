#!/usr/bin/env python3

# Test script to verify the fixes
from parser import parse_single_expression
from calc3 import solve_partial_derivative, solve_multiple_integral

def test_parser_fix():
    print("=== Testing Parser Fix ===")
    
    # Test x^2 parsing
    expr = parse_single_expression("x^2")
    print(f"x^2 -> {expr}")
    
    # Test more complex expressions
    expr2 = parse_single_expression("x^3 + y^2")
    print(f"x^3 + y^2 -> {expr2}")
    
    # Test with trigonometric functions
    expr3 = parse_single_expression("\\sin(x^2)")
    print(f"\\sin(x^2) -> {expr3}")

def test_derivative():
    print("\n=== Testing Partial Derivative ===")
    
    # Test x^2 derivative
    try:
        expr = parse_single_expression("x^2")
        result = solve_partial_derivative(expr, ['x'], 1)
        print(f"d/dx(x^2) = {result}")
    except Exception as e:
        print(f"Error with x^2 derivative: {e}")
    
    # Test more complex derivative
    try:
        expr = parse_single_expression("x^3 + y^2")
        result = solve_partial_derivative(expr, ['x'], 1)
        print(f"∂/∂x(x^3 + y^2) = {result}")
    except Exception as e:
        print(f"Error with complex derivative: {e}")

def test_integrals():
    print("\n=== Testing Multiple Integrals ===")
    
    # Test double integral
    try:
        expr = "x**2 + y**2"
        limits = [['0', '1'], ['0', '1']]  # x from 0 to 1, y from 0 to 1
        result = solve_multiple_integral(expr, limits)
        print(f"∬(x^2 + y^2) dx dy = {result}")
    except Exception as e:
        print(f"Error with double integral: {e}")

if __name__ == "__main__":
    test_parser_fix()
    test_derivative()
    test_integrals()
    print("\n=== Test Complete ===")
