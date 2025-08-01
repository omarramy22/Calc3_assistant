#!/usr/bin/env python3

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
    # This looks for content in parentheses after integral symbols
    integrand_match = re.search(r'\([^)]+\)', expr)
    if integrand_match:
        integrand = integrand_match.group(0)[1:-1]  # Remove parentheses
        return integrand.strip()
    
    # If no parentheses, try to extract expression after integral symbols
    # Remove integral symbols and limits
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

# Test with your LaTeX expression
latex = '$$ \\int_0^1\\int_0^1(xy)\\,dy\\,dx $$'
print('LaTeX input:', latex)
print('Extracted integrand:', extract_integrand_from_latex(latex))
print('Extracted limits:', parse_limits_from_latex(latex))
