from sympy import symbols, Matrix, diff, sympify, integrate, sqrt, solve, Eq, Integral, sin, cos, pi, simplify, trigsimp
def clean_trig_result(result, debug=False):
    """Clean up mathematical expressions without forcing numeric evaluation"""
    from sympy import log, E, exp, ln
    if debug:
        print(f"DEBUG: Original result: {result}")
    
    # First, apply symbolic substitutions to preserve exact forms
    try:
        # Replace log(e) with 1 symbolically
        result = result.subs(log(E), 1)
        if debug:
            print(f"DEBUG: After log(E) -> 1 substitution: {result}")
            
        # Also handle log(exp(1)) -> 1
        result = result.subs(log(exp(1)), 1)
        if debug:
            print(f"DEBUG: After log(exp(1)) -> 1 substitution: {result}")
            
    except Exception as e:
        if debug:
            print(f"DEBUG: Failed symbolic substitution: {e}")
        pass
    
    # Apply trigonometric simplification (preserves exact forms)
    try:
        result = trigsimp(result)
        if debug:
            print(f"DEBUG: After trigsimp(): {result}")
    except:
        pass
    
    # Apply general simplification (preserves exact forms)
    try:
        result = simplify(result)
        if debug:
            print(f"DEBUG: After simplify(): {result}")
    except:
        pass
    
    # Convert to string for pattern-based cleanup
    result_str = str(result)
    if debug:
        print(f"DEBUG: Result string: '{result_str}'")
    
    # Apply string-based replacements for patterns that SymPy might miss
    replacements = {
        'log(e)': '1',
        'log(E)': '1',
        '*log(e)': '',  # Remove *log(e) completely
        '*log(E)': '',  # Remove *log(E) completely
        'log(e)*': '',  # Remove log(e)* completely
        'log(E)*': '',  # Remove log(E)* completely
        # Trigonometric constants
        'sin(pi)': '0',
        'sin(2*pi)': '0', 
        'sin(-pi)': '0',
        'cos(pi)': '-1',
        'cos(2*pi)': '1',
        'cos(-pi)': '-1',
        'sin(0)': '0',
        'cos(0)': '1',
        'sin(pi)**2': '0',
        'cos(pi)**2': '1'
    }
    
    # Apply string replacements
    original_str = result_str
    for pattern, replacement in replacements.items():
        if pattern in result_str:
            result_str = result_str.replace(pattern, replacement)
            if debug:
                print(f"DEBUG: Replaced '{pattern}' with '{replacement}'")
    
    # If we made string replacements, convert back to sympy expression
    if result_str != original_str:
        try:
            result = sympify(result_str)
            if debug:
                print(f"DEBUG: After string replacement: {result}")
        except Exception as e:
            if debug:
                print(f"DEBUG: Failed to sympify after string replacement: {e}")
            # If sympify fails, keep the original result
            pass
    
    if debug:
        print(f"DEBUG: Final result: {result}")
    
    return result

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
        
        # Clean up the result
        derivative = clean_trig_result(derivative)
        return str(derivative)

    except Exception as e:
        return f"Error: {str(e)}"

def solve_arc_length(exprs: list, param: str, a: str, b: str) -> str:
    try:
        # Convert parameter to symbol
        t = symbols(param)
        a = sympify(a)
        b = sympify(b)

        components = [sympify(expr) for expr in exprs]
        derivatives = [diff(comp, t) for comp in components]
        integrand = sqrt(sum(d**2 for d in derivatives))

        result = integrate(integrand, (t, a, b)).doit()
        
        # Handle different result types properly
        if isinstance(result, Integral):
            # If it's still an unevaluated integral, try numerical evaluation
            try:
                result = result.evalf()
            except:
                return f"Unevaluated integral: {str(result)}"
        
        # Try to get a numerical result
        try:
            # First try to evaluate symbolically
            result = result.evalf()
            
            # Check if result is a number (not symbolic)
            if result.is_number:
                # If it's a number, we can round it
                if result.is_real:
                    # Round to 5 decimal places for real numbers
                    return str(round(float(result), 5))
                else:
                    # For complex numbers, clean and return the symbolic form
                    result = clean_trig_result(result)
                    return str(result)
            else:
                # If it's still symbolic, clean and return as-is
                result = clean_trig_result(result)
                return str(result)
        except:
            # If evaluation fails, clean and return the symbolic result
            result = clean_trig_result(result)
            return str(result)

    except Exception as e:
        return f"Error: {str(e)}"

