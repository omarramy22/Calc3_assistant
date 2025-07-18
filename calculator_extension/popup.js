// Wait until the popup is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  const courseSelect = document.getElementById("course");
  const operationSelect = document.getElementById("operation");
  const mathField = document.getElementById("mathfield");
  const variablesInput = document.getElementById("variables");
  const extraInput = document.getElementById("extra");
  const resultBox = document.getElementById("result");
  const calcButton = document.getElementById("calculate");
  const operationSection = document.getElementById("operation-section");

  // Helper: show/hide elements
  function showElement(el) {
    el.parentElement.style.display = "block";
  }

  function hideElement(el) {
    el.parentElement.style.display = "none";
  }

  // Helper: parse "x in [0,1], y in [0,2]" → [["x", 0, 1], ["y", 0, 2]]
  function parseLimits(input) {
    try {
      const terms = input.split(",").map(s => s.trim());
      return terms.map(term => {
        const [varName, range] = term.split("in").map(s => s.trim());
        const bounds = range.replace("[", "").replace("]", "").split(/\s*[,;]\s*/);
        return [varName, parseFloat(bounds[0]), parseFloat(bounds[1])];
      });
    } catch {
      return [];
    }
  }

  // Helper: parse "x y z" or "x, y, z" → ["x", "y", "z"]
  function parseVariables(input) {
    return input.split(/[\s,]+/).map(s => s.trim()).filter(s => s.length > 0);
  }

  // Dynamically update visible fields based on operation
  operationSelect.addEventListener("change", function () {
    const op = operationSelect.value;

    // Reset
    mathField.value = "";
    variablesInput.value = "";
    extraInput.value = "";

    // Show/hide fields based on operation
    showElement(mathField);
    hideElement(extraInput);
    showElement(variablesInput);

    if (["line_integral", "surface_integral", "directional_derivative", "lagrange_multipliers", "multiple_integral", "stokes_theorem"].includes(op)) {
      showElement(extraInput);
    }

    // Custom placeholders
    switch (op) {
      case "partial_derivative":
        mathField.placeholder = "e.g. 2xy + sin(t)";
        variablesInput.placeholder = "e.g. x t";
        extraInput.placeholder = ""; break;

      case "gradient":
        variablesInput.placeholder = "e.g. x y z";
        break;

      case "multiple_integral":
        extraInput.placeholder = "e.g. x in [0,1], y in [0,2]";
        break;

      case "directional_derivative":
        extraInput.placeholder = "Direction vector: e.g. 1, 1";
        break;

      case "line_integral":
        extraInput.placeholder = "Param: t; Curve: t, t^2, t^3";
        break;

      case "surface_integral":
        extraInput.placeholder = "Params: u, v; Surface: u, v, u*v; Bounds: u [0,1], v [0,2]";
        break;

      case "lagrange_multipliers":
        mathField.placeholder = "f(x,y)";
        variablesInput.placeholder = "x y";
        extraInput.placeholder = "Constraint: g(x,y)";
        break;
    }
  });

  courseSelect.addEventListener("change", function () {
  const selected = courseSelect.value;

    console.log("Course selected raw:", courseSelect.selectedIndex, selected, operationSection);

  if (selected && selected === "calc3") {
    operationSection.style.display = "block";
    console.log("Showing operation section for Calculus 3");
  } else {
    operationSection.style.display = "none";
  }
});
  // Handle Calculate button click
  calcButton.addEventListener("click", async function () {
    const operation = operationSelect.value;
    const expr = mathField.getValue();  // Get LaTeX directly from MathLive
    const vars = parseVariables(variablesInput.value);
    const extra = extraInput.value;

    let payload = { operation, expression: expr, variables: vars };

    // Add operation-specific input handling
    if (operation === "multiple_integral") {
      payload["limits"] = parseLimits(extra);
    } else if (operation === "directional_derivative") {
      const dir = extra.split(/[\s,]+/).map(Number);
      payload["direction"] = dir;
    } else if (operation === "lagrange_multipliers") {
      payload["constraint"] = mathField.getValue();  // Get constraint from MathLive
    } else if (operation === "line_integral") {
      const parts = extra.split(";");
      payload["param"] = parts[0].trim();  // e.g. t
      payload["curve"] = parts[1].split(",").map(s => s.trim());
    } else if (operation === "surface_integral" || operation === "stokes_theorem") {
      const parts = extra.split(";");
      payload["params"] = parseVariables(parts[0]);       // e.g. u, v
      payload["surface"] = parts[1].split(",").map(e => mathField.getValue());  // Get surface from MathLive
      if (parts[2]) {
        payload["bounds"] = parseLimits(parts[2]);
      }
    }

    // Send POST request to backend
    try {
      const res = await fetch("http://localhost:5000/solve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      resultBox.textContent = data.result || JSON.stringify(data);
    } catch (err) {
      resultBox.textContent = "Error: " + err.message;
    }
  });
  // Re-run logic if course was already selected (e.g. after reload)
    if (courseSelect.value === "calc3") {
        operationSection.style.display = "block";
    }
});
