#!/usr/bin/env python3
"""
Comprehensive debugging script for parser and app functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from parser import parse_expression, parse_integral_latex, parse_vector, parse_limits
from calc3 import solve_multiple_integral, solve_gradient, solve_partial_derivative

def debug_parser():
    print("=" * 60)
    print("DEBUGGING PARSER FUNCTIONS")
    print("=" * 60)
    
    # Test 1: Basic expressions
    print("\n1. Testing basic expression parsing:")
    test_expressions = [
        "x^2 + y",
        "sin(x)",
        "x*y + z^2",
        "exp(x)",
        "log(x)",
    ]
    
    for expr in test_expressions:
        try:
            result = parse_expression(expr)
            print(f"  ✓ '{expr}' -> {result} (type: {type(result).__name__})")
        except Exception as e:
            print(f"  ✗ '{expr}' -> ERROR: {e}")
    
    # Test 2: LaTeX expressions
    print("\n2. Testing LaTeX expression parsing:")
    latex_expressions = [
        r"\sin(x)",
        r"\cos(x^2)",
        r"\frac{x^2}{y}",
        r"x \cdot y",
        r"e^{x}",
        r"\pi x",
    ]
    
    for expr in latex_expressions:
        try:
            result = parse_expression(expr)
            print(f"  ✓ '{expr}' -> {result} (type: {type(result).__name__})")
        except Exception as e:
            print(f"  ✗ '{expr}' -> ERROR: {e}")
    
    # Test 3: Vector parsing
    print("\n3. Testing vector parsing:")
    vector_tests = [
        "x, y, z",
        "[sin(t), cos(t)]",
        "t^2, 2*t, 3",
        "x*y, y*z, x*z",
    ]
    
    for vector in vector_tests:
        try:
            result = parse_vector(vector)
            print(f"  ✓ '{vector}' -> {result}")
        except Exception as e:
            print(f"  ✗ '{vector}' -> ERROR: {e}")
    
    # Test 4: Limits parsing
    print("\n4. Testing limits parsing:")
    limits_tests = [
        "0, 1",
        "0 to 2*pi",
        "-1, 1",
        "0 1",
    ]
    
    for limits in limits_tests:
        try:
            result = parse_limits(limits)
            print(f"  ✓ '{limits}' -> {result}")
        except Exception as e:
            print(f"  ✗ '{limits}' -> ERROR: {e}")

def debug_calc_integration():
    print("\n" + "=" * 60)
    print("DEBUGGING CALC3 INTEGRATION")
    print("=" * 60)
    
    # Test simple integrations
    integration_tests = [
        ("x*y", [("x", "0", "1"), ("y", "0", "1")], "Double integral: x*y"),
        ("x^2", [("x", "0", "1")], "Single integral: x^2"),
        ("sin(x)", [("x", "0", "pi")], "Single integral: sin(x)"),
        ("1", [("x", "0", "1"), ("y", "0", "1")], "Double integral: constant 1"),
    ]
    
    for expr, limits, description in integration_tests:
        try:
            result = solve_multiple_integral(expr, limits)
            print(f"  ✓ {description}: {result}")
        except Exception as e:
            print(f"  ✗ {description}: ERROR: {e}")

def debug_other_operations():
    print("\n" + "=" * 60)
    print("DEBUGGING OTHER OPERATIONS")
    print("=" * 60)
    
    # Test gradient
    try:
        result = solve_gradient("x^2 + y^2", ["x", "y"])
        print(f"  ✓ Gradient of x^2 + y^2: {result}")
    except Exception as e:
        print(f"  ✗ Gradient test: ERROR: {e}")
    
    # Test partial derivative
    try:
        result = solve_partial_derivative("x^2*y", ["x"], 1)
        print(f"  ✓ Partial derivative ∂/∂x(x^2*y): {result}")
    except Exception as e:
        print(f"  ✗ Partial derivative test: ERROR: {e}")

def test_latex_alternatives():
    print("\n" + "=" * 60)
    print("TESTING LATEX PARSING ALTERNATIVES")
    print("=" * 60)
    
    test_expr = r"\sin(x^2) + \cos(y)"
    
    # Method 1: Try latex2sympy2
    print("\n1. Testing latex2sympy2:")
    try:
        from latex2sympy2 import latex2sympy
        result = latex2sympy(test_expr)
        print(f"  ✓ latex2sympy2: {result}")
    except ImportError:
        print("  ✗ latex2sympy2 not installed")
    except Exception as e:
        print(f"  ✗ latex2sympy2 error: {e}")
    
    # Method 2: Try SymPy's parse_latex
    print("\n2. Testing SymPy's parse_latex:")
    try:
        from sympy.parsing.latex import parse_latex
        result = parse_latex(test_expr)
        print(f"  ✓ SymPy parse_latex: {result}")
    except ImportError:
        print("  ✗ SymPy parse_latex not available")
    except Exception as e:
        print(f"  ✗ SymPy parse_latex error: {e}")
    
    # Method 3: Manual conversion
    print("\n3. Testing manual LaTeX conversion:")
    try:
        manual_expr = test_expr.replace(r'\sin', 'sin').replace(r'\cos', 'cos').replace('^', '**')
        from sympy import sympify
        result = sympify(manual_expr)
        print(f"  ✓ Manual conversion: {result}")
    except Exception as e:
        print(f"  ✗ Manual conversion error: {e}")

if __name__ == "__main__":
    debug_parser()
    debug_calc_integration()
    debug_other_operations()
    test_latex_alternatives()
    print("\n" + "=" * 60)
    print("DEBUGGING COMPLETE")
    print("=" * 60)
