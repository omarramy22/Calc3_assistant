from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import sympify

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
    parse_expression,
    parse_integral_latex,
    parse_vector,
    parse_limits,
    parse_integral_limits
)

app = Flask(__name__)
CORS(app)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        operation = data.get("operation", "")
        
        print(f"Operation: {operation}")
        print(f"Request data: {data}")
        
        if operation == "partial_derivative":
            function_str = data.get("function", "")
            variables_str = data.get("variables", "")
            order_str = data.get("order", "1")
            
            # Parse using SymPy
            function_expr = parse_expression(function_str)
            variables = parse_vector(variables_str)
            order = int(order_str) if order_str.isdigit() else 1
            
            return jsonify({
                "result": solve_partial_derivative(str(function_expr), variables, order)
            })
            
        elif operation in ["double_integral", "double_integral_polar"]:
            expression_str = data.get("function", "")
            variables_str = data.get("variables", "x,y" if operation == "double_integral" else "r,theta")
            limits_str = data.get("limits", "0,1,0,1" if operation == "double_integral" else "0,1,0,2*pi")
            
            if not expression_str.strip():
                return jsonify({"error": "Expression cannot be empty"}), 400
            
            # Check if it's a LaTeX integral template
            if '\\int' in expression_str:
                integrand, latex_limits = parse_integral_latex(expression_str)
                if latex_limits:
                    limits = latex_limits
                else:
                    variables = parse_vector(variables_str)
                    limits = parse_integral_limits(limits_str, variables)
            else:
                # Regular expression
                integrand_expr = parse_expression(expression_str)
                integrand = str(integrand_expr)
                variables = parse_vector(variables_str)
                limits = parse_integral_limits(limits_str, variables)
            
            return jsonify({
                "result": solve_multiple_integral(integrand, limits)
            })
            
        elif operation in ["triple_integral", "triple_integral_polar", "triple_integral_cylindrical"]:
            expression_str = data.get("function", "")
            
            # Default variables based on coordinate system
            if operation == "triple_integral":
                default_vars = "x,y,z"
                default_limits = "0,1,0,1,0,1"
            else:  # polar or cylindrical
                default_vars = "r,theta,z"
                default_limits = "0,1,0,2*pi,0,1"
            
            variables_str = data.get("variables", default_vars)
            limits_str = data.get("limits", default_limits)
            
            if not expression_str.strip():
                return jsonify({"error": "Expression cannot be empty"}), 400
            
            # Check if it's a LaTeX integral template
            if '\\int' in expression_str:
                integrand, latex_limits = parse_integral_latex(expression_str)
                if latex_limits:
                    limits = latex_limits
                else:
                    variables = parse_vector(variables_str)
                    limits = parse_integral_limits(limits_str, variables)
            else:
                # Regular expression
                integrand_expr = parse_expression(expression_str)
                integrand = str(integrand_expr)
                variables = parse_vector(variables_str)
                limits = parse_integral_limits(limits_str, variables)
            
            return jsonify({
                "result": solve_multiple_integral(integrand, limits)
            })
            
        elif operation == "arc_length":
            parametric_str = data.get("parametric", "")
            parameter_str = data.get("parameter", "t")
            limits_str = data.get("limits", "0,1")
            
            # Parse parametric functions
            parametric_functions = parse_vector(parametric_str)
            parameter = parameter_str.strip() if parameter_str.strip() else 't'
            limits = parse_limits(limits_str)
            
            return jsonify({
                "result": solve_arc_length(parametric_functions, parameter, str(limits[0]), str(limits[1]))
            })
            
        elif operation == "gradient":
            function_str = data.get("function", "")
            variables_str = data.get("variables", "x,y,z")
            
            function_expr = parse_expression(function_str)
            variables = parse_vector(variables_str)
            
            return jsonify({
                "result": solve_gradient(str(function_expr), variables)
            })
            
        elif operation == "divergence":
            vector_field_str = data.get("vector_field", "")
            
            vector_field = parse_vector(vector_field_str)
            variables = ['x', 'y', 'z'][:len(vector_field)]
            
            return jsonify({
                "result": solve_divergence(vector_field, variables)
            })
            
        elif operation == "curl":
            vector_field_str = data.get("vector_field", "")
            
            vector_field = parse_vector(vector_field_str)
            variables = ['x', 'y', 'z']  # Curl is always 3D
            
            return jsonify({
                "result": solve_curl(vector_field, variables)
            })
            
        elif operation in ["scalar_line_integral", "vector_line_integral"]:
            field_str = data.get("function" if operation == "scalar_line_integral" else "vector_field", "")
            curve_str = data.get("curve", "")
            limits_str = data.get("limits", "0,1")
            
            # Parse field (scalar string or vector list)
            if operation == "scalar_line_integral":
                field_expr = parse_expression(field_str)
                field = str(field_expr)
            else:
                field = parse_vector(field_str)
            
            curve = parse_vector(curve_str)
            limits = parse_limits(limits_str)
            
            return jsonify({
                "result": solve_line_integral(field, 't', curve, limits)
            })
            
        elif operation == "surface_integral":
            vector_field_str = data.get("vector_field", "")
            surface_str = data.get("surface", "")
            
            vector_field = parse_vector(vector_field_str)
            surface_expr = parse_expression(surface_str)
            
            # Basic parameters for surface integrals
            params = ['u', 'v']
            bounds = [(0, 1), (0, 1)]
            return jsonify({
                "result": solve_surface_integral(vector_field, params, str(surface_expr), bounds)
            })
            
        elif operation == "directional_derivative":
            function_str = data.get("function", "")
            direction_str = data.get("direction", "")
            point_str = data.get("point", "")
            
            function_expr = parse_expression(function_str)
            direction = parse_vector(direction_str)
            point = parse_vector(point_str)
            
            variables = ['x', 'y', 'z'][:len(direction)]
            
            return jsonify({
                "result": solve_directional_derivative(str(function_expr), variables, direction)
            })
            
        elif operation == "greens_theorem":
            vector_field_str = data.get("vector_field", "")
            
            vector_field = parse_vector(vector_field_str)
            variables = ['x', 'y']  # Green's theorem is 2D
            
            return jsonify({
                "result": solve_greens_theorem(vector_field, variables)
            })
            
        elif operation == "stokes_theorem":
            vector_field_str = data.get("vector_field", "")
            surface_str = data.get("surface", "")
            
            vector_field = parse_vector(vector_field_str)
            surface = parse_vector(surface_str)
            
            params = ['u', 'v']
            bounds = [(0, 1), (0, 1)]
            
            return jsonify({
                "result": solve_stokes_theorem(vector_field, params, surface, bounds)
            })
            
        elif operation == "lagrange_multipliers":
            function_str = data.get("function", "")
            constraint_str = data.get("constraint", "")
            
            function_expr = parse_expression(function_str)
            constraint_expr = parse_expression(constraint_str)
            
            # Extract variables from both expressions
            all_symbols = function_expr.free_symbols.union(constraint_expr.free_symbols)
            excluded = {'pi', 'e', 'I', 'lambda', 'mu', 'Lambda', 'Mu', 'E'}
            variables = [str(s) for s in all_symbols if str(s) not in excluded and len(str(s)) <= 3]
            variables.sort()
            
            if not variables:
                return jsonify({"error": "Could not extract variables from the function and constraint."}), 400
            
            return jsonify({
                "result": solve_lagrange_multipliers(str(function_expr), str(constraint_expr), variables)
            })
            
        else:
            return jsonify({"error": f"Unknown operation: {operation}"}), 400
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
