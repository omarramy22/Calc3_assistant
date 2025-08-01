from sympy import sympify, symbols, Integral

# Import latex2sympy for LaTeX parsing
try:
    from latex2sympy2 import latex2sympy
except ImportError:
    latex2sympy = None

def parse_latex_integral(latex_expr):
    """Parse LaTeX integral expressions and extract the integrand using latex2sympy"""
    if not latex_expr or not latex_expr.strip():
        return ""
    
    print(f"DEBUG: parse_latex_integral input: '{latex_expr}'")
    
    # Clean the expression
    clean_expr = latex_expr.strip()
    if clean_expr.startswith('$$') and clean_expr.endswith('$$'):
        clean_expr = clean_expr[2:-2].strip()
    elif clean_expr.startswith('$') and clean_expr.endswith('$'):
        clean_expr = clean_expr[1:-1].strip()
    
    print(f"DEBUG: Cleaned expression: '{clean_expr}'")
    
    if not latex2sympy:
        print("DEBUG: latex2sympy not available, using fallback")
        return _fallback_latex_parse(clean_expr)
    
    try:
        # Use latex2sympy to parse the entire LaTeX expression
        parsed = latex2sympy(clean_expr)
        print(f"DEBUG: latex2sympy result: '{parsed}' (type: {type(parsed).__name__})")
        
        # Check if it's an Integral object
        if isinstance(parsed, Integral):
            print("DEBUG: Found Integral object, extracting integrand")
            integrand = parsed.function
            limits = parsed.limits  # [(x, a, b), ...]
            
            print(f"DEBUG: Integrand: {integrand}")
            print(f"DEBUG: Integrand type: {type(integrand)}")
            print(f"DEBUG: Integrand free symbols: {integrand.free_symbols}")
            print(f"DEBUG: Limits: {limits}")
            
            # Return just the integrand as a string for solve_multiple_integral
            result_str = str(integrand)
            print(f"DEBUG: Final integrand string: '{result_str}'")
            
            # If the integrand is something like xy (single symbol), try to interpret it as x*y
            if result_str == 'xy' and len(integrand.free_symbols) == 1:
                print("DEBUG: Converting 'xy' single symbol to 'x*y' multiplication")
                result_str = 'x*y'
            elif result_str == 'xyz' and len(integrand.free_symbols) == 1:
                print("DEBUG: Converting 'xyz' single symbol to 'x*y*z' multiplication")
                result_str = 'x*y*z'
            
            print(f"DEBUG: Extracted integrand: '{result_str}'")
            return result_str
        else:
            # Not an integral, return as-is
            result_str = str(parsed)
            print(f"DEBUG: Not an integral, returning: '{result_str}'")
            return result_str
        
    except Exception as e:
        print(f"DEBUG: latex2sympy failed: {e}")
        return _fallback_latex_parse(clean_expr)

def parse_latex_integral_with_limits(latex_expr):
    """Parse LaTeX integral expressions and return both integrand and limits"""
    if not latex_expr or not latex_expr.strip():
        return "", []
    
    print(f"DEBUG: parse_latex_integral_with_limits input: '{latex_expr}'")
    
    # Clean the expression
    clean_expr = latex_expr.strip()
    if clean_expr.startswith('$$') and clean_expr.endswith('$$'):
        clean_expr = clean_expr[2:-2].strip()
    elif clean_expr.startswith('$') and clean_expr.endswith('$'):
        clean_expr = clean_expr[1:-1].strip()
    
    if not latex2sympy:
        print("DEBUG: latex2sympy not available for limits extraction")
        return parse_latex_integral(latex_expr), []
    
    try:
        # Use latex2sympy to parse the entire LaTeX expression
        parsed = latex2sympy(clean_expr)
        print(f"DEBUG: latex2sympy result: '{parsed}' (type: {type(parsed).__name__})")
        
        # Check if it's an Integral object
        if isinstance(parsed, Integral):
            integrand = parsed.function
            limits = parsed.limits  # [(x, a, b), ...]
            
            print(f"DEBUG: Integrand: {integrand}")
            print(f"DEBUG: Raw limits: {limits}")
            
            # Convert limits to the format expected by solve_multiple_integral
            vars_limits = []
            for limit_tuple in limits:
                if len(limit_tuple) == 3:
                    var, lower, upper = limit_tuple
                    vars_limits.append((str(var), str(lower), str(upper)))
                else:
                    var = limit_tuple[0]
                    vars_limits.append((str(var), "0", "1"))  # Default limits
            
            print(f"DEBUG: Formatted limits: {vars_limits}")
            
            return str(integrand), vars_limits
        else:
            return str(parsed), []
        
    except Exception as e:
        print(f"DEBUG: latex2sympy failed for limits extraction: {e}")
        return parse_latex_integral(latex_expr), []

