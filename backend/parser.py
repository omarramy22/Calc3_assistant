from sympy.parsing.latex import parse_latex
from latex2sympy2_extended import latex2sympy
from sympy import Derivative, Integral, symbols, SympifyError, Matrix, sympify
from sympy.core.basic import Basic
import re

def extract_all_derivatives(expr):
    derivatives = []
    if isinstance(expr, Derivative):
        derivatives.append(expr)
    elif isinstance(expr, Basic):
        for arg in expr.args:
            derivatives.extend(extract_all_derivatives(arg))
    return derivatives
def analyze_expression(latex_expr):
    try:
        if "\\htmlClass{arc}" in latex_expr:
            match = re.search(r'\\htmlClass\{arc\}\{(.+)\}', latex_expr)
            content = match.group(1)
            
            expr = latex2sympy(content)

            if not isinstance(expr, Integral):
               return {"error": "Expected an integral expression"}

            # Search recursively for Derivative nodes and collect their arguments
            derivatives = extract_all_derivatives(expr)
            inner_functions = []
            for d in derivatives:
                try:
                    inner_functions.append(sympify(d.expr))
                except Exception as e:
                    return {"error": f"Failed to parse derivative expression: {str(e)}"}
            limit = expr.limits[0]
            param = limit[0]  # e.g., t
            a = limit[1]
            b = limit[2]
            return {
                "type": "arc_length",
                "expression": inner_functions,
                "param": param,     # e.g., t
                "limits": [a, b]
            }
        elif "\\htmlClass{directional}" in latex_expr:
            match = re.search(r'\\htmlClass\{directional\}\{(.+)\}', latex_expr)
            content = match.group(1)
            content = content.replace("\\nabla", "").strip()
            parts = content.split("\\cdot")
    
            if len(parts) != 2:
                return {"error": "Could not split into function and direction"}
            try:
                func_expr = latex2sympy(parts[0].strip())
                dir_expr = latex2sympy(parts[1].strip())
            except Exception as e:
                return {"error": f"Failed to parse parts: {str(e)}"}
            vars = list(func_expr.free_symbols)
            return{
                "type" : "directional_derivative",
                "expression" : str(func_expr),
                "variables"  : [str(v) for v in vars],
                "direction"  : [str(d) for d in dir_expr]
            }
            
        elif "\\htmlClass{gradient}" in latex_expr:
            match = re.search(r'\\htmlClass\{gradient\}\{(.+)\}', latex_expr)
            content = match.group(1)
            content = content.replace("\\nabla", "").strip()
            try:
                func_expr = latex2sympy(content)
            except Exception as e:
                return {"error": f"Failed to parse content: {str(e)}"}
            vars = list(func_expr.free_symbols)
            return{
                "type" : "gradient",
                "expression" : str(func_expr),
                "variables"  : [str(v) for v in vars],
            }           
        
        parsed = latex2sympy(latex_expr)
        # Check for Partial Derivative
        if isinstance(parsed, Derivative):
            base_expr = parsed.expr
            vars_orders = parsed.variable_count
            variables = [str(v[0]) for v in vars_orders]
            orders = [v[1] for v in vars_orders]

            return {
                "type": "partial_derivative",
                "expression": str(base_expr),
                "variables": variables,
                "orders": orders
            }

        # Check for Integral
        if isinstance(parsed, Integral):
            integrand = parsed.function
            limits = parsed.limits  # [(x, a, b), ...]
            vars_limits = [(str(v[0]), v[1], v[2]) if len(v) == 3 else (str(v[0]), None, None) for v in limits]

            return {
                "type": "multiple_integral",
                "expression": str(integrand),
                "limits": vars_limits
            }

        # Add more recognitions like Curl, Gradient etc if needed later
        return {
            "type": "raw_expression",
            "expression": str(parsed)
        }

    except Exception as e:
        return {
            "type": "error",
            "message": str(e)
        }
