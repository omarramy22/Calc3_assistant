from calc3 import solve_partial_derivative, safe_sympify

print("=== Testing LaTeX Expression Parsing ===")

# Test the problematic expression
expr = r'x**2\cdot y+y\sin\left(xy\right)'
print(f"Expression: {expr}")

# Test parsing
try:
    parsed = safe_sympify(expr)
    print(f"Parsed successfully: {parsed}")
except Exception as e:
    print(f"Parsing failed: {e}")

# Test partial derivative
try:
    result = solve_partial_derivative(expr, ['x'], 1)
    print(f"Partial derivative w.r.t. x: {result}")
except Exception as e:
    print(f"Partial derivative failed: {e}")

print("\n=== Testing simpler cases ===")
simple_cases = [
    r'x**2\cdot y',
    r'\sin\left(x\right)',
    r'x + y\cdot z'
]

for case in simple_cases:
    try:
        parsed = safe_sympify(case)
        print(f"'{case}' -> {parsed}")
    except Exception as e:
        print(f"'{case}' -> ERROR: {e}")
