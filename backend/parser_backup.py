from sympy.parsing.latex import parse_latex
from sympy import Integral, symbols, sympify
import re

# Import latex2sympy for better LaTeX to SymPy conversion
try:
    from latex2sympy2 import latex2sympy
    HAS_LATEX2SYMPY = True
except ImportError:
    HAS_LATEX2SYMPY = False

def parse_single_expression(expr_str):
    """Parse a single mathematical expression - simplified approach"""
    if not expr_str or not expr_str.strip():
        return ""
    
    expr_str = expr_str.strip()
    
    # Simple direct approach - just convert ^ to ** and return
    # This fixes the x^2 -> x issue
    cleaned_expr = expr_str.replace('^', '**')
    
    # Handle basic LaTeX functions
    cleaned_expr = cleaned_expr.replace('\\sin', 'sin')
    cleaned_expr = cleaned_expr.replace('\\cos', 'cos')
    cleaned_expr = cleaned_expr.replace('\\tan', 'tan')
    cleaned_expr = cleaned_expr.replace('\\ln', 'log')
    cleaned_expr = cleaned_expr.replace('\\pi', 'pi')
    
    if not cleaned_expr:
            raise ValueError("LaTeX parser misinterpreted sin function")
            
        if ('cos(' in expr_str.lower() and 
            ('c*' in result_str and '*s(' in result_str and 'o' in result_str)):
            raise ValueError("LaTeX parser misinterpreted cos function")
            
        if ('tan(' in expr_str.lower() and 
            ('t*' in result_str and '*n(' in result_str and 'a' in result_str)):
            raise ValueError("LaTeX parser misinterpreted tan function")
        
        return str(result)
    except Exception as e:
        pass
    
    # Method 3: Direct SymPy parsing with comprehensive symbol/function context
    try:
        # Import all common math functions and symbols
        from sympy import (sin, cos, tan, cot, sec, csc, sinh, cosh, tanh, 
                          log, ln, exp, sqrt, pi, E, I, oo, 
                          asin, acos, atan, symbols)
        
        # Define comprehensive symbol set
        t, u, v, s, a, b, c = symbols('t u v s a b c')
        x, y, z = symbols('x y z')
        r, theta, phi = symbols('r theta phi')
        
        # Better LaTeX cleaning for direct sympify
        cleaned_expr = expr_str
        
        # Convert LaTeX patterns to SymPy-compatible format
        if '\\sin\\left(' in cleaned_expr:
            cleaned_expr = cleaned_expr.replace('\\sin\\left(', 'sin(').replace('\\right)', ')')
        if '\\cos\\left(' in cleaned_expr:
            cleaned_expr = cleaned_expr.replace('\\cos\\left(', 'cos(').replace('\\right)', ')')
        if '\\tan\\left(' in cleaned_expr:
            cleaned_expr = cleaned_expr.replace('\\tan\\left(', 'tan(').replace('\\right)', ')')
        if '\\log\\left(' in cleaned_expr:
            cleaned_expr = cleaned_expr.replace('\\log\\left(', 'log(').replace('\\right)', ')')
        if '\\sqrt{' in cleaned_expr:
            cleaned_expr = cleaned_expr.replace('\\sqrt{', 'sqrt(').replace('}', ')')
        if '\\frac{' in cleaned_expr:
            # Simple fraction handling: \frac{a}{b} -> (a)/(b)
            import re
            frac_pattern = r'\\frac\{([^{}]+)\}\{([^{}]+)\}'
            cleaned_expr = re.sub(frac_pattern, r'(\1)/(\2)', cleaned_expr)
        
        # Convert ^ to ** for powers
        cleaned_expr = cleaned_expr.replace('^', '**')
        # Convert pi symbol
        cleaned_expr = cleaned_expr.replace('\\pi', 'pi')
        
        # Parse with comprehensive context
        result = sympify(cleaned_expr, locals={
            # Variables
            't': t, 'u': u, 'v': v, 's': s, 'a': a, 'b': b, 'c': c,
            'x': x, 'y': y, 'z': z, 'r': r, 'theta': theta, 'phi': phi,
            # Trig functions
            'sin': sin, 'cos': cos, 'tan': tan, 'cot': cot, 'sec': sec, 'csc': csc,
            'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
            'asin': asin, 'acos': acos, 'atan': atan,
            # Other functions
            'log': log, 'ln': ln, 'exp': exp, 'sqrt': sqrt,
            # Constants
            'pi': pi, 'e': E, 'i': I, 'oo': oo
        })
        print(f"Direct sympify success: '{expr_str}' -> '{result}'")
        return str(result)
        
    except Exception as e:
        print(f"Direct sympify failed for '{expr_str}': {e}")
    
    # Method 4: Return cleaned string as absolute fallback
    cleaned = expr_str.replace('^', '**').replace('π', 'pi').replace('\\pi', 'pi')
    # Handle basic LaTeX cleanup for fallback
    if '\\sin\\left(' in cleaned:
        cleaned = cleaned.replace('\\sin\\left(', 'sin(').replace('\\right)', ')')
    if '\\cos\\left(' in cleaned:
        cleaned = cleaned.replace('\\cos\\left(', 'cos(').replace('\\right)', ')')
    if '\\tan\\left(' in cleaned:
        cleaned = cleaned.replace('\\tan\\left(', 'tan(').replace('\\right)', ')')
    
    # Handle simple function names without LaTeX formatting
    # This is important for cases like 'sin(t)' that might be parsed incorrectly
    if cleaned != expr_str:  # Only if we made changes
        print(f"Using fallback: '{expr_str}' -> '{cleaned}'")
    else:
        print(f"Using fallback (no changes): '{expr_str}'")
    
    return cleaned

