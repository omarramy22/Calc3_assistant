#!/usr/bin/env python3

import sys
sys.path.append('.')

from calc3 import safe_sympify
import sympy as sp

# Test parsing
expr = "x**2* y+y*sin(xy)"
print(f"Original expression: {expr}")

parsed = safe_sympify(expr)
print(f"Parsed expression: {parsed}")

# Check the terms
print(f"Expression args: {parsed.args}")

x, y = sp.symbols('x y')

# Manual check
manual_expr = x**2 * y + y * sp.sin(x*y)
print(f"Manual expression: {manual_expr}")

print(f"Expressions equal: {sp.simplify(parsed - manual_expr) == 0}")

# Compute derivatives manually
manual_derivative = sp.diff(manual_expr, x)
parsed_derivative = sp.diff(parsed, x)

print(f"Manual derivative: {manual_derivative}")  
print(f"Parsed derivative: {parsed_derivative}")
print(f"Derivatives equal: {sp.simplify(manual_derivative - parsed_derivative) == 0}")

# Let's specifically look at sin(xy) parsing
sin_term = "sin(xy)"
print(f"\nTesting sin term: {sin_term}")
sin_parsed = safe_sympify(sin_term)
print(f"Sin parsed: {sin_parsed}")
print(f"Sin derivative: {sp.diff(sin_parsed, x)}")
