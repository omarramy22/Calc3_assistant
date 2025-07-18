import unittest
from sympy import simplify, sqrt, symbols, sympify
from calc3 import *

class TestCalculusFunctions(unittest.TestCase):

    def test_partial_derivative(self):
        self.assertEqual(solve_partial_derivative("x*y", ["x", "y"], 2), "1")
        self.assertEqual(solve_partial_derivative("x + y", ["x"], 0), "x + y")

    def test_gradient(self):
        self.assertEqual(solve_gradient("x**2 + y**2", ["x", "y"]), ["2*x", "2*y"])
        self.assertEqual(solve_gradient("sin(x*y)", ["x", "y"]), ["y*cos(x*y)", "x*cos(x*y)"])

    def test_multiple_integral(self):
        self.assertEqual(solve_multiple_integral("x*y", [["x", 0, 2], ["y", 0, 3]]), "9")
        self.assertEqual(solve_multiple_integral("x", [["x", 0, 5]]), "25/2")

    def test_divergence(self):
        self.assertEqual(solve_divergence(["x", "y", "z"], ["x", "y", "z"]), "3")
        self.assertEqual(solve_divergence(["x**2", "y**2", "z**2"], ["x", "y", "z"]), "2*x + 2*y + 2*z")

    def test_curl(self):
        self.assertEqual(solve_curl(["x*y", "y*z", "z*x"], ["x", "y", "z"]), ["-y", "-z", "-x"])
        self.assertEqual(solve_curl(["0", "0", "0"], ["x", "y", "z"]), ["0", "0", "0"])

    def test_directional_derivative(self):
        res = solve_directional_derivative("x + y", ["x", "y"], [1/sqrt(2), 1/sqrt(2)])
        self.assertTrue(simplify(res) == sqrt(2))
        self.assertIn("Error", solve_directional_derivative("x + y", ["x", "y"], [0, 0]))

    def test_line_integral(self):
        result = solve_line_integral(["x", "y", "z"], "t", ["t", "t**2", "t**3"], [0, 1])
        expected = "3/2" 
        self.assertEqual(sympify(result), sympify(expected))

    def test_surface_integral(self):
        result = solve_surface_integral(["x", "y", "z"], ["u", "v"], ["u", "v", "u*v"], [[0, 1], [0, 2]])
        self.assertEqual(sympify(result), sympify("-1"))

    def test_greens_theorem(self):
        self.assertEqual(solve_greens_theorem(["-y", "x"], ["x", "y"]), "2")
        self.assertEqual(solve_greens_theorem(["0", "0"], ["x", "y"]), "0")

    def test_stokes_theorem_square_xy(self):
        vector_field = ["-y", "x", "0"]
        params = ["u", "v"]
        surface = ["u", "v", "0"]
        bounds = [[0, 1], [0, 1]] 
        
        result = solve_stokes_theorem(vector_field, params, surface, bounds)
        self.assertEqual(sympify(result), sympify("2"))

    def test_lagrange_multipliers(self):
        result = solve_lagrange_multipliers("x**2 + y**2", "x + y - 1", ["x", "y"])
        self.assertIn("x", result)
        self.assertIn("λ", "".join(result.keys()))

if __name__ == "__main__":
    unittest.main()