def solve_gradient(expr: str, variables: list) -> list[str]:
    try:
        expression = sympify(expr)
        sym_vars = [symbols(v) for v in variables]
        grad = [clean_trig_result(diff(expression, var)) for var in sym_vars]
        return [str(g) for g in grad]
    except Exception as e:
        return f"Error: {str(e)}"

def solve_multiple_integral(expr: str, limits: list) -> str:
    try:        
        # Create symbols for all variables first
        all_vars = {}
        for var, _, _ in limits:
            all_vars[var] = symbols(var)
        
        expression = sympify(expr, locals=all_vars)
        
        # Apply integrals in order: outer to inner
        for i, (var, a, b) in enumerate(limits):
            var_sym = all_vars[var]
            a_sym = sympify(a, locals=all_vars)
            b_sym = sympify(b, locals=all_vars)
            
            # Perform the integration
            integrated = integrate(expression, (var_sym, a_sym, b_sym))
            
            # Force evaluation if it's still an Integral object
            if hasattr(integrated, 'doit'):
                expression = integrated.doit()
            else:
                expression = integrated
            
        
        # Final simplification
        result = expression.simplify()
        
        # Clean up log(e) and other expressions
        result = clean_trig_result(result)
        
        final_str = str(result)
        return final_str
        
    except Exception as e:
        print(f"DEBUG solve_multiple_integral: ERROR: {e}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}"     

# Divergence
def solve_divergence(vector_field: list, variables: list) -> str:
    try:
        if len(vector_field) != len(variables):
            return "Error: Vector field and variable count must match."
        components = [sympify(c) for c in vector_field]
        sym_vars = [symbols(v) for v in variables]
        div = sum(diff(components[i], sym_vars[i]) for i in range(len(components)))
        
        # Clean up the result
        div = clean_trig_result(div)
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

        # Clean up each component
        curl_x = clean_trig_result(curl_x)
        curl_y = clean_trig_result(curl_y)
        curl_z = clean_trig_result(curl_z)

        return [str(curl_x), str(curl_y), str(curl_z)]
    except Exception as e:
        return [f"Error: {str(e)}"]

# Line integral 
def solve_line_integral(field, param: str, curve: list, bounds: list = [0, 1]) -> str:
    try:
        t = symbols(param)
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
        
        # Clean up the result
        result = clean_trig_result(result)
        return str(result)

    except Exception as e:
        return f"Error: {str(e)}"

# Surface integral 
def solve_surface_integral(field, params, surface, bounds, field_vars=("x", "y", "z")):
    try:
        u, v = symbols(params)
        field_syms = symbols(field_vars)
        r = Matrix([sympify(expr) for expr in surface])
        ru = r.diff(u)
        rv = r.diff(v)
        normal_vector = ru.cross(rv)
        normal_magnitude = sqrt(normal_vector.dot(normal_vector))

        is_vector = isinstance(field, list) and len(field) == 3
        is_scalar = isinstance(field, str) or (isinstance(field, list) and len(field) == 1)

        substitutions = dict(zip(field_syms, r))

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

        result = integrate(integrand, (u, bounds[0][0], bounds[0][1]), (v, bounds[1][0], bounds[1][1])).doit()
        
        # Clean up the result
        result = clean_trig_result(result)
        return str(result)

    except Exception as e:
        return f"Error: {str(e)}"
    
# Directional derivative    
def solve_directional_derivative(expr: str, variables: list, direction: list, point: list = None) -> str:
    try:
        if len(direction) != len(variables):
            return "Error: Direction vector must match the number of variables."
        
        expression = sympify(expr)
        sym_vars = [symbols(v) for v in variables]
        grad = Matrix([diff(expression, var) for var in sym_vars])
        dir_vector = Matrix(direction)
        magnitude = sqrt(sum(c**2 for c in dir_vector))
        if magnitude == 0:
            return "Error: Direction vector cannot be zero."
        
        unit_vector = dir_vector / magnitude
        directional_derivative = grad.dot(unit_vector)
        if point is not None and point != []:
            if len(point) != len(variables):
                return "Error: Point must have the same dimension as variables."
            subs_dict = dict(zip(sym_vars, point))
            # Use symbolic substitution instead of numeric evaluation
            evaluated_value = directional_derivative.subs(subs_dict)
            evaluated_value = clean_trig_result(evaluated_value)
            return str(evaluated_value)
        
        directional_derivative = clean_trig_result(directional_derivative)
        return str(directional_derivative)
    
    except Exception as e:
        return f"Error: {str(e)}"
def solve_greens_theorem(vector_field: list, region_bounds: list, variables: list):
    try:
        x, y = symbols(variables)

        M = sympify(vector_field[0])
        N = sympify(vector_field[1])
        curl_2d = diff(N, x) - diff(M, y)
        (x_lower, x_upper), (y_lower, y_upper) = region_bounds
        result = integrate(integrate(curl_2d, (x, x_lower, x_upper)), (y, y_lower, y_upper))

        # Clean up the result
        result = clean_trig_result(result)
        return str(result)
    
    except Exception as e:
        return f"Error: {str(e)}"
    
def solve_stokes_theorem(vector_field: list, params: list, surface: list, bounds: list, field_vars=("x", "y", "z")) -> str:
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

        x, y, z = symbols(field_vars)
        substitutions = {x: r[0], y: r[1], z: r[2]}
        curl_sub = curl.subs(substitutions)

        result = integrate(curl_sub.dot(normal), (u, bounds[0][0], bounds[0][1]), (v, bounds[1][0], bounds[1][1]))        
        
        # Clean up the result
        result = clean_trig_result(result)
        return str(simplify(result))
    except Exception as e:
        return f"Error: {str(e)}"


def solve_lagrange_multipliers(f_expr: str, g_expr: str, variables: list, h_expr: str = None) -> dict:
    try:
        # Create symbolic variables
        sym_vars = [symbols(v) for v in variables]
        
        # Parse expressions
        f = sympify(f_expr)
        g_constraint = sympify(g_expr)
        
        # Handle constraint format - convert "g = k" to "g - k = 0"
        if hasattr(g_constraint, 'lhs') and hasattr(g_constraint, 'rhs'):
            # It's an equation like x + y + z = 1
            g = g_constraint.lhs - g_constraint.rhs
        else:
            # Assume it's already in the form g(x,y,z) where we want g = 0
            g = g_constraint
        
        # Create Lagrange multiplier symbol
        lam = symbols('lam')  # Using 'lam' instead of 'lambda' to avoid Python keyword
        
        # Compute gradients
        grad_f = [diff(f, var) for var in sym_vars]
        grad_g = [diff(g, var) for var in sym_vars]
        
        # Set up system of equations
        equations = []
        
        # Gradient condition: ∇f = λ∇g
        for i in range(len(sym_vars)):
            equations.append(Eq(grad_f[i], lam * grad_g[i]))
        
        # Constraint: g = 0
        equations.append(Eq(g, 0))
        
        # Variables to solve for
        unknowns = sym_vars + [lam]
        
        # Try to solve the system
        solutions = []
        
        # Method 1: Standard solve
        try:
            sol = solve(equations, unknowns, dict=True)
            if sol:
                solutions.extend(sol)
        except Exception as e:
            pass
        
        # Method 2: Try without dict=True if standard fails
        if not solutions:
            try:
                sol = solve(equations, unknowns)
                if sol and isinstance(sol, list):
                    # Convert to dict format
                    for s in sol:
                        if len(s) == len(unknowns):
                            solution_dict = {unknowns[i]: s[i] for i in range(len(unknowns))}
                            solutions.append(solution_dict)
            except Exception as e:
                pass
        
        # Method 3: Try solving step by step for simple cases
        if not solutions and len(variables) == 2:
            try:
                # For 2D: solve the first two gradient equations for x,y in terms of lambda
                # then substitute into constraint
                x, y = sym_vars
                eq1, eq2, constraint = equations
                
                # Try to solve first two equations for x, y in terms of lambda
                partial_sol = solve([eq1, eq2], [x, y])
                if partial_sol:
                    # Substitute into constraint
                    constraint_sub = constraint.subs(partial_sol)
                    lambda_vals = solve(constraint_sub, lam)
                    
                    for lam_val in lambda_vals:
                        full_sol = partial_sol.copy()
                        full_sol[lam] = lam_val
                        # Substitute lambda back to get numeric values
                        final_sol = {k: v.subs(lam, lam_val) for k, v in full_sol.items()}
                        final_sol[lam] = lam_val
                        solutions.append(final_sol)
            except Exception as e:
                pass
        
        if not solutions:
            return {"error": "Could not solve the optimization problem. The constraint may be incompatible with the function, or the problem may have no critical points."}
        
        # Process and filter solutions
        real_solutions = []
        for i, s in enumerate(solutions):
            try:
                # Create a clean solution dictionary
                clean_sol = {}
                is_valid = True
                
                # Extract variable values (include lambda)
                for var_name in variables + ['lam']:
                    if var_name == 'lam':
                        var_sym = lam
                        result_key = 'lambda'  # Display as 'lambda' in results
                    else:
                        var_sym = symbols(var_name)
                        result_key = var_name
                    
                    if var_sym in s:
                        val = s[var_sym]
                        try:
                            # Try to evaluate to a float
                            numeric_val = float(val.evalf())
                            # Check if it's real (not NaN or infinity)
                            if not (abs(numeric_val) == float('inf') or numeric_val != numeric_val):
                                clean_sol[result_key] = round(numeric_val, 6)
                            else:
                                is_valid = False
                                break
                        except:
                            # If can't evaluate to float, keep symbolic but clean it first
                            if val.is_real is not False:  # Not explicitly complex
                                val = clean_trig_result(val)
                                clean_sol[result_key] = str(val)
                            else:
                                is_valid = False
                                break
                    elif var_name != 'lam':  # lambda is optional, variables are required
                        is_valid = False
                        break
                
                if is_valid and clean_sol:
                    # Calculate function value at this point
                    var_substitutions = {symbols(var): clean_sol[var] for var in variables}
                    f_val = f.subs(var_substitutions)
                    
                    try:
                        clean_sol["f_value"] = round(float(f_val.evalf()), 6)
                    except:
                        f_val = clean_trig_result(f_val)
                        clean_sol["f_value"] = str(f_val)
                    
                    # Check constraint satisfaction
                    g_val = g.subs(var_substitutions)
                    constraint_error = abs(float(g_val.evalf())) if g_val.is_number else float('inf')
                    
                    if constraint_error < 1e-10:  # Constraint is satisfied
                        real_solutions.append(clean_sol)
                
            except Exception as eval_error:
                continue
        
        if not real_solutions:
            return {"error": "No valid real solutions found. The optimization problem may have no feasible critical points."}
        
        return real_solutions
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"Error solving Lagrange multipliers: {str(e)}"}
