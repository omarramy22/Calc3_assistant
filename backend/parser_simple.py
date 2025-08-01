from sympy import sympify, symbols

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
