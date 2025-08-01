from calc3 import solve_partial_derivative
from sympy import symbols, diff, sin, cos

# Test the partial derivative calculation
expr = r'x^2\cdot y+y\sin\left(xy\right)'
print("Expression:", expr)

# Test with our function
result = solve_partial_derivative(expr, ['x'], 1)
print("Our result:", result)

# Test with direct SymPy to verify expected result
x, y = symbols('x y')
sympy_expr = x**2*y + y*sin(x*y)
expected = diff(sympy_expr, x)
print("Expected result:", expected)
print("Expected simplified:", expected.simplify())

# Check if they match
print("Results match:", str(result) == str(expected))
