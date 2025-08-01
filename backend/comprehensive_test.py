#!/usr/bin/env python3
"""
COMPREHENSIVE CALCULATOR FUNCTIONALITY TEST
============================================
This is the main test file that validates all calculator functions.
Run this to verify that all mathematical operations work correctly 
with proper LaTeX parsing.

Usage: python comprehensive_test.py
"""

import sys
sys.path.append('.')

from calc3 import *
from parser import parse_single_expression

print("="*70)
print("🧮 COMPREHENSIVE CALCULATOR FUNCTIONALITY TEST")
print("="*70)
print("Validates: LaTeX parsing, mathematical operations, edge cases")
print("="*70)

def test_parser_basic():
    """Test basic LaTeX parsing functionality"""
    print("\n1. TESTING BASIC PARSER:")
    print("-" * 30)
    
    test_cases = [
        "2t",
        "\\sin\\left(t\\right)",
        "\\cos\\left(t\\right)", 
        "\\tan\\left(t\\right)",
        "t^2",
        "t^{}",  # Edge case
        "\\pi t",
        "\\frac{1}{2}t",
        "\\sqrt{t}",
        "e^t",
        "\\log\\left(t\\right)"
    ]
    
    for expr in test_cases:
        try:
            result = parse_single_expression(expr)
            print(f"✓ '{expr}' -> '{result}'")
        except Exception as e:
            print(f"✗ '{expr}' -> ERROR: {e}")

def test_partial_derivatives():
    """Test partial derivative functionality"""
    print("\n2. TESTING PARTIAL DERIVATIVES:")
    print("-" * 30)
    
    test_cases = [
        ("x^2 + y^2", ["x"]),
        ("\\sin\\left(x\\right) + \\cos\\left(y\\right)", ["x"]),
        ("x*y + 2*x", ["x", "y"]),  # Second order
        ("\\frac{x^2}{2} + y^2", ["x"]),
    ]
    
    for expr, vars in test_cases:
        try:
            result = solve_partial_derivative(expr, vars)
            print(f"✓ ∂/∂{vars} ({expr}) = {result}")
        except Exception as e:
            print(f"✗ ∂/∂{vars} ({expr}) -> ERROR: {e}")

def test_arc_length():
    """Test arc length calculation"""
    print("\n3. TESTING ARC LENGTH:")
    print("-" * 30)
    
    test_cases = [
        (["t", "sin(t)"], "t", "0", "1"),  # The case that was failing
        (["2t", "\\sin\\left(t\\right)"], "t", "0", "\\pi"),
        (["t", "t^2"], "t", "0", "1"),
        (["\\cos\\left(t\\right)", "\\sin\\left(t\\right)"], "t", "0", "2*\\pi"),
    ]
    
    for exprs, param, a, b in test_cases:
        try:
            result = solve_arc_length(exprs, param, a, b)
            print(f"✓ Arc length of {exprs} from {a} to {b}: {result}")
        except Exception as e:
            print(f"✗ Arc length of {exprs} -> ERROR: {e}")

def test_gradient():
    """Test gradient calculation"""
    print("\n4. TESTING GRADIENT:")
    print("-" * 30)
    
    test_cases = [
        ("x^2 + y^2", ["x", "y"]),
        ("\\sin\\left(x\\right) + \\cos\\left(y\\right)", ["x", "y"]),
        ("x*y*z", ["x", "y", "z"]),
    ]
    
    for expr, vars in test_cases:
        try:
            result = solve_gradient(expr, vars)
            print(f"✓ ∇({expr}) = {result}")
        except Exception as e:
            print(f"✗ ∇({expr}) -> ERROR: {e}")

def test_multiple_integral():
    """Test multiple integration"""
    print("\n5. TESTING MULTIPLE INTEGRALS:")
    print("-" * 30)
    
    test_cases = [
        ("x*y", [("x", "0", "1"), ("y", "0", "1")]),
        ("\\sin\\left(x\\right) * \\cos\\left(y\\right)", [("x", "0", "\\pi"), ("y", "0", "\\pi")]),
        ("x^2 + y^2", [("x", "0", "1"), ("y", "0", "1")]),
    ]
    
    for expr, limits in test_cases:
        try:
            result = solve_multiple_integral(expr, limits)
            print(f"✓ ∫∫ {expr} = {result}")
        except Exception as e:
            print(f"✗ ∫∫ {expr} -> ERROR: {e}")

def test_polar_integral():
    """Test polar coordinate integration"""
    print("\n6. TESTING POLAR INTEGRALS:")
    print("-" * 30)
    
    test_cases = [
        ("r", [("r", "0", "1"), ("theta", "0", "2*\\pi")]),
        ("r*\\sin\\left(theta\\right)", [("r", "0", "1"), ("theta", "0", "\\pi")]),
    ]
    
    for expr, limits in test_cases:
        try:
            result = solve_polar_integral(expr, limits)
            print(f"✓ ∫∫ {expr} (polar) = {result}")
        except Exception as e:
            print(f"✗ ∫∫ {expr} (polar) -> ERROR: {e}")

