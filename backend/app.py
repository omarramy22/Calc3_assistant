from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy.parsing.latex import parse_latex
from sympy import sympify, symbols

# Import latex2sympy for better LaTeX to SymPy conversion
try:
    from latex2sympy2 import latex2sympy
except ImportError:
    latex2sympy = None

from calc3 import (
    solve_partial_derivative,
    solve_multiple_integral,
    solve_arc_length,
    solve_gradient,
    solve_divergence,
    solve_curl,
    solve_line_integral,
    solve_surface_integral,
    solve_directional_derivative,
    solve_greens_theorem,
    solve_stokes_theorem,
    solve_lagrange_multipliers
)

from parser import (
    analyze_expression,
    parse_vector_input,
    parse_parametric_functions,
    parse_single_expression,
    parse_latex_expression,
    parse_latex_integral,
    parse_latex_integral_with_limits
)

app = Flask(__name__)
CORS(app)

def safe_sympify(expr_str):
    """Safely convert string to SymPy expression with proper LaTeX parsing"""
    if not expr_str or expr_str.strip() == '':
        return None
    
    try:
        # First try direct sympify with basic conversion
        expr_clean = expr_str.replace('^', '**')
        return sympify(expr_clean)
    except Exception as e:
        print(f"Direct sympify failed for '{expr_str}': {e}")
        # Try LaTeX parser if the expression contains LaTeX commands
        try:
            if '\\' in expr_str:  # Contains LaTeX commands
                parsed = parse_latex_expression(expr_str)
                print(f"LaTeX parsing: '{expr_str}' -> '{parsed}'")
            else:
                parsed = parse_single_expression(expr_str)
                print(f"Simple parsing: '{expr_str}' -> '{parsed}'")
            
            # Make sure the parsed result is valid before sympifying
            if parsed and parsed.strip():
                return sympify(parsed)
            else:
                raise ValueError(f"Parser returned empty result for '{expr_str}'")
                
        except Exception as e2:
            print(f"Parser also failed for '{expr_str}': {e2}")
            # Instead of trying sympify again with the original string,
            # return a symbol with a safe name or raise the error
            raise ValueError(f"Could not parse expression: {expr_str}")

def parse_limits(limits_str):
    """Parse limits in user-friendly formats like '0, 1' or '0to1' or '0 to 1'"""
    if not limits_str:
        return [0, 1]  # Default limits
    
    limits_str = limits_str.strip()
    
    # Handle comma-separated format: "0, 1"
    if ',' in limits_str:
        parts = limits_str.split(',')
        if len(parts) == 2:
            try:
                return [sympify(parts[0].strip()), sympify(parts[1].strip())]
            except:
                return [0, 1]
    
    # Handle "to" format: "0to1" or "0 to 1"  
    if 'to' in limits_str.lower():
        parts = limits_str.lower().split('to')
        if len(parts) == 2:
            try:
                return [sympify(parts[0].strip()), sympify(parts[1].strip())]
            except:
                return [0, 1]
    
    # Handle space-separated format: "0 1"
    parts = limits_str.split()
    if len(parts) == 2:
        try:
            return [sympify(parts[0]), sympify(parts[1])]
        except:
            return [0, 1]
    
    # Default fallback
    return [0, 1]

def parse_parameter_limits(limits_str):
    """Parse parameter limits for compatibility"""
    return parse_limits(limits_str)

