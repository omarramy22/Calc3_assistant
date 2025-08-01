#!/usr/bin/env python3

import sys
sys.path.append('.')

from calc3 import solve_partial_derivative, safe_sympify
import sympy as sp

# Test the exact same calculation that should be working
expr = "x**2* y+y*sin(xy)"
variables = ['x']

print("=== DEBUGGING PARTIAL DERIVATIVE ===")
print(f"Expression: {expr}")
print(f"Variables: {variables}")

# Step 1: Parse the expression 
try:
    expression = safe_sympify(expr)
    print(f"Parsed expression: {expression}")
    print(f"Expression type: {type(expression)}")
except Exception as e:
    print(f"Failed to parse expression: {e}")
    exit(1)

# Step 2: Create symbols
x, y = sp.symbols('x y')
print(f"Symbols created: x={x}, y={y}")

# Step 3: Manually compute the derivative
manual_derivative = sp.diff(expression, x)
print(f"Manual derivative: {manual_derivative}")
print(f"Manual derivative simplified: {sp.simplify(manual_derivative)}")

# Step 4: Use our function
our_derivative = solve_partial_derivative(expr, variables)
print(f"Our function result: {our_derivative}")

# Step 5: Compare
print(f"Match: {str(manual_derivative) == our_derivative}")

print("\n=== TESTING WITH ORIGINAL LATEX ===")
latex_expr = "x^2\\cdot y+y\\sin\\left(xy\\right)"
our_latex_result = solve_partial_derivative(latex_expr, ['x'])
print(f"LaTeX result: {our_latex_result}")
