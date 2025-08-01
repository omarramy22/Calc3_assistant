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
    solve_polar_integral,
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
    parse_parametric_functions
)

app = Flask(__name__)
CORS(app)

def safe_sympify(expr_str):
    """Safely convert string to SymPy expression with proper parsing"""
    if not expr_str or expr_str.strip() == '':
        return None
    
    try:
        # First try direct sympify
        return sympify(expr_str)
    except:
        try:
            # Try latex2sympy if available and if the string looks like LaTeX
            if latex2sympy and ('\\' in expr_str or '{' in expr_str):
                return latex2sympy(expr_str)
        except:
            pass
        
        try:
            # Try parsing as LaTeX using SymPy's parser
            return parse_latex(expr_str)
        except:
            # If all fail, try some common replacements
            expr_str = expr_str.replace('^', '**')  # Convert ^ to **
            expr_str = expr_str.replace('π', 'pi')   # Convert π to pi
            return sympify(expr_str)

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

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        operation = data.get("operation", "")
        
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
            
        elif operation == "multiple_integral":
            expression_str = data.get("expression", "")
            
            # Check if this is a LaTeX expression
            result = analyze_expression(expression_str)
            
            if result.get("type") in ["double_integral", "triple_integral"]:
                if "error" in result:
                    return jsonify({"error": result["error"]}), 400
                
                # Use the parsed result
                expression = result["expression"]
                limits = result["limits"]
                
                return jsonify({
                    "result": solve_multiple_integral(expression, limits)
                })
            else:
                # Manual input format - fallback
                variables_str = data.get("variables", "x,y")
                limits_str = data.get("limits", "0,1,0,1")
                
                return jsonify({
                    "result": solve_multiple_integral(expression_str, [])
                })
                
        elif operation == "polar_integral":
            expression_str = data.get("expression", "")
            
            # Check if this is a LaTeX expression first
            result = analyze_expression(expression_str)
            
            if result.get("type") in ["double_integral", "triple_integral"]:
                if "error" in result:
                    return jsonify({"error": result["error"]}), 400
                
                # Use the parsed result for polar coordinates
                expression = result["expression"]
                limits = result["limits"]
                
                return jsonify({
                    "result": solve_polar_integral(expression, limits)
                })
            else:
                # Manual input - create default limits for polar coordinates
                # Default: r from 0 to 1, theta from 0 to 2*pi
                default_limits = [('r', 0, 1), ('theta', 0, '2*pi')]
                
                return jsonify({
                    "result": solve_polar_integral(str(function), default_limits)
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