def _fallback_latex_parse(latex_expr):
    """Fallback LaTeX parsing when latex2sympy is not available"""
    import re
    
    # For integral expressions, extract the integrand
    if '\\int' in latex_expr:
        # First, handle LaTeX delimiter commands
        temp_expr = latex_expr
        
        # Remove \left and \right commands (they're just for sizing delimiters)
        temp_expr = re.sub(r'\\left[\(\[\{]', '(', temp_expr)
        temp_expr = re.sub(r'\\right[\)\]\}]', ')', temp_expr)
        temp_expr = temp_expr.replace('\\left', '').replace('\\right', '')
        
        # Handle other common LaTeX commands
        temp_expr = temp_expr.replace('\\cdot', '*')
        temp_expr = temp_expr.replace('\\times', '*')
        temp_expr = temp_expr.replace('\\,', ' ')  # thin space
        temp_expr = temp_expr.replace('\\ ', ' ')  # regular space
        
        # Remove integral symbols and limits
        temp_expr = re.sub(r'\\int[_\^{}\d\w\s]*', '', temp_expr)
        
        # Remove differentials (dx, dy, dz) - be more careful about backslashes
        temp_expr = re.sub(r'\\,?\s*d[xyz]', '', temp_expr)
        temp_expr = re.sub(r'd[xyz]', '', temp_expr)
        
        # Clean up extra spaces and strip
        temp_expr = re.sub(r'\s+', ' ', temp_expr).strip()
        
        # Remove outer parentheses if they wrap the entire expression
        if temp_expr.startswith('(') and temp_expr.endswith(')'):
            temp_expr = temp_expr[1:-1].strip()
        
        # Handle common patterns like 'xy' -> 'x*y', 'xyz' -> 'x*y*z'
        if temp_expr == 'xy':
            temp_expr = 'x*y'
        elif temp_expr == 'xyz':
            temp_expr = 'x*y*z'
        elif temp_expr == 'xz':
            temp_expr = 'x*z'
        elif temp_expr == 'yz':
            temp_expr = 'y*z'
        elif temp_expr == '1':
            temp_expr = '1'  # Keep constants as-is
        elif not temp_expr:
            temp_expr = 'x*y'  # Default fallback
        
        print(f"DEBUG _fallback_latex_parse: '{latex_expr}' -> '{temp_expr}'")
        return temp_expr
    
    return latex_expr

def parse_single_expression(expr_str):
    """Parse a single mathematical expression - SIMPLE version for general use"""
    if not expr_str or not expr_str.strip():
        return ""
    
    expr_str = expr_str.strip()
    
    # Very basic parsing - only handle essential conversions
    cleaned_expr = expr_str.replace('^', '**')  # Convert powers
    
    return cleaned_expr

