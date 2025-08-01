#!/usr/bin/env python3

# Test script to check what's happening without running server
import sys
sys.path.append('.')

# Import the functions directly to test them
import re

def extract_integrand_from_latex(latex_expr):
    """Extract the integrand from LaTeX integral expressions"""
    print(f"DEBUG extract_integrand_from_latex: Input = '{latex_expr}'")
    
    if not latex_expr:
        print("DEBUG extract_integrand_from_latex: Empty input")
        return ""
    
    # Remove $$ delimiters
    expr = latex_expr.strip()
    print(f"DEBUG extract_integrand_from_latex: After strip = '{expr}'")
    
    if expr.startswith('$$') and expr.endswith('$$'):
        expr = expr[2:-2].strip()
        print(f"DEBUG extract_integrand_from_latex: After removing $$ = '{expr}'")
    elif expr.startswith('$') and expr.endswith('$'):
        expr = expr[1:-1].strip()
        print(f"DEBUG extract_integrand_from_latex: After removing $ = '{expr}'")
    
    # Look for patterns like \int_a^b\int_c^d(expression)
    # Pattern to match integrals and extract the integrand
    integrand_match = re.search(r'\([^)]+\)', expr)
    print(f"DEBUG extract_integrand_from_latex: Parentheses match = {integrand_match}")
    
    if integrand_match:
        integrand = integrand_match.group(0)[1:-1]  # Remove parentheses
        print(f"DEBUG extract_integrand_from_latex: Extracted from parentheses = '{integrand.strip()}'")
        return integrand.strip()
    
    # If no parentheses, try to extract expression after integral symbols
    print("DEBUG extract_integrand_from_latex: No parentheses found, trying regex cleanup")
    expr = re.sub(r'\\int[_^{}\d\w\s]*', '', expr)
    print(f"DEBUG extract_integrand_from_latex: After removing \\int = '{expr}'")
    expr = re.sub(r'\\,d[xyz]', '', expr)  # Remove dx, dy, dz
    print(f"DEBUG extract_integrand_from_latex: After removing dx,dy,dz = '{expr}'")
    expr = expr.strip()
    
    result = expr if expr else "x*y"  # Default fallback
    print(f"DEBUG extract_integrand_from_latex: Final result = '{result}'")
    return result

def test_latex_parsing():
    print("=== Testing LaTeX Parsing ===\n")
    
    test_expressions = [
        "$$ \\int_0^1\\int_0^1(xy)\\,dy\\,dx $$",
        "\\int_0^1\\int_0^1(xy)\\,dy\\,dx",
        "(xy)",
        "xy",
        "",
        None
    ]
    
    for expr in test_expressions:
        print(f"Input: {repr(expr)}")
        result = extract_integrand_from_latex(expr)
        print(f"Output: '{result}'")
        print("-" * 50)

def test_data_processing():
    print("\n=== Testing Data Processing ===\n")
    
    # Simulate the data that would come from frontend
    test_data = {
        "operation": "double_integral",
        "expression": "$$ \\int_0^1\\int_0^1(xy)\\,dy\\,dx $$",
        "variables": "x,y",
        "limits": "0,1,0,1"
    }
    
    expression_str = test_data.get("expression", "")
    print(f"expression_str = '{expression_str}'")
    print(f"expression_str.strip() = '{expression_str.strip()}'")
    print(f"len(expression_str.strip()) = {len(expression_str.strip())}")
    print(f"'\\int' in expression_str = {'\\int' in expression_str}")
    
    if not expression_str.strip():
        print("Would return: Expression cannot be empty")
    else:
        print("Expression is not empty, continuing...")
        
        if '\\int' in expression_str:
            print("LaTeX integral detected")
            integrand = extract_integrand_from_latex(expression_str)
            print(f"Extracted integrand: '{integrand}'")
        else:
            print("Regular expression")

if __name__ == "__main__":
    test_latex_parsing()
    test_data_processing()
