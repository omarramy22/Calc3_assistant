#!/usr/bin/env python3

# Direct test without imports that might fail
test_expr = r'x**2\cdot y+y\sin\left(xy\right)'
print("Original expression:")
print(repr(test_expr))

# Manual parsing
import re
cleaned = test_expr

# Step by step transformations
print("\nStep-by-step transformations:")
print("1. Original:", repr(cleaned))

cleaned = re.sub(r'\\left[\(\[\{]', '(', cleaned)
print("2. After \\left->( :", repr(cleaned))

cleaned = re.sub(r'\\right[\)\]\}]', ')', cleaned)  
print("3. After \\right->) :", repr(cleaned))

cleaned = cleaned.replace('\\left', '').replace('\\right', '')
print("4. After remove remaining \\left/\\right:", repr(cleaned))

cleaned = cleaned.replace('\\cdot', '*')
print("5. After \\cdot->* :", repr(cleaned))

cleaned = cleaned.replace('\\sin', 'sin')
print("6. After \\sin->sin :", repr(cleaned))

cleaned = cleaned.replace('^', '**')
print("7. After ^->** :", repr(cleaned))

print("\nFinal result:")
print(repr(cleaned))

# Test if this can be sympified
try:
    from sympy import sympify, symbols
    x, y = symbols('x y')
    result = sympify(cleaned, locals={'x': x, 'y': y})
    print("Sympify successful!")
    print("Result:", result)
except Exception as e:
    print("Sympify failed:", e)
    print("Error type:", type(e).__name__)
