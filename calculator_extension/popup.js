document.addEventListener("DOMContentLoaded", function () {
  const courseSelect = document.getElementById("course");
  const operationSection = document.getElementById("operation-section");
  const mathField = document.getElementById("mathfield");
  const Additional_mathField = document.getElementById("mathfield_additional");
  const result = document.getElementById("result");

  // LaTeX templates for each operation
  const latexTemplates = {
    partial_derivative: '\\frac{\\partial}{\\partial x} f(x, y)',
    arc_length: '\\htmlClass{arc}{\\int_{0}^{1} \\sqrt{\\left(\\frac{d}{dt}x(t)\\right)^2 + \\left(\\frac{d}{dt}y(t)\\right)^2 + \\left(\\frac{d}{dt}z(t)\\right)^2} \\, dt}',
    gradient: '\\htmlClass{gradient}{\\nabla f(x, y, z)}',
    double_integral: '\\int_{0}^{1} \\int_{0}^{1}  ( f(x, y) )  \\, dy\\, dx',
    double_integral_polar:'\\int_{0}^{2\\pi} \\int_{0}^{1} ( r * f(r, \\theta) ) \\, dr\\, d\\theta',
    triple_integral: '\\int_{0}^{1} \\int_{0}^{1} \\int_{0}^{1} ( f(x, y, z) ) \\, dz\\, dy\\, dx',
    triple_integral_polar: '\\int_{0}^{\\pi} \\int_{0}^{1} \\int_{0}^{1} ( r * f(r, \\theta, z) ) \\, dz\\, dr \\, d\\theta',
    triple_integral_cylindrical: '\\int_{0}^{\\pi} \\int_{0}^{\\pi} \\int_{0}^{1} ( \\rho^2 * \\sin(\\phi) * f(\\rho, \\theta, \\phi) ) \\, d\\rho\\, d\\theta\\, d\\phi',
    divergence: '\\nabla \\cdot \\vec{F}(x, y, z)',
    curl: '\\nabla \\times \\vec{F}(x, y, z)',
    scalar_line_integral: '\\htmlClass{scalar_line_integral}{\\int_{0}^{1} ( f(x, y, z) ) \\, ds,\\vec{r}(t) = [2t, -2t, t]}',
    vector_line_integral: '\\htmlClass{vector_line_integral}{\\int_{0}^{1} ([x, y, z]) \\cdot \\frac{d\\vec{r}}{dt} \\, dt,\\vec{r}(t) = [2t, -2t, t]}',
    surface_integral: '\\iint_S \\vec{F} \\cdot d\\vec{S}',
    directional_derivative: '\\htmlClass{directional}{\\nabla f(x, y, z) \\cdot (r_x, r_y, r_z)}',
    greens_theorem: '\\oint_C \\vec{F} \\cdot d\\vec{r} = \\iint_R \\left(\\frac{\\partial Q}{\\partial x} - \\frac{\\partial P}{\\partial y}\\right)\\,dx\\,dy',
    stokes_theorem: '\\iint_S \\nabla \\times \\vec{F} \\cdot d\\vec{S} = \\oint_C \\vec{F} \\cdot d\\vec{r}',
    lagrange_multipliers: '\\htmlClass{lagrange}{\\nabla f(x, y, z) = \\lambda \\nabla g(x, y, z), g(x, y, z) = k}',
  };
  

  const savedCourse = localStorage.getItem("selectedCourse");
  if (savedCourse) {
    courseSelect.value = savedCourse;
  }

  // Save selection and toggle operation section
  courseSelect.addEventListener("change", () => {
    const selected = courseSelect.value;
    localStorage.setItem("selectedCourse", selected);

    if (selected === "calc3") {
      operationSection.style.display = "block";
    } else {
      operationSection.style.display = "none";
    }
  });

  // Restore course selection from localStorage
  if (savedCourse) {
    courseSelect.dispatchEvent(new Event("change"));
  }

  // Initialize math field with previous value
  const savedExpression = localStorage.getItem("savedExpression");
  if (savedExpression) {
    mathField.setValue(savedExpression);
  }

  // store the value in the local storage on input
  mathField.addEventListener("input", () => {
  localStorage.setItem("savedExpression", mathField.getValue());
  });

  // Handle operation button clicks
  document.querySelectorAll("#operation-buttons button").forEach((btn) => {
    btn.addEventListener("click", () => {
      const op = btn.dataset.op;
      mathField.focus();
      mathField.insert(latexTemplates[op] || "");
      localStorage.setItem("savedExpression", mathField.getValue());
    });
  });

  // Handle Calculate button
  document.getElementById("calculate").addEventListener("click", async () => {
    const latexInput = mathField.getValue().trim();
    const safeLatex = latexInput.replace(/(\w)\^\{\s*\}/g, "$1");


    if (!safeLatex || safeLatex === "") {
      result.textContent = "Please enter a valid expression.";
      return;
    }

    result.textContent = "Calculating...";

    try {
      const response = await fetch("http://localhost:5000/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ latex: safeLatex }),
      });

      const data = await response.json();

      if (response.ok) {
        if (Array.isArray(data.result)) {
          result.innerHTML = data.result
            .map(
              (sol, idx) =>
                `Solution ${idx + 1}: x = ${sol.x}, y = ${sol.y}, λ = ${sol.λ}, f_max/min = ${sol.f_value}`
            )
            .join("<br>");
        } else if (typeof data.result === "object") {
          result.textContent = JSON.stringify(data.result, null, 2);
        } else {
          result.textContent = data.result || "No result returned.";
        }
      }
      else {
        result.textContent = data.error || "An error occurred.";
      }
    } catch (err) {
      result.textContent = "Failed to connect to backend, check the input and try again.";
      console.error(err);
    }
  });
});