def convert_latex_to_expression(latex_expr):
    """Convert LaTeX expression to a standard mathematical expression using latex2sympy"""
    if not latex_expr or not latex_expr.strip():
        return ""
    
    # Clean the expression
    clean_expr = latex_expr.strip()
    if clean_expr.startswith('$$') and clean_expr.endswith('$$'):
        clean_expr = clean_expr[2:-2].strip()
    elif clean_expr.startswith('$') and clean_expr.endswith('$'):
        clean_expr = clean_expr[1:-1].strip()
    
    print(f"DEBUG: Input LaTeX: '{latex_expr}'")
    print(f"DEBUG: Cleaned LaTeX: '{clean_expr}'")
    
    # For integral expressions, we need to extract just the integrand
    if '\\int' in clean_expr:
        # Use regex to extract the integrand from LaTeX integral
        import re
        
        # Handle common patterns: \int_a^b\int_c^d f(x,y) dx dy
        # Look for content after integral symbols but before dx, dy, dz
        
        # Remove integral symbols and limits first
        temp_expr = re.sub(r'\\int[_\^{}\d\w\s]*', '', clean_expr)
        print(f"DEBUG: After removing \\int: '{temp_expr}'")
        
        # Remove differential elements (dx, dy, dz, etc.)
        temp_expr = re.sub(r'\\,?d[xyz]', '', temp_expr)
        print(f"DEBUG: After removing dx,dy,dz: '{temp_expr}'")
        
        # Handle \cdot and other LaTeX symbols
        temp_expr = temp_expr.replace('\\cdot', '*')
        temp_expr = temp_expr.replace('\\,', '')
        
        # Remove parentheses if they wrap the entire expression
        temp_expr = temp_expr.strip()
        if temp_expr.startswith('(') and temp_expr.endswith(')'):
            temp_expr = temp_expr[1:-1]
        
        print(f"DEBUG: Final integrand extracted: '{temp_expr}'")
        
        # Now convert the integrand using latex2sympy if available
        try:
            if latex2sympy and temp_expr.strip():
                sympy_expr = latex2sympy(temp_expr)
                result = str(sympy_expr)
                print(f"DEBUG: latex2sympy converted integrand '{temp_expr}' to '{result}'")
                return result
            else:
                return temp_expr.strip() if temp_expr.strip() else "x*y"
        except Exception as e:
            print(f"DEBUG: latex2sympy failed on integrand: {e}")
            return temp_expr.strip() if temp_expr.strip() else "x*y"
    
    # For non-integral expressions, use latex2sympy directly
    try:
        if latex2sympy:
            # Handle \cdot before passing to latex2sympy
            clean_expr = clean_expr.replace('\\cdot', '*')
            
            sympy_expr = latex2sympy(clean_expr)
            result = str(sympy_expr)
            print(f"DEBUG: latex2sympy converted '{clean_expr}' to '{result}'")
            
            # Clean up common LaTeX residue
            result = result.replace('\\right', '').replace('\\left', '')
            result = result.replace('\\,', '').replace('\\', '')
            result = result.strip()
            
            print(f"DEBUG: After cleanup: '{result}'")
            return result
    except Exception as e:
        print(f"DEBUG: latex2sympy failed: {e}")
    
    # Fallback to manual extraction
    return extract_integrand_from_latex(latex_expr)

def extract_integrand_from_latex(latex_expr):
    """Extract the integrand from LaTeX integral expressions using latex2sympy"""
    if not latex_expr:
        return ""
    
    # Remove $$ delimiters
    expr = latex_expr.strip()
    if expr.startswith('$$') and expr.endswith('$$'):
        expr = expr[2:-2].strip()
    elif expr.startswith('$') and expr.endswith('$'):
        expr = expr[1:-1].strip()
    
    # Use latex2sympy to convert the entire LaTeX expression
    try:
        if latex2sympy:
            # Convert the LaTeX to SymPy expression
            sympy_expr = latex2sympy(expr)
            print(f"DEBUG: latex2sympy converted '{expr}' to '{sympy_expr}'")
            return str(sympy_expr)
        else:
            # Fallback if latex2sympy not available
            import re
            integrand_match = re.search(r'\([^)]+\)', expr)
            if integrand_match:
                integrand = integrand_match.group(0)[1:-1]
                return integrand.strip()
            return "x*y"
    except Exception as e:
        print(f"DEBUG: latex2sympy failed with error: {e}")
        # Fallback to manual parsing
        import re
        integrand_match = re.search(r'\([^)]+\)', expr)
        if integrand_match:
            integrand = integrand_match.group(0)[1:-1]
            return integrand.strip()
        return "x*y"