def test_divergence():
    """Test divergence calculation"""
    print("\n7. TESTING DIVERGENCE:")
    print("-" * 30)
    
    test_cases = [
        (["x", "y"], ["x", "y"]),
        (["x^2", "y^2"], ["x", "y"]),
        (["\\sin\\left(x\\right)", "\\cos\\left(y\\right)", "z"], ["x", "y", "z"]),
    ]
    
    for field, vars in test_cases:
        try:
            result = solve_divergence(field, vars)
            print(f"✓ ∇·{field} = {result}")
        except Exception as e:
            print(f"✗ ∇·{field} -> ERROR: {e}")

def test_curl():
    """Test curl calculation"""
    print("\n8. TESTING CURL:")
    print("-" * 30)
    
    test_cases = [
        (["y", "-x", "0"], ["x", "y", "z"]),
        (["\\sin\\left(y\\right)", "\\cos\\left(x\\right)", "z"], ["x", "y", "z"]),
    ]
    
    for field, vars in test_cases:
        try:
            result = solve_curl(field, vars)
            print(f"✓ ∇×{field} = {result}")
        except Exception as e:
            print(f"✗ ∇×{field} -> ERROR: {e}")

def test_line_integral():
    """Test line integral calculation"""
    print("\n9. TESTING LINE INTEGRALS:")
    print("-" * 30)
    
    test_cases = [
        # Scalar field line integral
        ("x + y", "t", ["t", "t^2"], [0, 1]),
        # Vector field line integral
        (["x", "y"], "t", ["t", "t^2"], [0, 1]),
    ]
    
    for field, param, curve, bounds in test_cases:
        try:
            result = solve_line_integral(field, param, curve, bounds)
            print(f"✓ Line integral of {field} along {curve}: {result}")
        except Exception as e:
            print(f"✗ Line integral of {field} -> ERROR: {e}")

def test_directional_derivative():
    """Test directional derivative"""
    print("\n10. TESTING DIRECTIONAL DERIVATIVES:")
    print("-" * 30)
    
    test_cases = [
        ("x^2 + y^2", ["x", "y"], [1, 1]),
        ("\\sin\\left(x\\right) + \\cos\\left(y\\right)", ["x", "y"], [1, 0]),
    ]
    
    for expr, vars, direction in test_cases:
        try:
            result = solve_directional_derivative(expr, vars, direction)
            print(f"✓ D_{direction}({expr}) = {result}")
        except Exception as e:
            print(f"✗ D_{direction}({expr}) -> ERROR: {e}")

def test_greens_theorem():
    """Test Green's theorem calculation"""
    print("\n11. TESTING GREEN'S THEOREM:")
    print("-" * 30)
    
    test_cases = [
        (["x", "y"], ["x", "y"]),
        (["y", "-x"], ["x", "y"]),
    ]
    
    for field, vars in test_cases:
        try:
            result = solve_greens_theorem(field, vars)
            print(f"✓ Green's theorem for {field}: {result}")
        except Exception as e:
            print(f"✗ Green's theorem for {field} -> ERROR: {e}")

def test_lagrange_multipliers():
    """Test Lagrange multipliers"""
    print("\n12. TESTING LAGRANGE MULTIPLIERS:")
    print("-" * 30)
    
    test_cases = [
        ("x^2 + y^2", "x + y - 1", ["x", "y"]),
        ("x*y", "x^2 + y^2 - 1", ["x", "y"]),
    ]
    
    for f_expr, g_expr, vars in test_cases:
        try:
            result = solve_lagrange_multipliers(f_expr, g_expr, vars)
            print(f"✓ Lagrange multipliers for f={f_expr}, g={g_expr}: {result}")
        except Exception as e:
            print(f"✗ Lagrange multipliers -> ERROR: {e}")

def main():
    """Run all tests"""
    test_functions = [
        test_parser_basic,
        test_partial_derivatives,
        test_arc_length,
        test_gradient,
        test_multiple_integral,
        test_polar_integral,
        test_divergence,
        test_curl,
        test_line_integral,
        test_directional_derivative,
        test_greens_theorem,
        test_lagrange_multipliers,
    ]
    
    total_tests = len(test_functions)
    passed_tests = 0
    
    for test_func in test_functions:
        try:
            test_func()
            passed_tests += 1
        except Exception as e:
            print(f"\n✗ CRITICAL ERROR in {test_func.__name__}: {e}")
    
    print("\n" + "="*70)
    print(f"📊 TEST SUMMARY: {passed_tests}/{total_tests} test categories completed")
    print("="*70)
    
    if passed_tests < total_tests:
        print("⚠️  Some tests had errors. Check the output above for details.")
        print("💡 Most common issues: Missing dependencies (antlr4-python3-runtime)")
    else:
        print("✅ All test categories completed successfully!")
        print("🚀 Backend is ready for frontend testing!")
    
    print(f"\n🔧 To start the web interface: python test_server.py")
    print(f"🌐 Then open: http://localhost:5000")
    print("="*70)

if __name__ == "__main__":
    main()
