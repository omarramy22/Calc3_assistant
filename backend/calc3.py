from sympy import symbols, Matrix, diff, sympify, integrate, sqrt

def solve_partial_derivative(expr: str, variables: list, order: int = 1) -> str:

    try:
        expression = sympify(expr)
        
        if order and len(variables) < order:
            variables += [variables[-1]] * (order - len(variables))

        differentiation_variables = [symbols(var) for var in variables]
        
        if not order :
            derivative = expression
        else:
            derivative = diff(expression, *differentiation_variables)
        return str(derivative)

    except Exception as e:
        return f"Error: {str(e)}"

def solve_gradient(expr: str, variables: list) -> list:
    try:
        expression = sympify(expr)
        sym_vars = [symbols(v) for v in variables]
        grad = [str(diff(expression, var)) for var in sym_vars]
        return grad
    except Exception as e:
        return [f"Error: {str(e)}"]

def solve_multiple_integral(expr: str, limits: list) -> str:
    try:
        expression = sympify(expr)
        sym_limits = [(symbols(var), a, b) for (var, a, b) in limits]
        result = integrate(expression, *sym_limits)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

# Divergence
def solve_divergence(vector_field: list, variables: list) -> str:
    try:
        if len(vector_field) != len(variables):
            return "Error: Vector field and variable count must match."
        components = [sympify(c) for c in vector_field]
        sym_vars = [symbols(v) for v in variables]
        div = sum(diff(components[i], sym_vars[i]) for i in range(len(components)))
        return str(div)
    except Exception as e:
        return f"Error: {str(e)}"

# Curl (for 3D only)
def solve_curl(vector_field: list[str], variables: list[str]) -> list[str]:
    try:
        if len(vector_field) != 3 or len(variables) != 3:
            return ["Error: Curl is only defined for 3D vector fields."]
        x, y, z = symbols(variables)
        F1, F2, F3 = [sympify(f) for f in vector_field]

        curl_x = diff(F3, y) - diff(F2, z)
        curl_y = diff(F1, z) - diff(F3, x)
        curl_z = diff(F2, x) - diff(F1, y)

        return [str(curl_x), str(curl_y), str(curl_z)]
    except Exception as e:
        return [f"Error: {str(e)}"]

# Line integral 
def solve_line_integral(vector_field: list, param: str, curve: list, param_bounds: list = [0, 1]) -> list:
    try:
        t = symbols(param)
        a, b = param_bounds
        r = Matrix([sympify(f) for f in curve])
        dr = r.diff(t)
        F = Matrix([sympify(f) for f in vector_field])
        F_sub = F.subs({symbols('x'): r[0], symbols('y'): r[1], symbols('z'): r[2]})
        dot = F_sub.dot(dr)
        result = integrate(dot, (t, a, b))
        return str(result)
    except Exception as e:
        return [f"Error: {str(e)}"]

# Surface integral 
def solve_surface_integral(vector_field, params, surface, bounds):
    try:
        u, v = symbols(params)
        r = Matrix([sympify(expr) for expr in surface])
        ru = r.diff(u)
        rv = r.diff(v)
        normal_vector = ru.cross(rv)

        F = Matrix([sympify(f) for f in vector_field])
        x, y, z = symbols("x y z")
        substitutions = {x: r[0], y: r[1], z: r[2]}
        F_sub = F.subs(substitutions)

        integrand = F_sub.dot(normal_vector)
        result = integrate(integrand, (u, bounds[0][0], bounds[0][1]), (v, bounds[1][0], bounds[1][1]))
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
    
# Directional derivative    
def solve_directional_derivative(expr: str, variables: list, direction: list) -> str:
    try:
        if len(direction) != len(variables):
            return "Error: Direction vector must match the number of variables."
        expression = sympify(expr)
        sym_vars = [symbols(v) for v in variables]
        grad = Matrix([diff(expression, var) for var in sym_vars])
        dir_vector = Matrix(direction)

        # Normalize the direction vector
        magnitude = sqrt(sum(c**2 for c in dir_vector))
        if magnitude == 0:
            return "Error: Direction vector cannot be zero."
        unit_vector = dir_vector / magnitude

        directional_derivative = grad.dot(unit_vector)
        return str(directional_derivative)
    except Exception as e:
        return f"Error: {str(e)}"

def solve_greens_theorem(vector_field: list, variables: list) -> str:
    try:
        x, y = [symbols(v) for v in variables]
        M = sympify(vector_field[0])
        N = sympify(vector_field[1])
        curl_2d = diff(N, x) - diff(M, y)
        return str(curl_2d)
    except Exception as e:
        return f"Error: {str(e)}"
    
def solve_stokes_theorem(vector_field: list, params: list, surface: list, bounds: list) -> str:
    try:
        u, v = symbols(params)
        r = Matrix([sympify(expr) for expr in surface])
        ru = r.diff(u)
        rv = r.diff(v)
        normal = ru.cross(rv)  # 3x1 vector

        F = Matrix([sympify(f) for f in vector_field])
        curl = Matrix([
            diff(F[2], symbols("y")) - diff(F[1], symbols("z")),
            diff(F[0], symbols("z")) - diff(F[2], symbols("x")),
            diff(F[1], symbols("x")) - diff(F[0], symbols("y")),
        ])

        x, y, z = symbols("x y z")
        substitutions = {x: r[0], y: r[1], z: r[2]}
        curl_sub = curl.subs(substitutions)

        result = integrate(curl_sub.dot(normal), (u, bounds[0][0], bounds[0][1]), (v, bounds[1][0], bounds[1][1]))        
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def solve_lagrange_multipliers(f_expr: str, g_expr: str, variables: list) -> dict:
    try:
        from sympy import Eq, solve, symbols, sympify

        sym_vars = [symbols(v) for v in variables]
        f = sympify(f_expr)
        g = sympify(g_expr)
        λ = symbols('λ')

        eqs = [
            Eq(diff(f, var), λ * diff(g, var))
            for var in sym_vars
        ] + [Eq(g, 0)]

        sol = solve(eqs, sym_vars + [λ], dict=True)
        return {str(k): str(v) for s in sol for k, v in s.items()}
    except Exception as e:
        return {"error": str(e)}



