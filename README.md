# 🧮 AUC Calculator

A comprehensive mathematical calculator designed for AUC students, featuring advanced calculus operations, vector calculus, and LaTeX expression parsing.

## 📖 Table of Contents
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🔢 Core Mathematical Operations
- **Partial Derivatives** - Calculate partial derivatives of multivariable functions
- **Arc Length** - Compute arc length of parametric curves
- **Gradient** - Find gradient vectors of scalar fields
- **Multiple Integrals** - Evaluate double and triple integrals
- **Polar Integrals** - Integration in polar coordinate systems

### 🌊 Vector Calculus
- **Divergence** - Calculate divergence of vector fields
- **Curl** - Compute curl of 3D vector fields
- **Line Integrals** - Evaluate line integrals over curves
- **Surface Integrals** - Calculate surface integrals over parametric surfaces
- **Directional Derivatives** - Find derivatives in specified directions

### 📐 Advanced Topics
- **Green's Theorem** - 2D circulation and flux calculations
- **Stokes' Theorem** - Relating surface and line integrals
- **Lagrange Multipliers** - Constrained optimization problems

### 🎨 User Experience
- **LaTeX Input Support** - Parse complex mathematical expressions like `\sin\left(t\right)`
- **Real-time Calculation** - Instant results as you type
- **Parameter Persistence** - Browser remembers your settings
- **Error Handling** - Graceful error messages and validation
- **Responsive Design** - Works on desktop and mobile devices

### 🔧 Technical Features
- **Advanced Parsing** - Multi-tier parsing system (latex2sympy → SymPy → fallbacks)
- **Edge Case Handling** - Handles malformed LaTeX like `t^{}`
- **Comprehensive Functions** - All trigonometric, logarithmic, and exponential functions
- **Browser Extension Ready** - Can be packaged as Chrome/Firefox extension

## 🖼️ Screenshots

*Web Interface*
- Clean, intuitive calculator interface
- Real-time LaTeX rendering with MathLive
- Organized operation categories

*Browser Extension*
- Popup calculator for quick access
- Same functionality as web version
- Lightweight and fast

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Modern web browser

### Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/omarramy22/AUC_calculator.git
   cd AUC_calculator
   ```

2. **Install Python dependencies**
   ```bash
   pip install sympy flask latex2sympy2 antlr4-python3-runtime
   ```

3. **Start the server**
   ```bash
   python backend/test_server.py
   ```
   Or use the batch file:
   ```bash
   start_flask.bat
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

### Browser Extension Installation
1. Open Chrome/Firefox extension settings
2. Enable "Developer mode"
3. Click "Load unpacked" and select the `calculator_extension` folder

## 💻 Usage

### Web Interface
1. **Select Operation** - Choose from dropdown menus (Derivatives, Integrals, etc.)
2. **Enter Expression** - Type mathematical expressions using LaTeX syntax
3. **Set Parameters** - Define variables, limits, and bounds
4. **Calculate** - Click calculate to get instant results

### Supported LaTeX Syntax
```latex
2t                          # Simple expressions
\sin\left(t\right)         # Trigonometric functions
\frac{x^2}{2}              # Fractions
\sqrt{x + y}               # Square roots
\int_{0}^{1} x dx          # Integrals
```

### API Endpoints
```
POST /calculate/partial_derivative
POST /calculate/arc_length
POST /calculate/gradient
POST /calculate/multiple_integral
POST /calculate/polar_integral
POST /calculate/divergence
POST /calculate/curl
# ... and more
```

## 📁 Project Structure

```
AUC_calculator/
├── 🌐 Frontend
│   ├── calculator_extension/     # Browser extension
│   │   ├── popup.html           # Main interface
│   │   ├── popup.js             # Frontend logic
│   │   ├── styles.css           # Styling
│   │   └── manifest.json        # Extension config
│   
├── ⚙️ Backend
│   ├── app.py                   # Flask server & API
│   ├── calc3.py                 # Mathematical functions
│   ├── parser.py                # LaTeX parsing engine
│   └── README.md                # Backend documentation
│
├── 🧪 Testing
│   ├── comprehensive_test.py    # Complete validation
│   ├── frontend_test_guide.py   # Frontend test cases
│   └── test_server.py           # Development server
│
└── 📋 Configuration
    ├── start_flask.bat          # Windows startup script
    └── README.md                # This file
```

## 📚 API Documentation

### Partial Derivatives
```javascript
POST /calculate/partial_derivative
{
    "expression": "\\sin\\left(x\\right) + x^2",
    "variables": ["x"],
    "order": 1
}
```

### Arc Length
```javascript
POST /calculate/arc_length
{
    "expressions": ["2t", "\\sin\\left(t\\right)"],
    "parameter": "t",
    "bounds": ["0", "\\pi"]
}
```

### Vector Operations
```javascript
POST /calculate/divergence
{
    "vector_field": ["x^2", "y^2", "z^2"],
    "variables": ["x", "y", "z"]
}
```

## 🛠️ Development

### Setting Up Development Environment
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt  # If available
   # Or manually install: sympy flask latex2sympy2 antlr4-python3-runtime
   ```

2. **Run tests**
   ```bash
   cd backend
   python comprehensive_test.py
   ```

3. **Start development server**
   ```bash
   python backend/test_server.py
   ```

### Key Components
- **Parser System**: Multi-tier LaTeX parsing for robust expression handling
- **Mathematical Engine**: Built on SymPy for accurate symbolic computation
- **Web API**: RESTful Flask endpoints for all operations
- **Frontend**: Vanilla JavaScript with MathLive for LaTeX rendering

### Adding New Features
1. Add mathematical function to `calc3.py`
2. Create API endpoint in `app.py`
3. Add frontend controls in `popup.html/popup.js`
4. Write tests in `comprehensive_test.py`

## 🧪 Testing

### Backend Testing
```bash
# Complete functionality test
python backend/comprehensive_test.py

# Frontend test guide
python backend/frontend_test_guide.py
```

### Manual Testing
1. Start test server: `python backend/test_server.py`
2. Open: http://localhost:5000
3. Test various mathematical expressions
4. Verify LaTeX parsing works correctly

### Test Cases
- ✅ Basic expressions: `2t`, `x^2`
- ✅ Trigonometric: `\sin\left(t\right)`, `\cos\left(x\right)`
- ✅ Edge cases: `t^{}`, empty inputs
- ✅ Complex expressions: `\frac{x^2}{2} + \sqrt{y}`
- ✅ All mathematical operations

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make changes and test**
   ```bash
   python backend/comprehensive_test.py
   ```
4. **Commit changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open Pull Request**

### Development Guidelines
- Write tests for new features
- Follow existing code style
- Update documentation
- Test LaTeX parsing thoroughly

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Omar Ramy** - [@omarramy22](https://github.com/omarramy22)

## 🙏 Acknowledgments

- Built for AUC (American University in Cairo) students
- Powered by SymPy for mathematical computations
- Uses MathLive for LaTeX rendering
- LaTeX parsing via latex2sympy2

## 📞 Support

For questions, issues, or suggestions:
- 🐛 [Open an Issue](https://github.com/omarramy22/AUC_calculator/issues)
- 📧 Contact: [Your Email]
- 💬 Discussions: [GitHub Discussions]

---

**⭐ Star this repository if it helped you with your calculus homework!** 
