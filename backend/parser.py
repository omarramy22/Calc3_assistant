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
        elif "\\htmlClass{lagrange}" in latex_expr:
            match = re.search(r'\\htmlClass\{lagrange\}\{(.+)\}', latex_expr)
            content = match.group(1)
            content = content.replace("\\nabla", "").strip()
            content = content.replace("\\lambda", "").strip()
            try:
                grad_eqn, constraint_eqn = content.split(',')
            except ValueError:
                return {"error": "Expected two comma-separated expressions."}
            parts = grad_eqn.split("=")
            parts2 =  constraint_eqn.split("=")
            
            
            if len(parts) != 2:
                return {"error": "Could not split into function and constraint"}
            if len(parts2) != 2:
                return {"error": "Could not split into constraint and value"}
            
            
            try:
                func_expr = latex2sympy(parts[0].strip())
                constraint_expr_right = latex2sympy(parts[1].strip())
                constraint_expr_left = latex2sympy(parts2[0].strip())
            except Exception as e:
                return {"error": f"Failed to parse parts: {str(e)}"}
            if constraint_expr_left != constraint_expr_right:
                return {"error": "Constraint expressions do not match."}
            vars = list(func_expr.free_symbols)
            return{
                "type" : "lagrange_multipliers",
                "function" : str(func_expr),
                "constraint" : str(constraint_expr_right),
                "variables"  : [str(v) for v in vars],
            }
        elif "htmlClass{scalar_line_integral}" in latex_expr:
            match = re.search(r'\\htmlClass\{scalar_line_integral\}\{(.+)\}', latex_expr)
            content = match.group(1)
            parts = content.split(",", maxsplit=2)
            parts1 = parts[0] + ',' + parts[1]
            if len(parts) != 3:
                return {"error": "Could not split into function and direction"}
            try:
                func_expr = latex2sympy(parts1.strip())
                integrand = func_expr.function
                a = func_expr.limits[0][1]  # Lower limit
                b = func_expr.limits[0][2]  # Upper limit
                parts2 = parts[2].strip().split("=")
                if len(parts2) != 2:
                    return {"error": "Could not split into parameter and curve"}
                dir_expr = latex2sympy(parts2[1].strip())
                param = dir_expr.free_symbols
                param = [str(p) for p in param]
                if len(param) != 1:
                    return {"error": "Expected exactly one parameter for the curve."}
            except Exception as e:
                return {"error": f"Failed to parse parts: {str(e)}"}
            
            return{
                "type" : "scalar_line_integral",
                "field" : str(integrand),
                "param"  : param[0],
                "curve"  : [str(d) for d in dir_expr],
                "bounds": [a, b] 
            }
            
        elif "htmlClass{vector_line_integral}" in latex_expr:

            match = re.search(r'\\htmlClass\{vector_line_integral\}\{(.+)\}', latex_expr)
            content = match.group(1)
            parts = content.split(",", maxsplit=4)
            if len(parts) != 5:
                return {"error": "Could not split into function and direction"}
            
            integral_raw = parts[0] + ',' + parts[1] + ',' + parts[2] + ',' + parts[3]
            if "\\cdot" in integral_raw:
                integrand_vec, rest = integral_raw.split("\\cdot")
                cleaned_integral = integrand_vec.strip() + "\\, dt"
            try:
                vec_expr = latex2sympy(cleaned_integral.strip())
                print(f"Parsed vector expression: {vec_expr}")
                integrand = vec_expr.function
                a = vec_expr.limits[0][1]  # Lower limit
                b = vec_expr.limits[0][2]  # Upper limit
                parts2 = parts[2].strip().split("=")
                if len(parts2) != 2:
                    return {"error": "Could not split into parameter and curve"}
                
                dir_expr = latex2sympy(parts2[1].strip())
                param = dir_expr.free_symbols
                param = [str(p) for p in param]
                if len(param) != 1:
                    return {"error": "Expected exactly one parameter for the curve."}
            except Exception as e:
                return {"error": f"Failed to parse parts: {str(e)}"}
            
            return{
                "type" : "vector_line_integral",
                "field" : integrand,
                "param"  : param[0],
                "curve"  : [str(d) for d in dir_expr],
                "bounds": [a, b] 
            }
            
        parsed = latex2sympy(latex_expr)
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