def parse_parametric_functions(param_str):
    """Parse parametric functions by splitting on commas and using latex2sympy for each part"""
    if not param_str:
        return []
    
    print(f"Parsing parametric string: '{param_str}'")
    
    # Remove outer brackets if present
    param_str = param_str.strip()
    if param_str.startswith('[') and param_str.endswith(']'):
        param_str = param_str[1:-1]
    
    # Split by comma
    components = [comp.strip() for comp in param_str.split(',') if comp.strip()]
    print(f"Split into components: {components}")
    
    # Parse each component using latex2sympy as primary method
    parsed_components = []
    for i, comp in enumerate(components):
        if not comp:
            continue
            
        parsed_expr = parse_single_expression(comp)
        parsed_components.append(parsed_expr)
        print(f"Component {i}: '{comp}' -> '{parsed_expr}'")
    
    print(f"Final parsed components: {parsed_components}")
    return parsed_components

def parse_vector_input(vector_str):
    """Parse vector input by splitting on commas and using latex2sympy for each part"""
    if not vector_str:
        return []
    
    print(f"Parsing vector string: '{vector_str}'")
    
    # Remove outer brackets if present
    vector_str = vector_str.strip()
    if vector_str.startswith('[') and vector_str.endswith(']'):
        vector_str = vector_str[1:-1]
    
    # Split by comma
    components = [comp.strip() for comp in vector_str.split(',') if comp.strip()]
    
    # Parse each component using latex2sympy as primary method
    parsed_components = []
    for comp in components:
        if not comp:
            continue
            
        parsed_expr = parse_single_expression(comp)
        parsed_components.append(parsed_expr)
    
    print(f"Parsed vector components: {parsed_components}")
    return parsed_components

def analyze_expression(latex_expr):
    """Analyze LaTeX expressions for integral operations"""
    try:
        # Handle multiple integral expressions
        if "\\int_" in latex_expr:
            return parse_integral_expression(latex_expr)
        else:
            return {"type": "raw_expression", "expression": latex_expr}
    except Exception as e:
        return {"error": f"Failed to parse expression: {str(e)}"}

def parse_integral_expression(latex_expr):
    """Parse integral expressions using latex2sympy as primary method, then SymPy's LaTeX parser"""
    print(f"Parsing integral: {latex_expr}")
    
    # Method 1: Try latex2sympy first (PRIMARY METHOD)
    if HAS_LATEX2SYMPY:
        try:
            result = latex2sympy(latex_expr)
            print(f"latex2sympy parsed integral: {result} (type: {type(result)})")
            
            # Check if it's an Integral object
            if isinstance(result, Integral):
                return _extract_integral_info(result)
            # If it has Integral objects within it
            elif hasattr(result, 'atoms'):
                integrals = result.atoms(Integral)
                if integrals:
                    integral = list(integrals)[0]
                    return _extract_integral_info(integral)
                    
        except Exception as e:
            print(f"latex2sympy failed for integral '{latex_expr}': {e}")
    
    # Method 2: Try SymPy's LaTeX parser
    try:
        # Clean up the LaTeX expression for better parsing
        cleaned_expr = latex_expr.replace('\\,', ' ')  # Remove LaTeX spacing commands
        cleaned_expr = cleaned_expr.replace('^{}', '')  # Remove empty power braces
        
        # Use SymPy's LaTeX parser
        parsed_expr = parse_latex(cleaned_expr)
        print(f"SymPy parsed integral: {parsed_expr} (type: {type(parsed_expr)})")
        
        # Check if it's an Integral object
        if isinstance(parsed_expr, Integral):
            return _extract_integral_info(parsed_expr)
        # If it has Integral objects within it
        elif hasattr(parsed_expr, 'atoms'):
            integrals = parsed_expr.atoms(Integral)
            if integrals:
                integral = list(integrals)[0]
                return _extract_integral_info(integral)
        
    except Exception as e:
        print(f"SymPy LaTeX parser failed: {str(e)}")
    
    # Method 3: Return error if both methods fail
    return {"error": f"Could not parse integral expression: {latex_expr}"}

def _extract_integral_info(integral):
    """Extract information from a SymPy Integral object"""
    # Extract the integrand (the function being integrated)
    integrand = integral.function
    print(f"Integrand: {integrand}")
    
    # Extract the limits of integration
    limits = []
    for limit_tuple in integral.limits:
        if len(limit_tuple) == 3:  # (variable, lower, upper)
            var, lower, upper = limit_tuple
            var_name = str(var)  # Convert symbol to string
            limits.append((var_name, lower, upper))
            print(f"Limit: {var_name} from {lower} to {upper}")
        elif len(limit_tuple) == 1:  # Just variable, no limits
            var = limit_tuple[0]
            var_name = str(var)
            limits.append((var_name, 0, 1))  # Default limits
            print(f"Variable with default limits: {var_name}")
    
    # Count integrals
    integral_count = len(limits)
    
    return {
        "type": f"{'triple' if integral_count >= 3 else 'double'}_integral",
        "expression": str(integrand),
        "limits": limits,
        "variables": [limit[0] for limit in limits]
    }


