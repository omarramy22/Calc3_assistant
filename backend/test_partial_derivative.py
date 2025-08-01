from parser import parse_single_expression
from sympy import sympify, symbols

# Test the problematic partial derivative expression
test_expr = r'x**2\cdot y+y\sin\left(xy\right)'
print(f"Original expression: {test_expr}")

# Parse it
parsed = parse_single_expression(test_expr)
print(f"Parsed expression: {parsed}")

# Test with sympify
try:
    x, y = symbols('x y')
    result = sympify(parsed, locals={'x': x, 'y': y})
    print(f"Sympify successful: {result}")
except Exception as e:
    print(f"Sympify failed: {e}")

# Test a few more cases
test_cases = [
    r'x**2\cdot y',
    r'\sin\left(xy\right)', 
    r'x**2 + y\cdot\sin\left(x\right)',
    r'\left(x+y\right)**2'
]

print("\n=== Testing more expressions ===")
for expr in test_cases:
    parsed = parse_single_expression(expr)
    print(f"'{expr}' -> '{parsed}'")
    try:
        result = sympify(parsed, locals={'x': x, 'y': y})
        print(f"  Sympify: OK -> {result}")
    except Exception as e:
        print(f"  Sympify: ERROR -> {e}")
    print()
