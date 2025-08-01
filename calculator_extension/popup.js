document.addEventListener("DOMContentLoaded", function () {
  const courseSelect = document.getElementById("course");
  const operationSection = document.getElementById("operation-section");
  const operationSelect = document.getElementById("operation-select");
  const inputFields = document.getElementById("input-fields");
  const result = document.getElementById("result");

  // Operation configurations - defines input fields for each operation
  const operationConfigs = {
    partial_derivative: {
      fields: [
        { id: 'function', label: 'Function f(x,y,z)', placeholder: 'x^2 + y^2 + z^2' },
        { id: 'variables', label: 'differentiation Variables (comma-separated)', placeholder: 'x, y' }
      ]
    },
    gradient: {
      fields: [
        { id: 'function', label: 'Function f(x,y,z)', placeholder: 'x^2 + y^2 + z^2' }
      ]
    },
    double_integral: {
      fields: [
        { id: 'function', label: 'Function f(x,y)', placeholder: '' }
      ],
      hasLatexButtons: true
    },
    double_integral_polar: {
      fields: [
        { id: 'function', label: 'Function f(r,θ)', placeholder: '' }
      ],
      hasLatexButtons: true
    },
    triple_integral: {
      fields: [
        { id: 'function', label: 'Function f(x,y,z)', placeholder: '' }
      ],
      hasLatexButtons: true
    },
    triple_integral_polar: {
      fields: [
        { id: 'function', label: 'Function f(r,θ,z)', placeholder: '' }
      ],
      hasLatexButtons: true
    },
    triple_integral_cylindrical: {
      fields: [
        { id: 'function', label: 'Function f(ρ,θ,φ)', placeholder: '' }
      ],
      hasLatexButtons: true
    },
    arc_length: {
      fields: [
        { id: 'parametric', label: 'Parametric Functions', placeholder: '2t, 4t, t^2' },
        { id: 'parameter', label: 'Parameter', placeholder: 't' },
        { id: 'limits', label: 'Parameter Limits', placeholder: '0, 1' }
      ]
    },
    divergence: {
      fields: [
        { id: 'vector_field', label: 'Vector Field F(x,y,z)', placeholder: 'P(x,y,z), Q(x,y,z), R(x,y,z)' }
      ]
    },
    curl: {
      fields: [
        { id: 'vector_field', label: 'Vector Field F(x,y,z)', placeholder: 'P(x,y,z), Q(x,y,z), R(x,y,z)' }
      ]
    },
    scalar_line_integral: {
      fields: [
        { id: 'function', label: 'Scalar Function f(x,y,z)', placeholder: 'x^2 + y^2 + z^2' },
        { id: 'curve', label: 'Parametric Curve r(t)', placeholder: '2t, -2t, t' },
        { id: 'limits', label: 'Parameter Limits', placeholder: '0, 1' }
      ]
    },
    vector_line_integral: {
      fields: [
        { id: 'vector_field', label: 'Vector Field F(x,y,z)', placeholder: 'x, y, z' },
        { id: 'curve', label: 'Parametric Curve r(t)', placeholder: '2t, -2t, t' },
        { id: 'limits', label: 'Parameter Limits', placeholder: '0, 1' }
      ]
    },
    surface_integral: {
      fields: [
        { id: 'vector_field', label: 'Vector Field F(x,y,z)', placeholder: 'P(x,y,z), Q(x,y,z), R(x,y,z)' },
        { id: 'surface', label: 'Surface S', placeholder: 'z = x^2 + y^2' }
      ]
    },
    directional_derivative: {
      fields: [
        { id: 'function', label: 'Function f(x,y,z)', placeholder: 'x^2 + y^2 + z^2' },
        { id: 'direction', label: 'Direction Vector', placeholder: '1, 1, 1' },
        { id: 'point', label: 'Point (x,y,z)', placeholder: '1, 2, 3' }
      ]
    },
    greens_theorem: {
      fields: [
        { id: 'vector_field', label: 'Vector Field F = [P, Q]', placeholder: 'x*y, x^2 + y^2' },
        { id: 'curve', label: 'Closed Curve C', placeholder: 'x^2 + y^2 = 4' }
      ]
    },
    stokes_theorem: {
      fields: [
        { id: 'vector_field', label: 'Vector Field F(x,y,z)', placeholder: 'y*z, x*z, x*y' },
        { id: 'surface', label: 'Surface S with boundary C', placeholder: 'z = x^2 + y^2, z ≤ 1' }
      ]
    },
    lagrange_multipliers: {
      fields: [
        { id: 'function', label: 'Function to optimize f(x,y,z)', placeholder: 'x^2 + y^2 + z^2' },
        { id: 'constraint', label: 'Constraint g(x,y,z) = k', placeholder: 'x + y + z - 1' }
      ]
    }
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

  // Function to create input fields based on operation
  function createInputFields(operation) {
    const config = operationConfigs[operation];
    if (!config) return;

    inputFields.innerHTML = '';
    inputFields.style.display = 'block';

    config.fields.forEach((field, index) => {
      const fieldContainer = document.createElement('div');
      fieldContainer.className = 'field-container';
      fieldContainer.style.marginBottom = '15px';

      const label = document.createElement('label');
      label.textContent = field.label;
      label.style.display = 'block';
      label.style.marginBottom = '5px';
      label.style.fontWeight = 'bold';

      const mathField = document.createElement('math-field');
      mathField.id = `input-${field.id}`;
      mathField.setAttribute('virtual-keyboard-mode', 'manual');
      mathField.style.width = '100%';
      mathField.style.minHeight = '40px';
      
      // Set placeholder using the value property for visibility
      mathField.value = field.placeholder;
      mathField.style.color = '#999';
      
      // Restore saved value from localStorage
      const savedValue = localStorage.getItem(`calc3_${operation}_${field.id}`);
      
      // Special handling for parameter field - always restore saved value even if it matches placeholder
      if (field.id === 'parameter' && operation === 'arc_length') {
        if (savedValue) {
          mathField.setValue(savedValue);
          mathField.style.color = '#000';
        }
      } else {
        // Normal handling for other fields - don't restore if it matches placeholder
        if (savedValue && savedValue !== field.placeholder) {
          mathField.setValue(savedValue);
          mathField.style.color = '#000';
        }
      }
      
      // Handle focus and blur to manage placeholder behavior
      mathField.addEventListener('focus', function() {
        if (this.getValue() === field.placeholder) {
          this.setValue('');
          this.style.color = '#000';
        }
      });
      
      mathField.addEventListener('blur', function() {
        const currentValue = this.getValue().trim();
        
        // Special handling for parameter field - don't treat 't' as empty even if it matches placeholder
        if (field.id === 'parameter' && operation === 'arc_length') {
          if (currentValue === '') {
            this.setValue(field.placeholder);
            this.style.color = '#999';
            localStorage.removeItem(`calc3_${operation}_${field.id}`);
          } else {
            // Always save parameter value, even if it's 't'
            localStorage.setItem(`calc3_${operation}_${field.id}`, currentValue);
          }
        } else {
          // Normal handling for other fields
          if (currentValue === '') {
            this.setValue(field.placeholder);
            this.style.color = '#999';
            localStorage.removeItem(`calc3_${operation}_${field.id}`);
          } else {
            localStorage.setItem(`calc3_${operation}_${field.id}`, currentValue);
          }
        }
      });
      
      // Also save on input changes
      mathField.addEventListener('input', function() {
        const currentValue = this.getValue().trim();
        
        // Special handling for parameter field
        if (field.id === 'parameter' && operation === 'arc_length') {
          if (currentValue !== '') {
            localStorage.setItem(`calc3_${operation}_${field.id}`, currentValue);
          }
        } else {
          // Normal handling for other fields
          if (currentValue !== '' && currentValue !== field.placeholder) {
            localStorage.setItem(`calc3_${operation}_${field.id}`, currentValue);
          }
        }
      });

      fieldContainer.appendChild(label);
      fieldContainer.appendChild(mathField);

      // Add LaTeX helper buttons for integral operations
      if (config.hasLatexButtons && field.id === 'function') {
        const buttonContainer = document.createElement('div');
        buttonContainer.style.marginTop = '10px';
        buttonContainer.style.display = 'flex';
        buttonContainer.style.gap = '5px';
        buttonContainer.style.flexWrap = 'wrap';

        // Add integral template button based on operation type
        let integralButton;
        if (operation === 'double_integral') {
          integralButton = {
            symbol: '∬ Generate Double Integral',
            latex: '\\int_{0}^{1} \\int_{0}^{1} ( f(x, y) ) \\, dy\\, dx'
          };
        } else if (operation === 'double_integral_polar') {
          integralButton = {
            symbol: '∬ Generate Polar Double Integral',
            latex: '\\int_{0}^{2\\pi} \\int_{0}^{1} ( r * f(r, \\theta) ) \\, dr\\, d\\theta'
          };
        } else if (operation === 'triple_integral') {
          integralButton = {
            symbol: '∭ Generate Triple Integral',
            latex: '\\int_{0}^{1} \\int_{0}^{1} \\int_{0}^{1} ( f(x, y, z) ) \\, dz\\, dy\\, dx'
          };
        } else if (operation === 'triple_integral_polar') {
          integralButton = {
            symbol: '∭ Generate Cylindrical Integral',
            latex: '\\int_{0}^{\\pi} \\int_{0}^{1} \\int_{0}^{1} ( r \\cdot f(r, \\theta, z) ) \\, dz\\, dr \\, d\\theta'
          };
        } else if (operation === 'triple_integral_cylindrical') {
          integralButton = {
            symbol: '∭ Generate Spherical Integral',
            latex: '\\int_{0}^{\\pi} \\int_{0}^{\\pi} \\int_{0}^{1} ( \\rho^2 \\cdot \\sin(\\phi) \\cdot f(\\rho, \\theta, \\phi) ) \\, d\\rho\\, d\\theta\\, d\\phi'
          };
        }

        if (integralButton) {
          const templateBtn = document.createElement('button');
          templateBtn.textContent = integralButton.symbol;
          templateBtn.type = 'button';
          templateBtn.style.padding = '8px 12px';
          templateBtn.style.fontSize = '13px';
          templateBtn.style.backgroundColor = '#4CAF50';
          templateBtn.style.color = 'white';
          templateBtn.style.border = 'none';
          templateBtn.style.borderRadius = '5px';
          templateBtn.style.cursor = 'pointer';
          templateBtn.style.fontWeight = 'bold';
          templateBtn.style.marginBottom = '10px';
          templateBtn.style.width = '100%';
          
          templateBtn.addEventListener('click', () => {
            // Clear the field and insert the full template
            mathField.setValue(integralButton.latex);
            mathField.style.color = '#000';
            mathField.focus();
          });
          
          buttonContainer.appendChild(templateBtn);
        }

        fieldContainer.appendChild(buttonContainer);
      }

      inputFields.appendChild(fieldContainer);
    });

    // Add calculate button
    const calculateBtn = document.createElement('button');
    calculateBtn.id = 'calculate';
    calculateBtn.textContent = 'Calculate';
    calculateBtn.style.marginTop = '20px';
    calculateBtn.style.padding = '10px 20px';
    calculateBtn.style.backgroundColor = '#007bff';
    calculateBtn.style.color = 'white';
    calculateBtn.style.border = 'none';
    calculateBtn.style.borderRadius = '5px';
    calculateBtn.style.cursor = 'pointer';

    inputFields.appendChild(calculateBtn);

    // Add event listener to calculate button
    calculateBtn.addEventListener('click', handleCalculate);
  }

  // Handle operation selection
  operationSelect.addEventListener("change", () => {
    const selectedOperation = operationSelect.value;
    if (selectedOperation) {
      createInputFields(selectedOperation);
      localStorage.setItem("selectedOperation", selectedOperation);
    } else {
      inputFields.style.display = 'none';
    }
  });

  // Restore operation selection from localStorage
  const savedOperation = localStorage.getItem("selectedOperation");
  if (savedOperation) {
    operationSelect.value = savedOperation;
    operationSelect.dispatchEvent(new Event("change"));
  }

  // Function to display error messages in a user-friendly format
  function displayError(errorMessage) {
    // Clear previous results
    result.innerHTML = '';
    
    // Create a container for the error
    const errorContainer = document.createElement('div');
    errorContainer.style.cssText = `
      margin-top: 20px;
      padding: 15px;
      background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
      border: 2px solid #fc8181;
      border-radius: 12px;
      box-shadow: 0 4px 6px rgba(252, 129, 129, 0.2);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 100%;
      box-sizing: border-box;
      overflow: hidden;
      word-wrap: break-word;
    `;
    
    // Add error title
    const titleElement = document.createElement('h4');
    titleElement.textContent = '❌ Error:';
    titleElement.style.cssText = `
      margin: 0 0 15px 0;
      color: #c53030;
      font-size: 18px;
      font-weight: 600;
      border-bottom: 2px solid #fc8181;
      padding-bottom: 8px;
      display: inline-block;
    `;
    errorContainer.appendChild(titleElement);
    
    // Add error message as plain text (not MathLive)
    const errorText = document.createElement('div');
    errorText.textContent = errorMessage;
    errorText.style.cssText = `
      background-color: #ffffff;
      border: 1px solid #fc8181;
      border-radius: 8px;
      padding: 12px;
      font-size: 14px;
      line-height: 1.5;
      color: #2d3748;
      font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
      white-space: pre-wrap;
      word-break: break-word;
      box-shadow: inset 0 1px 2px rgba(0,0,0,0.075);
    `;
    errorContainer.appendChild(errorText);
    
    result.appendChild(errorContainer);
  }

  // Function to display results based on operation type
  function displayResult(resultData, operation) {
    // Clear previous results
    result.innerHTML = '';
    
    // Create a container for the result
    const resultContainer = document.createElement('div');
    resultContainer.style.cssText = `
      margin-top: 20px;
      padding: 15px;
      background: linear-gradient(135deg, #f8f9fa 0%, #f1f3f4 100%);
      border: 2px solid #e9ecef;
      border-radius: 12px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 100%;
      box-sizing: border-box;
      overflow: hidden;
      word-wrap: break-word;
    `;
    
    // Add title
    const titleElement = document.createElement('h4');
    titleElement.textContent = 'Result:';
    titleElement.style.cssText = `
      margin: 0 0 15px 0;
      color: #343a40;
      font-size: 18px;
      font-weight: 600;
      border-bottom: 2px solid #007bff;
      padding-bottom: 8px;
      display: inline-block;
    `;
    resultContainer.appendChild(titleElement);
    
    if (Array.isArray(resultData)) {
      // Handle different operations differently
      if (operation === 'lagrange_multipliers') {
        // For Lagrange multipliers, show detailed solutions
        resultData.forEach((sol, idx) => {
          const solutionDiv = document.createElement('div');
          solutionDiv.style.cssText = `
            margin-bottom: 12px;
            padding: 8px;
            background-color: white;
            border-radius: 8px;
            border-left: 4px solid #007bff;
          `;
          
          const solutionLabel = document.createElement('strong');
          solutionLabel.textContent = `Solution ${idx + 1}:`;
          solutionLabel.style.cssText = `
            display: block;
            margin-bottom: 6px;
            color: #495057;
            font-size: 13px;
          `;
          
          const mathResult = document.createElement('math-field');
          mathResult.setAttribute('read-only', 'true');
          mathResult.style.cssText = `
            width: 100%;
            max-width: 100%;
            min-height: 45px;
            background-color: #ffffff;
            border: 1px solid #ced4da;
            border-radius: 6px;
            padding: 10px;
            font-size: 13px;
            line-height: 1.4;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.075);
            box-sizing: border-box;
            overflow: auto;
          `;
          
          if (typeof sol === 'object') {
            mathResult.setValue(JSON.stringify(sol, null, 2));
          } else {
            // Clean up LaTeX formatting for better display
            let cleanSol = sol.toString();
            cleanSol = cleanSol
              .replace(/\*\*/g, '^')  // Convert ** to ^
              .replace(/sqrt\(([^)]+)\)/g, '\\sqrt{$1}')  // Convert sqrt(expr) to \sqrt{expr}
              .replace(/\*(?=[a-zA-Z])/g, '')  // Remove * before variables (x*y -> xy)
              .replace(/([a-zA-Z0-9])\*(?=[a-zA-Z])/g, '$1')  // Remove * between variables/numbers and variables
              .replace(/\$\$/g, '');  // Remove $$ delimiters if present
            
            mathResult.setValue(cleanSol);
          }
          
          solutionDiv.appendChild(solutionLabel);
          solutionDiv.appendChild(mathResult);
          resultContainer.appendChild(solutionDiv);
        });
      } else if (['curl', 'gradient', 'divergence'].includes(operation)) {
        // For vector operations, display as vector notation
        const mathResult = document.createElement('math-field');
        mathResult.setAttribute('read-only', 'true');
        mathResult.style.cssText = `
          width: 100%;
          max-width: 100%;
          min-height: 55px;
          background-color: #ffffff;
          border: 2px solid #28a745;
          border-radius: 8px;
          padding: 12px;
          font-size: 15px;
          font-weight: 500;
          text-align: center;
          box-shadow: 0 2px 4px rgba(40, 167, 69, 0.2);
          box-sizing: border-box;
          overflow: auto;
        `;
        
        if (resultData.length === 3) {
          // 3D vector
          mathResult.setValue(`\\langle ${resultData[0]}, ${resultData[1]}, ${resultData[2]} \\rangle`);
        } else if (resultData.length === 2) {
          // 2D vector
          mathResult.setValue(`\\langle ${resultData[0]}, ${resultData[1]} \\rangle`);
        } else {
          // Fallback for other array lengths
          mathResult.setValue(`\\langle ${resultData.join(', ')} \\rangle`);
        }
        
        resultContainer.appendChild(mathResult);
      } else {
        // For other array results, show as numbered solutions
        resultData.forEach((sol, idx) => {
          const solutionDiv = document.createElement('div');
          solutionDiv.style.cssText = `
            margin-bottom: 12px;
            padding: 8px;
            background-color: white;
            border-radius: 8px;
            border-left: 4px solid #6c757d;
          `;
          
          const solutionLabel = document.createElement('strong');
          solutionLabel.textContent = `Solution ${idx + 1}:`;
          solutionLabel.style.cssText = `
            display: block;
            margin-bottom: 6px;
            color: #495057;
            font-size: 13px;
          `;
          
          const mathResult = document.createElement('math-field');
          mathResult.setAttribute('read-only', 'true');
          mathResult.style.cssText = `
            width: 100%;
            max-width: 100%;
            min-height: 45px;
            background-color: #ffffff;
            border: 1px solid #ced4da;
            border-radius: 6px;
            padding: 10px;
            font-size: 13px;
            line-height: 1.4;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.075);
            box-sizing: border-box;
            overflow: auto;
          `;
          
          // Clean up LaTeX formatting for better display
          let cleanSol = sol.toString();
          cleanSol = cleanSol
            .replace(/\*\*/g, '^')  // Convert ** to ^
            .replace(/sqrt\(([^)]+)\)/g, '\\sqrt{$1}')  // Convert sqrt(expr) to \sqrt{expr}
            .replace(/\*(?=[a-zA-Z])/g, '')  // Remove * before variables (x*y -> xy)
            .replace(/([a-zA-Z0-9])\*(?=[a-zA-Z])/g, '$1')  // Remove * between variables/numbers and variables
            .replace(/\$\$/g, '');  // Remove $$ delimiters if present
          
          mathResult.setValue(cleanSol);
          
          solutionDiv.appendChild(solutionLabel);
          solutionDiv.appendChild(mathResult);
          resultContainer.appendChild(solutionDiv);
        });
      }
    } else {
      // Single result
      const mathResult = document.createElement('math-field');
      mathResult.setAttribute('read-only', 'true');
      mathResult.style.cssText = `
        width: 100%;
        max-width: 100%;
        min-height: 55px;
        background-color: #ffffff;
        border: 2px solid #17a2b8;
        border-radius: 8px;
        padding: 12px;
        font-size: 15px;
        font-weight: 500;
        text-align: center;
        box-shadow: 0 2px 4px rgba(23, 162, 184, 0.2);
        box-sizing: border-box;
        overflow: auto;
      `;
      
      if (typeof resultData === "object") {
        mathResult.setValue(JSON.stringify(resultData, null, 2));
      } else {
        // Clean up the LaTeX formatting for better display
        let cleanResult = resultData.toString() || "No result returned.";
        
        // Convert Python-style expressions to proper LaTeX more carefully
        cleanResult = cleanResult
          .replace(/\*\*/g, '^')  // Convert ** to ^
          .replace(/sqrt\(([^)]+)\)/g, '\\sqrt{$1}')  // Convert sqrt(expr) to \sqrt{expr}
          .replace(/\*(?=[a-zA-Z])/g, '')  // Remove * before variables (x*y -> xy)
          .replace(/([a-zA-Z0-9])\*(?=[a-zA-Z])/g, '$1')  // Remove * between variables/numbers and variables
          .replace(/\$\$/g, '');  // Remove $$ delimiters if present
        
        mathResult.setValue(cleanResult);
      }
      
      resultContainer.appendChild(mathResult);
    }
    
    // Add copy button
    const copyBtn = document.createElement('button');
    copyBtn.textContent = '📋 Copy Result';
    copyBtn.style.cssText = `
      margin-top: 15px;
      padding: 12px 20px;
      background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-size: 14px;
      font-weight: 600;
      transition: all 0.3s ease;
      box-shadow: 0 2px 4px rgba(40, 167, 69, 0.3);
      width: 100%;
    `;
    
    // Add hover effect
    copyBtn.addEventListener('mouseenter', () => {
      copyBtn.style.transform = 'translateY(-2px)';
      copyBtn.style.boxShadow = '0 4px 8px rgba(40, 167, 69, 0.4)';
    });
    
    copyBtn.addEventListener('mouseleave', () => {
      copyBtn.style.transform = 'translateY(0)';
      copyBtn.style.boxShadow = '0 2px 4px rgba(40, 167, 69, 0.3)';
    });
    
    copyBtn.addEventListener('click', () => {
      let textToCopy = '';
      
      if (Array.isArray(resultData)) {
        if (['curl', 'gradient', 'divergence'].includes(operation)) {
          if (resultData.length === 3) {
            textToCopy = `<${resultData[0]}, ${resultData[1]}, ${resultData[2]}>`;
          } else if (resultData.length === 2) {
            textToCopy = `<${resultData[0]}, ${resultData[1]}>`;
          } else {
            textToCopy = `<${resultData.join(', ')}>`;
          }
        } else {
          textToCopy = resultData.map((sol, idx) => `Solution ${idx + 1}: ${sol}`).join('\n');
        }
      } else {
        textToCopy = resultData.toString();
      }
      
      navigator.clipboard.writeText(textToCopy).then(() => {
        copyBtn.textContent = '✅ Copied!';
        setTimeout(() => {
          copyBtn.textContent = '📋 Copy Result';
        }, 2000);
      }).catch(() => {
        copyBtn.textContent = '❌ Copy Failed';
        setTimeout(() => {
          copyBtn.textContent = '📋 Copy Result';
        }, 2000);
      });
    });
    
    resultContainer.appendChild(copyBtn);
    
    result.appendChild(resultContainer);
  }

  // Handle Calculate button
  async function handleCalculate() {
    const selectedOperation = operationSelect.value;
    if (!selectedOperation) {
      displayError("Please select an operation.");
      return;
    }

    const config = operationConfigs[selectedOperation];
    const inputData = { operation: selectedOperation };

    // Collect input values, ignoring placeholder text
    config.fields.forEach(field => {
      const mathField = document.getElementById(`input-${field.id}`);
      if (mathField) {
        // Try to get plain text instead of LaTeX
        let value = '';
        let rawValue = '';
        
        try {
          // Get the raw LaTeX value first for debugging
          rawValue = mathField.getValue();
          
          // Try different methods to get plain text
          if (mathField.expression && mathField.expression !== rawValue) {
            value = mathField.expression;
          } else if (mathField.value && mathField.value !== rawValue) {
            value = mathField.value;
          } else {
            // Use the raw LaTeX value - backend will handle conversion
            value = rawValue;
          }
        } catch (e) {
          value = mathField.getValue();
        }
        
        value = value.trim();
                
        // For arc length parameter field, handle specially
        if (selectedOperation === 'arc_length' && field.id === 'parameter') {
          // If value is empty, use 't' as default
          // But if user actually typed 't', keep it (don't treat as placeholder)
          if (!value) {
            value = 't';
          }
          // If user explicitly typed 't', keep it as is (no special handling needed)
        } else {
          // For other fields, empty placeholder means empty value
          if (value === field.placeholder) {
            value = '';
          }
        }
        
        inputData[field.id] = value;
      }
    });

    // Debug: log the complete input data being sent
    
    // Validate required fields
    let missingFields = [];
    
    if (selectedOperation === 'arc_length') {
      // For arc length, only parametric and limits are required (parameter defaults to 't')
      missingFields = config.fields.filter(field => 
        !inputData[field.id] && field.id !== 'parameter'
      );
    } else {
      // For other operations, all fields are required
      missingFields = config.fields.filter(field => !inputData[field.id]);
    }
    if (missingFields.length > 0) {
      displayError(`Please fill in: ${missingFields.map(f => f.label).join(', ')}`);
      return;
    }

    result.textContent = "Calculating...";

    try {
      const response = await fetch("http://localhost:5000/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inputData),
      });

      const data = await response.json();

      if (response.ok) {
        // Check if the result is actually an error message
        if (typeof data.result === 'string' && data.result.toLowerCase().includes('error')) {
          displayError(data.result);
        } else {
          displayResult(data.result, selectedOperation);
        }
      } else {
        displayError(data.error || "An error occurred.");
      }
    } catch (err) {
      displayError("Failed to connect to backend, check the input and try again.");
      console.error(err);
    }
  }
});
