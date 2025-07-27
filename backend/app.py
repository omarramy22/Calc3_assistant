from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import SympifyError
from parser import analyze_expression
from calc3 import (
    solve_partial_derivative,
    solve_gradient,
    solve_multiple_integral,
    solve_arc_length,
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

@app.route('/calculate', methods=['POST'])
def solve():
    latex = request.json.get("latex", "")
    print(f"Received LaTeX: {latex}")
    result = analyze_expression(latex)

    if result["type"] == "partial_derivative":
        try:
            return jsonify({
                "result": solve_partial_derivative(
                    result["expression"],
                    result["variables"],
                    result["orders"][0] if result["orders"] else 1
                )
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif result["type"] == "arc_length":
        try:
            return jsonify({
                "result": solve_arc_length(
                    result["expression"],
                    result["param"],
                    result["limits"][0],
                    result["limits"][1]
                )
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif result["type"] == "directional_derivative":
        try:
            return jsonify({
                "result": solve_directional_derivative(
                    result["expression"],
                    result["variables"],
                    result["direction"]
                )
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif result["type"] == "gradient":
        try:
            return jsonify({
                "result": solve_gradient(
                    result["expression"],
                    result["variables"]
                )
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif result["type"] == "multiple_integral":
        try:
            return jsonify({
                "result": solve_multiple_integral(
                    result["expression"],
                    result["limits"]
                )
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif result["type"] == "raw_expression":
        return jsonify({"result": "Unrecognized symbolic operation"})

    else:
        return jsonify({"error": result.get("message", "Unknown parsing error")}), 400

if __name__ == "__main__":
    app.run(debug=True)