def parse_latex_expression(expr_str):
    """Parse LaTeX expressions with full LaTeX command handling - for non-integral LaTeX"""
    if not expr_str or not expr_str.strip():
        return ""
    
    expr_str = expr_str.strip()
    
    # Handle LaTeX commands that might appear in general expressions
    cleaned_expr = expr_str
    
    # Handle LaTeX delimiter commands
    import re
    cleaned_expr = re.sub(r'\\left[\(\[\{]', '(', cleaned_expr)
    cleaned_expr = re.sub(r'\\right[\)\]\}]', ')', cleaned_expr)
    cleaned_expr = cleaned_expr.replace('\\left', '').replace('\\right', '')
    
    # Handle LaTeX mathematical symbols
    cleaned_expr = cleaned_expr.replace('\\cdot', '*')
    cleaned_expr = cleaned_expr.replace('\\times', '*')
    cleaned_expr = cleaned_expr.replace('\\,', '')  # Remove thin spaces
    cleaned_expr = cleaned_expr.replace('\\ ', ' ')  # Handle regular spaces
    
    # Handle LaTeX functions - IMPORTANT: Add * before functions when needed
    cleaned_expr = re.sub(r'([a-zA-Z0-9)])\\sin', r'\1*sin', cleaned_expr)  # y\sin -> y*sin
    cleaned_expr = re.sub(r'([a-zA-Z0-9)])\\cos', r'\1*cos', cleaned_expr)  # y\cos -> y*cos
    cleaned_expr = re.sub(r'([a-zA-Z0-9)])\\tan', r'\1*tan', cleaned_expr)  # y\tan -> y*tan
    
    # Now replace the LaTeX function commands
    cleaned_expr = cleaned_expr.replace('\\sin', 'sin')
    cleaned_expr = cleaned_expr.replace('\\cos', 'cos')
    cleaned_expr = cleaned_expr.replace('\\tan', 'tan')
    cleaned_expr = cleaned_expr.replace('\\ln', 'log')
    cleaned_expr = cleaned_expr.replace('\\log', 'log')
    cleaned_expr = cleaned_expr.replace('\\pi', 'pi')
    cleaned_expr = cleaned_expr.replace('\\e', 'E')
    
    # Convert ^ to ** for powers
    cleaned_expr = cleaned_expr.replace('^', '**')
    
    # Clean up any remaining backslashes that might cause issues
    cleaned_expr = re.sub(r'\\([a-zA-Z]+)', r'\1', cleaned_expr)  # Remove backslashes from remaining commands
    
    # Handle implicit multiplication for common variable patterns
    # This handles cases like sin(xy) -> sin(x*y), cos(xyz) -> cos(x*y*z), etc.
    cleaned_expr = re.sub(r'\b(xy)\b', 'x*y', cleaned_expr)  # xy -> x*y
    cleaned_expr = re.sub(r'\b(xyz)\b', 'x*y*z', cleaned_expr)  # xyz -> x*y*z
    cleaned_expr = re.sub(r'\b(xz)\b', 'x*z', cleaned_expr)  # xz -> x*z
    cleaned_expr = re.sub(r'\b(yz)\b', 'y*z', cleaned_expr)  # yz -> y*z
    
    return cleaned_expr

def parse_parametric_functions(param_str):
    """Parse parametric functions by splitting on commas"""
    if not param_str:
        return []
    
    # Remove outer brackets if present
    param_str = param_str.strip()
    if param_str.startswith('[') and param_str.endswith(']'):
        param_str = param_str[1:-1]
    
    # Split by comma and parse each component
    components = [comp.strip() for comp in param_str.split(',') if comp.strip()]
    parsed_components = []
    
    for comp in components:
        parsed_expr = parse_single_expression(comp)
        parsed_components.append(parsed_expr)
    
    return parsed_components

def parse_vector_input(vector_str):
    """Parse vector input by splitting on commas"""
    if not vector_str:
        return []
    
    # Remove outer brackets if present
    vector_str = vector_str.strip()
    if vector_str.startswith('[') and vector_str.endswith(']'):
        vector_str = vector_str[1:-1]
    
    # Split by comma and parse each component
    components = [comp.strip() for comp in vector_str.split(',') if comp.strip()]
    parsed_components = []
    
    for comp in components:
        parsed_expr = parse_single_expression(comp)
        parsed_components.append(parsed_expr)
    
    return parsed_components

def analyze_expression(latex_expr):
    """Analyze expressions - simplified"""
    return {"type": "raw_expression", "expression": latex_expr}