def parse_limits_from_latex(latex_expr):
    """Extract limits from LaTeX integral expressions"""
    if not latex_expr:
        return "0,1,0,1"
    
    import re
    
    # Find all _a^b patterns
    limits_matches = re.findall(r'_(\d+)\^(\d+)', latex_expr)
    if limits_matches:
        # Flatten the list: [(0,1), (0,1)] -> [0,1,0,1]
        limits_list = []
        for lower, upper in limits_matches:
            limits_list.extend([lower, upper])
        return ','.join(limits_list)
    
    return "0,1,0,1"  # Default fallback

def parse_integral_limits(limits_str, variables):
    """Parse limits for multiple integrals in the format expected by solve_multiple_integral"""
    if not limits_str or not variables:
        # Default limits based on number of variables
        if len(variables) == 2:
            return [('x', '0', '1'), ('y', '0', '1')]
        elif len(variables) == 3:
            return [('x', '0', '1'), ('y', '0', '1'), ('z', '0', '1')]
        else:
            return [('x', '0', '1')]
    
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
            # Default if not enough limits provided
            limits.append((var, '0', '1'))
    
    return limits

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        operation = data.get("operation", "")
        
        # Add comprehensive debug logging for ALL requests
        print("="*80)
        print("INCOMING REQUEST DEBUG INFO:")
        print(f"Raw request data: {data}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Request content type: {request.content_type}")
        print(f"Operation: {operation}")
        
        # Log all fields in the data
        for key, value in data.items():
            print(f"  {key}: '{value}' (type: {type(value).__name__}, len: {len(str(value)) if value else 0})")
        print("="*80)
        
        if operation == "partial_derivative":
            function_str = data.get("function", "")
            variables_str = data.get("variables", "")
            order_str = data.get("order", "1")
            
            function = safe_sympify(function_str)
            variables = parse_vector_input(variables_str)
            order = int(order_str) if order_str.isdigit() else 1
            
            return jsonify({
                "result": solve_partial_derivative(str(function), variables, order)
            })
            
        elif operation == "double_integral":
            expression_str = data.get("function", "")  # Changed from "expression" to "function"
            variables_str = data.get("variables", "x,y")
            limits_str = data.get("limits", "0,1,0,1")
            
            # Debug prints
            print(f"DEBUG: Received data: {data}")
            print(f"DEBUG: expression_str = '{expression_str}'")
            
            # Check if the expression is empty
            if not expression_str.strip():
                print("DEBUG: Expression is empty, returning error")
                return jsonify({"error": "Expression cannot be empty"}), 400
            
            # Use the new parser function for LaTeX or regular expressions
            if '\\int' in expression_str or '$' in expression_str:
                print("DEBUG: LaTeX expression detected, using parse_latex_integral_with_limits")
                parsed_expr, latex_limits = parse_latex_integral_with_limits(expression_str)
                
                # Use LaTeX limits if they were successfully extracted and look reasonable
                if latex_limits and len(latex_limits) >= 2:
                    print(f"DEBUG: Using LaTeX limits: {latex_limits}")
                    limits = latex_limits
                else:
                    print("DEBUG: LaTeX limits not found or incomplete, using manual limits")
                    variables = parse_vector_input(variables_str) if variables_str else ['x', 'y']
                    limits = parse_integral_limits(limits_str, variables)
            else:
                print("DEBUG: Regular expression input")
                parsed_expr = parse_single_expression(expression_str)
                variables = parse_vector_input(variables_str) if variables_str else ['x', 'y']
                limits = parse_integral_limits(limits_str, variables)
            
            print(f"DEBUG: Final parsed expression = '{parsed_expr}'")
            print(f"DEBUG: Final limits = {limits}")
            print(f"DEBUG: About to call solve_multiple_integral('{parsed_expr}', {limits})")
            
            result = solve_multiple_integral(parsed_expr, limits)
            print(f"DEBUG: solve_multiple_integral returned: '{result}'")
            
            return jsonify({
                "result": result
            })
            
        elif operation == "double_integral_polar":
            expression_str = data.get("function", "")  # Changed from "expression" to "function"
            variables_str = data.get("variables", "r,theta")
            limits_str = data.get("limits", "0,1,0,2*pi")
            
            if not expression_str.strip():
                return jsonify({"error": "Expression cannot be empty"}), 400
            
            # Use the new parser function for LaTeX or regular expressions
            if '\\int' in expression_str or '$' in expression_str:
                parsed_expr = parse_latex_integral(expression_str)
            else:
                parsed_expr = parse_single_expression(expression_str)
            
            variables = parse_vector_input(variables_str) if variables_str else ['r', 'theta']
            limits = parse_integral_limits(limits_str, variables)
            
            return jsonify({
                "result": solve_multiple_integral(parsed_expr, limits)
            })
            
        elif operation == "triple_integral":
            expression_str = data.get("function", "")  # Changed from "expression" to "function"
            variables_str = data.get("variables", "x,y,z")
            limits_str = data.get("limits", "0,1,0,1,0,1")
            
            if not expression_str.strip():
                return jsonify({"error": "Expression cannot be empty"}), 400
            
            # Use the new parser function for LaTeX or regular expressions
            if '\\int' in expression_str or '$' in expression_str:
                parsed_expr = parse_latex_integral(expression_str)
            else:
                parsed_expr = parse_single_expression(expression_str)
            
            variables = parse_vector_input(variables_str) if variables_str else ['x', 'y', 'z']
            limits = parse_integral_limits(limits_str, variables)
            
            return jsonify({
                "result": solve_multiple_integral(parsed_expr, limits)
            })
            
        elif operation == "triple_integral_polar":
            expression_str = data.get("function", "")  # Changed from "expression" to "function"
            variables_str = data.get("variables", "r,theta,z")
            limits_str = data.get("limits", "0,1,0,2*pi,0,1")
            
            if not expression_str.strip():
                return jsonify({"error": "Expression cannot be empty"}), 400
            
            # Use the new parser function for LaTeX or regular expressions
            if '\\int' in expression_str or '$' in expression_str:
                parsed_expr = parse_latex_integral(expression_str)
            else:
                parsed_expr = parse_single_expression(expression_str)
            
            variables = parse_vector_input(variables_str) if variables_str else ['r', 'theta', 'z']
            limits = parse_integral_limits(limits_str, variables)
            
            return jsonify({
                "result": solve_multiple_integral(parsed_expr, limits)
            })
            
        elif operation == "triple_integral_cylindrical":
            expression_str = data.get("function", "")  # Changed from "expression" to "function"
            variables_str = data.get("variables", "r,theta,z")
            limits_str = data.get("limits", "0,1,0,2*pi,0,1")
            
            if not expression_str.strip():
                return jsonify({"error": "Expression cannot be empty"}), 400
            
            # Use the new parser function for LaTeX or regular expressions
            if '\\int' in expression_str or '$' in expression_str:
                parsed_expr = parse_latex_integral(expression_str)
            else:
                parsed_expr = parse_single_expression(expression_str)
            
            variables = parse_vector_input(variables_str) if variables_str else ['r', 'theta', 'z']
            limits = parse_integral_limits(limits_str, variables)
            
            return jsonify({
                "result": solve_multiple_integral(parsed_expr, limits)
            })
        elif operation == "arc_length":
            parametric_str = data.get("parametric", "")
            parameter_str = data.get("parameter", "")
            limits_str = data.get("limits", "")
            
            # Parse parametric functions using the improved parser
            try:
                parametric_functions = parse_parametric_functions(parametric_str)
                parameter = parameter_str.strip() if parameter_str and parameter_str.strip() else 't'
                limits = parse_limits(limits_str)
                
                # Convert limits to strings for calc3.py compatibility
                result = solve_arc_length(parametric_functions, parameter, str(limits[0]), str(limits[1]))
                
                return jsonify({"result": result})
                
            except Exception as e:
                return jsonify({"error": f"Arc length parsing error: {str(e)}"}), 400
            
        elif operation == "divergence":
            vector_field_str = data.get("vector_field", "")
            vector_field = parse_vector_input(vector_field_str)
            # Default to x,y,z variables for 3D or x,y for 2D
            variables = ['x', 'y', 'z'][:len(vector_field)]
            
            return jsonify({
                "result": solve_divergence(vector_field, variables)
            })
            
        elif operation == "curl":
            vector_field_str = data.get("vector_field", "")
            vector_field = parse_vector_input(vector_field_str)
            variables = ['x', 'y', 'z']  # Curl is always 3D
            
            return jsonify({
                "result": solve_curl(vector_field, variables)
            })
            
        elif operation == "gradient":
            function_str = data.get("function", "")
            variables_str = data.get("variables", "x,y,z")
            
            function = safe_sympify(function_str)
            variables = parse_vector_input(variables_str)
            
            return jsonify({
                "result": solve_gradient(str(function), variables)
            })
            
        elif operation in ["scalar_line_integral", "vector_line_integral"]:
            field_str = data.get("function" if operation == "scalar_line_integral" else "vector_field", "")
            curve_str = data.get("curve", "")
            limits_str = data.get("limits", "")
            
            # Parse field (scalar string or vector list)
            field = field_str if operation == "scalar_line_integral" else parse_vector_input(field_str)
            curve = parse_parametric_functions(curve_str)
            limits = parse_limits(limits_str)
            
            return jsonify({
                "result": solve_line_integral(field, 't', curve, limits)
            })
            
        elif operation == "surface_integral":
            vector_field_str = data.get("vector_field", "")
            surface_str = data.get("surface", "")
            
            vector_field = parse_vector_input(vector_field_str)
            surface = safe_sympify(surface_str)
            
            # For now, provide basic parameters for surface integrals
            # This is a simplified implementation - real surface integrals need parametric forms
            params = ['u', 'v']  # Default parameters
            bounds = [(0, 1), (0, 1)]  # Default bounds
            
            return jsonify({
                "result": solve_surface_integral(vector_field, params, str(surface), bounds)
            })
            
        elif operation == "directional_derivative":
            function_str = data.get("function", "")
            direction_str = data.get("direction", "")
            point_str = data.get("point", "")
            
            function = safe_sympify(function_str)
            direction = parse_vector_input(direction_str)
            point = parse_vector_input(point_str)
            
            # For directional derivative, we need variables from the function
            variables = ['x', 'y', 'z'][:len(direction)]
            
            return jsonify({
                "result": solve_directional_derivative(str(function), variables, direction)
            })
            
        elif operation == "greens_theorem":
            vector_field_str = data.get("vector_field", "")
            
            vector_field = parse_vector_input(vector_field_str)
            variables = ['x', 'y']  # Green's theorem is 2D
            
            return jsonify({
                "result": solve_greens_theorem(vector_field, variables)
            })
            
        elif operation == "stokes_theorem":
            vector_field_str = data.get("vector_field", "")
            surface_str = data.get("surface", "")
            
            vector_field = parse_vector_input(vector_field_str)
            surface = parse_parametric_functions(surface_str)
            
            # Default parameters and bounds for Stokes' theorem
            params = ['u', 'v']
            bounds = [(0, 1), (0, 1)]
            
            return jsonify({
                "result": solve_stokes_theorem(vector_field, params, surface, bounds)
            })
            
        elif operation == "lagrange_multipliers":
            function_str = data.get("function", "")
            constraint_str = data.get("constraint", "")
            
            # Automatically extract variables from function and constraint
            function_parsed = safe_sympify(function_str)
            constraint_parsed = safe_sympify(constraint_str)
            
            # Get all free symbols from both expressions
            all_symbols = function_parsed.free_symbols.union(constraint_parsed.free_symbols)
            # Filter out known constants and lambda/mu symbols, keep only likely variable names
            excluded = {'pi', 'e', 'I', 'lambda', 'mu', 'Lambda', 'Mu', 'E'}
            variables = [str(s) for s in all_symbols if str(s) not in excluded and len(str(s)) <= 3]
            variables.sort()  # Sort for consistency
            
            if not variables:
                return jsonify({"error": "Could not extract variables from the function and constraint. Please ensure they contain variables like x, y, z."}), 400
            
            return jsonify({
                "result": solve_lagrange_multipliers(function_str, constraint_str, variables)
            })
            
        else:
            return jsonify({"error": f"Unknown operation: {operation}"}), 400
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
