from sympy import sympify, symbols, latex
from sympy.parsing.latex import parse_latex
import re

def preprocess_constraint(constraint_str):
    """
    Convert constraint equations like 'x+y = 1' to expressions like 'x+y-1'
    """
    if not constraint_str or '=' not in constraint_str:
        return constraint_str
    
    # Split by '=' and convert to expression form
    parts = constraint_str.split('=')
    if len(parts) == 2:
        left_side = parts[0].strip()
        right_side = parts[1].strip()
        
        # Convert 'left = right' to 'left - right' 
        # Handle cases where right side is 0
        if right_side == '0':
            return left_side
        else:
            return f"({left_side}) - ({right_side})"
    
    return constraint_str

def extract_variables_from_string(expr_str):
    """Extract variable names from mathematical expressions using regex"""
    if not expr_str:
        return set()
        
    # Clean up LaTeX and common symbols
    cleaned = expr_str.replace('\\', '').replace('{', '').replace('}', '')
    cleaned = cleaned.replace('sin', '').replace('cos', '').replace('tan', '')
    cleaned = cleaned.replace('sec', '').replace('csc', '').replace('cot', '')
    cleaned = cleaned.replace('log', '').replace('ln', '').replace('exp', '')
    cleaned = cleaned.replace('sqrt', '').replace('pi', '').replace('frac', '')
    
    # Find single letters that could be variables (excluding numbers and operators)
    variables = set()
    for match in re.finditer(r'\b[a-zA-Z]\b', cleaned):
        var = match.group()
        # Exclude common constants and functions
        if var not in {'e', 'E', 'i', 'I', 'o', 'O'}:
            variables.add(var)
    
    return variables
def clean_power_formatting(expr_str):
    """
    Clean up power formatting issues where SymPy returns powers with braces.
    Converts expressions like x^{10} to x^10 and e^{x} to e^x
    """
    if not expr_str:
        return expr_str
    
    expr_str = str(expr_str)  # Ensure it's a string
    
    # Fix SymPy's ** notation back to ^ for display
    expr_str = expr_str.replace('**', '^')
    
    # Remove unnecessary braces from simple powers
    # x^{10} -> x^10, e^{2} -> e^2
    expr_str = re.sub(r'\^{(\d+)}', r'^\1', expr_str)
    
    # Remove unnecessary braces from single variable powers
    # e^{x} -> e^x, sin^{t} -> sin^t
    expr_str = re.sub(r'\^{([a-zA-Z])}', r'^\1', expr_str)
    
    # For complex expressions, keep parentheses instead of braces
    # e^{x*y} -> e^(x*y), log^{x+1} -> log^(x+1)
    expr_str = re.sub(r'\^{([^}]+)}', r'^(\1)', expr_str)
    
    return expr_str

def parse_expression(expr):
    """
    Parse any mathematical expression (LaTeX or regular) using SymPy.
    Returns a cleaned string representation of the SymPy expression.
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
                # Preprocess LaTeX to fix common formatting issues
                expr = preprocess_latex(expr)
                parsed_expr = parse_latex(expr)
                return clean_power_formatting(parsed_expr)
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
                parsed_expr = sympify(expr)
                return clean_power_formatting(parsed_expr)
        else:
            # Handle common patterns and use sympify
            expr = expr.replace('^', '**')  # Convert powers
            parsed_expr = sympify(expr)
            return clean_power_formatting(parsed_expr)
    except:
        try:
            # Fallback: try sympify with power conversion
            expr = expr.replace('^', '**')
            parsed_expr = sympify(expr)
            return clean_power_formatting(parsed_expr)
        except:
            # Last resort: return as symbol with cleanup
            result = symbols(expr)
            return clean_power_formatting(result)

def preprocess_latex(latex_expr):
    """
    Preprocess LaTeX expressions to fix common formatting issues before parsing.
    """
    if not latex_expr:
        return latex_expr
    
    # Fix square root without braces: \sqrt2 -> \sqrt{2}
    latex_expr = re.sub(r'\\sqrt(\d+)', r'\\sqrt{\1}', latex_expr)
    
    # Fix square root with variables without braces: \sqrtx -> \sqrt{x}
    latex_expr = re.sub(r'\\sqrt([a-zA-Z])', r'\\sqrt{\1}', latex_expr)
    
    # Fix other functions without braces like \sin2 -> \sin{2}, \cos3 -> \cos{3}
    latex_expr = re.sub(r'\\(sin|cos|tan|sec|csc|cot|log|ln|exp)(\d+)', r'\\\1{\2}', latex_expr)
    
    # Fix function with variables without braces: \sinx -> \sin{x}
    latex_expr = re.sub(r'\\(sin|cos|tan|sec|csc|cot|log|ln|exp)([a-zA-Z])', r'\\\1{\2}', latex_expr)
    
    return latex_expr

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
    
    # Preprocess LaTeX to fix common formatting issues
    latex_expr = preprocess_latex(latex_expr)
    
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
            # The parse_expression already applies clean_power_formatting
            components.append(parsed if parsed else comp)
    
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

def format_expression_output(expr):
    """
    Global function to format any expression output with proper power notation.
    Can be used by calc3.py or other modules for consistent formatting.
    """
    if expr is None:
        return None
    return clean_power_formatting(str(expr))
