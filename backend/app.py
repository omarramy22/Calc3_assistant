from flask import Flask, request, jsonify
from flask_cors import CORS
from calc3 import (
    solve_partial_derivative,
    solve_gradient,
    solve_multiple_integral,
    solve_divergence,
    solve_curl,
    solve_line_integral,
    solve_surface_integral,
    solve_directional_derivative,
    solve_greens_theorem,
    solve_stokes_theorem,
    solve_lagrange_multipliers
)

app = Flask(__name__)
CORS(app)

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    operation = data.get("operation")
    expression = data.get("expression")
    variables = data.get("variables", [])
    order = data.get("order", len(variables))
    limits = data.get("limits", [])
    vector_field = data.get("vector_field", [])
    param = data.get("param")
    curve = data.get("curve", [])
    params = data.get("params", [])
    surface = data.get("surface", [])
    direction = data.get("direction", [])
    constraint = data.get("constraint")


    if operation == "partial_derivative":
        result = solve_partial_derivative(expression, variables, order)
    elif operation == "gradient":
        result = solve_gradient(expression, variables)
    elif operation == "multiple_integral":
        result = solve_multiple_integral(expression, limits)
    elif operation == "divergence":
        result = solve_divergence(vector_field, variables)
    elif operation == "curl":
        result = solve_curl(vector_field, variables)
    elif operation == "line_integral":
        result = solve_line_integral(vector_field, param, curve)
    elif operation == "surface_integral":
        result = solve_surface_integral(vector_field, params, surface)
    elif operation == "directional_derivative":
        result = solve_directional_derivative(expression, variables, direction)
    elif operation == "greens_theorem":
        result = solve_greens_theorem(vector_field, variables)
    elif operation == "stokes_theorem":
        result = solve_stokes_theorem(vector_field, params, surface)
    elif operation == "lagrange_multipliers":
        result = solve_lagrange_multipliers(expression, constraint, variables)
    else:
        return jsonify({"error": "Invalid operation"}), 400

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
