from calc3 import safe_sympify
from sympy import symbols

# Test the problematic partial derivative expression
test_expr = r'x**2\cdot y+y\sin\left(xy\right)'
print(f"Testing expression: {test_expr}")

# Test safe_sympify
try:
    result = safe_sympify(test_expr)
    print(f"safe_sympify successful: {result}")
    print(f"Result type: {type(result)}")
except Exception as e:
    print(f"safe_sympify failed: {e}")

# Test the LaTeX parser directly
from parser import parse_latex_expression
try:
    parsed = parse_latex_expression(test_expr)
    print(f"parse_latex_expression: '{test_expr}' -> '{parsed}'")
    
    # Test sympify on the parsed result
    x, y = symbols('x y')
    result = safe_sympify(parsed)
    print(f"sympify on parsed result: {result}")
except Exception as e:
    print(f"Direct LaTeX parsing failed: {e}")
