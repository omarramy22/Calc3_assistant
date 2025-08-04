from sympy import sympify, symbols, latex
from sympy.parsing.latex import parse_latex

def parse_expression(expr):
    """
    Parse any mathematical expression (LaTeX or regular) using SymPy.
    Returns a SymPy expression that can be converted to string.
    """
    if not expr or not expr.strip():
        return None
    
    expr = expr.strip()
    
    # Remove LaTeX delimiters if present
    if expr.startswith('$$') and expr.endswith('$$'):
        expr = expr[2:-2].strip()
    elif expr.startswith('$') and expr.endswith('$'):
        expr = expr[1:-1].strip()
    
    try:
        # Try LaTeX parsing first if it looks like LaTeX
        if '\\' in expr:
            try:
                return parse_latex(expr)
            except:
                # If parse_latex fails, do manual conversion
                expr = expr.replace('\\sin', 'sin')
                expr = expr.replace('\\cos', 'cos')
                expr = expr.replace('\\tan', 'tan')
                expr = expr.replace('\\sec', 'sec')
                expr = expr.replace('\\csc', 'csc')
                expr = expr.replace('\\cot', 'cot')
                expr = expr.replace('\\ln', 'log')
                expr = expr.replace('\\log', 'log')
                expr = expr.replace('\\pi', 'pi')
                expr = expr.replace('\\cdot', '*')
                expr = expr.replace('^', '**')
                return sympify(expr)
        else:
            # Handle common patterns and use sympify
            expr = expr.replace('^', '**')  # Convert powers
            # Remove curly braces in exponents: x^{2} -> x^2
            return sympify(expr)
    except:
        try:
            # Fallback: try sympify with power conversion
            expr = expr.replace('^', '**')
            return sympify(expr)
        except:
            # Last resort: return as symbol
            return symbols(expr)

def parse_integral_latex(latex_expr):
    """
    Parse LaTeX integral expressions and extract integrand and limits.
    Special handling for integrals since they come as LaTeX templates.
    """
    if not latex_expr or not latex_expr.strip():
        return "", []
    
    latex_expr = latex_expr.strip()
    
    # Remove LaTeX delimiters
    if latex_expr.startswith('$$') and latex_expr.endswith('$$'):
        latex_expr = latex_expr[2:-2].strip()
    elif latex_expr.startswith('$') and latex_expr.endswith('$'):
        latex_expr = latex_expr[1:-1].strip()
    
    try:
        # Parse the LaTeX integral using SymPy's parse_latex
        try:
            parsed = parse_latex(latex_expr)
        except:
            # If parse_latex fails, return the original expression
            return latex_expr, []
        
        # If it's an Integral object, extract components
        if hasattr(parsed, 'function') and hasattr(parsed, 'limits'):
            integrand = str(parsed.function)
            
            # Convert limits to the format expected by calc3.py
            limits = []
            for limit_tuple in parsed.limits:
                if len(limit_tuple) == 3:
                    var, lower, upper = limit_tuple
                    limits.append((str(var), str(lower), str(upper)))
                else:
                    var = limit_tuple[0]
                    limits.append((str(var), "0", "1"))
            
            return integrand, limits
        else:
            # Not an integral, just return the expression
            return str(parsed), []
    except:
        # Fallback: return the original expression
        return latex_expr, []

def parse_vector(vector_str):
    """Parse vector input (comma-separated values)"""
    if not vector_str:
        return []
    
    # Remove brackets if present
    vector_str = vector_str.strip()
    if vector_str.startswith('[') and vector_str.endswith(']'):
        vector_str = vector_str[1:-1]
    
    # Split and parse each component
    components = []
    for comp in vector_str.split(','):
        comp = comp.strip()
        if comp:
            parsed = parse_expression(comp)
            components.append(str(parsed) if parsed else comp)
    
    return components

def parse_limits(limits_str):
    """Parse limits in various formats"""
    if not limits_str:
        return [0, 1]
    
    limits_str = limits_str.strip()
    
    # Handle comma-separated: "0, 1"
    if ',' in limits_str:
        parts = limits_str.split(',')
        if len(parts) == 2:
            try:
                return [sympify(parts[0].strip()), sympify(parts[1].strip())]
            except:
                return [0, 1]
    
    # Handle "to" format: "0 to 1"
    if 'to' in limits_str.lower():
        parts = limits_str.lower().split('to')
        if len(parts) == 2:
            try:
                return [sympify(parts[0].strip()), sympify(parts[1].strip())]
            except:
                return [0, 1]
    
    # Handle space-separated: "0 1"
    parts = limits_str.split()
    if len(parts) == 2:
        try:
            return [sympify(parts[0]), sympify(parts[1])]
        except:
            return [0, 1]
    
    return [0, 1]

def parse_integral_limits(limits_str, variables):
    """Parse limits for multiple integrals"""
    if not limits_str or not variables:
        # Default limits based on number of variables
        return [(var, '0', '1') for var in variables]
    
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
            limits.append((var, '0', '1'))
    
    return limits
