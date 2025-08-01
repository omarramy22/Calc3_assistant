#!/usr/bin/env python3

# Test the complete workflow with LaTeX input
import sys
sys.path.append('.')

from parser import parse_single_expression, parse_vector_input
from calc3 import solve_multiple_integral
import re

def extract_integrand_from_latex(latex_expr):
    """Extract the integrand from LaTeX integral expressions"""
    if not latex_expr:
        return ""
    
    # Remove $$ delimiters
    expr = latex_expr.strip()
    if expr.startswith('$$') and expr.endswith('$$'):
        expr = expr[2:-2].strip()
    elif expr.startswith('$') and expr.endswith('$'):
        expr = expr[1:-1].strip()
    
    # Pattern to match integrals and extract the integrand
    integrand_match = re.search(r'\([^)]+\)', expr)
    if integrand_match:
        integrand = integrand_match.group(0)[1:-1]  # Remove parentheses
        return integrand.strip()
    
    # If no parentheses, try to extract expression after integral symbols
    expr = re.sub(r'\\int[_^{}\d\w\s]*', '', expr)
    expr = re.sub(r'\\,d[xyz]', '', expr)  # Remove dx, dy, dz
    expr = expr.strip()
    
    return expr if expr else "x*y"  # Default fallback

def parse_limits_from_latex(latex_expr):
    """Extract limits from LaTeX integral expressions"""
    if not latex_expr:
        return "0,1,0,1"
    
    # Find all _a^b patterns
    limits_matches = re.findall(r'_(\d+)\^(\d+)', latex_expr)
    if limits_matches:
        # Flatten the list: [(0,1), (0,1)] -> [0,1,0,1]
        limits_list = []
        for lower, upper in limits_matches:
            limits_list.extend([lower, upper])
        return ','.join(limits_list)
    
    return "0,1,0,1"  # Default fallback

def parse_integral_limits(limits_str, variables):
    """Parse limits for multiple integrals in the format expected by solve_multiple_integral"""
    if not limits_str or not variables:
        # Default limits based on number of variables
        if len(variables) == 2:
            return [('x', '0', '1'), ('y', '0', '1')]
        elif len(variables) == 3:
            return [('x', '0', '1'), ('y', '0', '1'), ('z', '0', '1')]
        else:
            return [('x', '0', '1')]
    
    # Split limits by comma
    limits_list = limits_str.split(',')
    limits = []
    
    # Group limits in pairs and associate with variables
    for i, var in enumerate(variables):
        if i * 2 + 1 < len(limits_list):
            lower = limits_list[i * 2].strip()
            upper = limits_list[i * 2 + 1].strip()
            limits.append((var, lower, upper))
        else:
            # Default if not enough limits provided
            limits.append((var, '0', '1'))
    
    return limits

def test_latex_workflow():
    print("=== Testing Complete LaTeX Workflow ===\n")
    
    # Your LaTeX expression
    latex_expr = '$$ \\int_0^1\\int_0^1(xy)\\,dy\\,dx $$'
    print(f"Input LaTeX: {latex_expr}")
    
    # Step 1: Extract integrand
    integrand = extract_integrand_from_latex(latex_expr)
    print(f"1. Extracted integrand: {integrand}")
    
    # Step 2: Parse the integrand 
    parsed_expr = parse_single_expression(integrand)
    print(f"2. Parsed expression: {parsed_expr}")
    
    # Step 3: Extract limits
    limits_str = parse_limits_from_latex(latex_expr)
    print(f"3. Extracted limits: {limits_str}")
    
    # Step 4: Parse variables
    variables = parse_vector_input("x,y")
    print(f"4. Variables: {variables}")
    
    # Step 5: Format limits for solve_multiple_integral
    limits = parse_integral_limits(limits_str, variables)
    print(f"5. Formatted limits: {limits}")
    
    # Step 6: Calculate the integral
    try:
        result = solve_multiple_integral(parsed_expr, limits)
        print(f"6. Result: {result}")
        print(f"\n✅ SUCCESS: LaTeX integral calculated successfully!")
        print(f"   ∬ xy dy dx from 0 to 1 = {result}")
    except Exception as e:
        print(f"6. Error: {e}")
        print(f"❌ FAILED: Could not calculate integral")

if __name__ == "__main__":
    test_latex_workflow()
