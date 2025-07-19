document.addEventListener("DOMContentLoaded", function () {
  const courseSelect = document.getElementById("course");
  const operationSection = document.getElementById("operation-section");
  const mathField = document.getElementById("mathfield");
  const result = document.getElementById("result");

  // LaTeX templates for each operation
  const latexTemplates = {
    partial_derivative: '\\frac{\\partial}{\\partial x} f(x, y)',
    gradient: '\\nabla f(x, y)',
    multiple_integral: '\\iint_R f(x, y)\\,dx\\,dy',
    divergence: '\\nabla \\cdot \\vec{F}(x, y, z)',
    curl: '\\nabla \\times \\vec{F}(x, y, z)',
    line_integral: '\\oint_C \\vec{F} \\cdot d\\vec{r}',
    surface_integral: '\\iint_S \\vec{F} \\cdot d\\vec{S}',
    directional_derivative: '\\nabla f(x, y) \\cdot \\vec{u}',
    greens_theorem: '\\oint_C \\vec{F} \\cdot d\\vec{r} = \\iint_R \\left(\\frac{\\partial Q}{\\partial x} - \\frac{\\partial P}{\\partial y}\\right)\\,dx\\,dy',
    stokes_theorem: '\\iint_S \\nabla \\times \\vec{F} \\cdot d\\vec{S} = \\oint_C \\vec{F} \\cdot d\\vec{r}',
    lagrange_multipliers: '\\nabla f(x, y) = \\lambda \\nabla g(x, y)',
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
      mathField.setValue(latexTemplates[op] || "");
      localStorage.setItem("savedExpression", mathField.getValue());
    });
  });

  // Handle Calculate button
  document.getElementById("calculate").addEventListener("click", async () => {
    const latexInput = mathField.getValue().trim();

    if (!latexInput) {
      result.textContent = "Please enter a valid expression.";
      return;
    }

    result.textContent = "Calculating...";

    try {
      const response = await fetch("http://localhost:5000/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ latex: latexInput }),
      });

      const data = await response.json();

      if (response.ok) {
        result.textContent = data.result || "No result returned.";
      } else {
        result.textContent = data.error || "An error occurred.";
      }
    } catch (err) {
      result.textContent = "Failed to connect to backend.";
      console.error(err);
    }
  });
});
