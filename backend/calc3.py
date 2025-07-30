from sympy import symbols, Matrix, diff, sympify, integrate, sqrt, solve, Eq, Integral, sin, cos, pi, expand
from sympy.abc import r, theta, _clash1

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

def solve_arc_length(exprs: list, param: str, a: str, b: str) -> str:

    try:
        t = param
        a = sympify(a)
        b = sympify(b)

        components = [sympify(expr) for expr in exprs]
        derivatives = [diff(comp, t) for comp in components]
        integrand = sqrt(sum(d**2 for d in derivatives))

        result = integrate(integrand, (t, a, b)).doit()
        if isinstance(result, Integral):
            result = result.evalf()
            result = round(result, 5)
        return str(result)

    except Exception as e:
        return f"Error: {str(e)}"

def solve_gradient(expr: str, variables: list) -> str:
    try:
        expression = sympify(expr)
        sym_vars = [symbols(v) for v in variables]
        grad = [diff(expression, var) for var in sym_vars]

        # Choose unit vectors dynamically
        unit_vectors = ['i', 'j', 'k', 'l', 'm', 'n']  # add more if needed

        if len(grad) > len(unit_vectors):
            return "Error: Not enough unit vector symbols defined."

        terms = [f"{grad[i]}*{unit_vectors[i]}" for i in range(len(grad))]
        return " + ".join(terms)
    except Exception as e:
        return f"Error: {str(e)}"

def solve_multiple_integral(expr: str, limits: list) -> str:
    try:
        local_dict = _clash1.copy()
        for var, _, _ in limits:
            local_dict[var] = symbols(var)

        expression = sympify(expr, locals=local_dict)
        # Apply integrals in order: outer to inner
        print(limits)
        for var, a, b in limits:
            var_sym = local_dict[var]
            a_sym = sympify(a, locals=local_dict)
            b_sym = sympify(b, locals=local_dict)
            expression = integrate(expression, (var_sym, a_sym, b_sym))
        return str(expression.doit().simplify())
    except Exception as e:
        return f"Error: {str(e)}"     

def solve_polar_integral(expr: str, limits: list) -> str:
    try:
        local_dict = _clash1.copy()
        for var, _, _ in limits:
            local_dict[var] = symbols(var)
        
        expression = sympify(expr, locals=local_dict)

        for var, a, b in limits:
            var_sym = local_dict[var]
            lower = sympify(a, locals=local_dict)
            upper = sympify(b, locals=local_dict)
            expression = integrate(expression, (var_sym, lower, upper))

        return str(expression.doit().simplify())
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
def solve_line_integral(field, param: str, curve: list, bounds: list = [0, 1]) -> str:
    try:
        t = sympify(param)
        a, b = bounds
        r = Matrix([sympify(f) for f in curve])
        dr = r.diff(t)
        subs_map = {symbols(var): r[i] for i, var in enumerate('xyz'[:len(r)])}

        # Auto-detect field type
        if isinstance(field, str):
            # Scalar field: ∫ f(x, y, ...) ds
            f = sympify(field).subs(subs_map)
            magnitude = sqrt(sum(comp**2 for comp in dr))
            integrand = f * magnitude
            
        elif isinstance(field, (list, Matrix)):
            # Vector field: ∫ F · dr
            F = Matrix([sympify(f) for f in field])
            F_sub = F.subs(subs_map)
            integrand = F_sub.dot(dr)
        else:
            return "Error: Field must be a string or list"

        result = integrate(integrand, (t, a, b))
        return str(result.evalf())

    except Exception as e:
        return f"Error: {str(e)}"

# Surface integral 
def solve_surface_integral(field, params, surface, bounds):
    try:
        u, v = symbols(params)
        x, y, z = symbols("x y z")
        r = Matrix([sympify(expr) for expr in surface])
        ru = r.diff(u)
        rv = r.diff(v)
        normal_vector = ru.cross(rv)
        normal_magnitude = sqrt(normal_vector.dot(normal_vector))

        is_vector = isinstance(field, list) and len(field) == 3
        is_scalar = isinstance(field, str) or (isinstance(field, list) and len(field) == 1)
        substitutions = {x: r[0], y: r[1], z: r[2]}

        if is_vector:
            F = Matrix([sympify(f) for f in field])
            F_sub = F.subs(substitutions)
            integrand = F_sub.dot(normal_vector)
        elif is_scalar:
            f = sympify(field if isinstance(field, str) else field[0])
            f_sub = f.subs(substitutions)
            integrand = f_sub * normal_magnitude
        else:
            return "Error: Could not determine field type (expected scalar or 3D vector)."

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


def solve_lagrange_multipliers(f_expr: str, g_expr: str, variables: list, h_expr: str = None) -> dict:
    try:
        sym_vars = [symbols(v) for v in variables]
        f = sympify(f_expr)
        g = sympify(g_expr)
        λ = symbols('λ')

        eqs = []
        
        if h_expr:
            h = sympify(h_expr)
            μ = symbols('μ')
            eqs += [Eq(diff(f, var), λ * diff(g, var) + μ * diff(h, var)) for var in sym_vars]
            eqs.append(Eq(g, 0))
            eqs.append(Eq(h, 0))
            unknowns = sym_vars + [λ, μ]
        else:
            # Only one constraint
            eqs += [Eq(diff(f, var), λ * diff(g, var)) for var in sym_vars]
            eqs.append(Eq(g, 0))
            unknowns = sym_vars + [λ]

        sol = solve(eqs, unknowns, dict=True)
        real_solutions = []
        for s in sol:
            if all(v.is_real for v in s.values()):
                f_val = f.subs(s)
                s_eval = {str(k): str(v) for k, v in s.items()}
                s_eval["f_value"] = str(f_val)
                real_solutions.append(s_eval)
         
        if not real_solutions:
            return {"error": "No real solutions found."}       
        return real_solutions
    except Exception as e:
        return {"error": str(e)}
