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
- **Modern Interface** - Beautiful gradient backgrounds and smooth animations
- **Error Handling** - Graceful error messages and validation
- **Responsive Design** - Works on desktop and mobile devices
- **Browser Extension** - Quick access popup calculator

### 🔧 Technical Features
- **Single API Endpoint** - Unified `/calculate` endpoint handling all operations
- **Advanced Parsing** - Multi-tier parsing system (latex2sympy → SymPy → fallbacks)
- **Edge Case Handling** - Handles malformed LaTeX like `t^{}`
- **Comprehensive Functions** - All trigonometric, logarithmic, and exponential functions
- **Modern UI** - Gradient backgrounds, smooth animations, and glass-morphism effects
- **Cross-browser Support** - Chrome and Firefox extension compatibility

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
- Modern web browser (Chrome, Firefox, Edge)

### Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/omarramy22/AUC_calculator.git
   cd AUC_calculator
   ```

2. **Install Python dependencies**
   ```bash
   pip install flask flask-cors sympy latex2sympy2 antlr4-python3-runtime
   ```

3. **Start the server**
   - **Using the batch file (Windows):**
   ```bash
   start_flask.bat
   ```
   
   - **Or manually:**
   ```bash
   cd backend
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

### Browser Extension Installation
1. Open Chrome/Firefox and go to Extensions page
   - Chrome: `chrome://extensions/`
   - Firefox: `about:addons`
2. Enable "Developer mode" (Chrome) or "Debug add-ons" (Firefox)
3. Click "Load unpacked" and select the `calculator_extension` folder
4. The AUC Calculator icon should appear in your browser toolbar

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
POST /calculate
# Single endpoint that handles all operations based on "operation" parameter:
# - partial_derivative
# - double_integral  
# - double_integral_polar
# - arc_length
# - gradient
# - divergence
# - curl
# - line_integral
# - surface_integral
# - directional_derivative
# - greens_theorem
# - stokes_theorem
# - lagrange_multipliers
```

## 📁 Project Structure

```
AUC_calculator/
├── 🌐 Frontend
│   └── calculator_extension/     # Browser extension
│       ├── popup.html           # Main interface
│       ├── popup.js             # Frontend logic  
│       ├── styles.css           # Modern styling with gradients
│       ├── manifest.json        # Extension configuration
│       └── icons/               # Extension icons
│   
├── ⚙️ Backend
│   ├── app.py                   # Flask server & single API endpoint
│   ├── calc3.py                 # Mathematical computation functions
│   ├── parser.py                # LaTeX parsing engine
│   ├── static/                  # Static web files
│   │   └── index.html          # Web interface
│   └── __pycache__/            # Python cache files
│
└── 📋 Configuration
    ├── start_flask.bat          # Windows startup script
    └── README.md                # This documentation
```

## 📚 API Documentation

### Partial Derivatives
```javascript
POST /calculate
{
    "operation": "partial_derivative",
    "function": "\\sin\\left(x\\right) + x^2",
    "variables": "x",
    "order": "1"
}
```

### Double Integrals
```javascript
POST /calculate
{
    "operation": "double_integral",
    "function": "x*y",
    "variables": "x,y",
    "limits": "0,1,0,2"
}
```

### Vector Operations
```javascript
POST /calculate
{
    "operation": "divergence",
    "vector_field": "x^2,y^2,z^2",
    "variables": "x,y,z"
}
```

## 🛠️ Development

### Setting Up Development Environment
1. **Install dependencies**
   ```bash
   pip install flask flask-cors sympy latex2sympy2 antlr4-python3-runtime
   ```

2. **Start development server**
   ```bash
   # Using batch file
   start_flask.bat
   
   # Or manually
   cd backend
   python app.py
   ```

3. **Access the application**
   - Web interface: `http://localhost:5000`
   - Browser extension: Load `calculator_extension` folder

### Key Components
- **Parser System**: Multi-tier LaTeX parsing for robust expression handling
- **Mathematical Engine**: Built on SymPy for accurate symbolic computation
- **Web API**: RESTful Flask endpoints for all operations
- **Frontend**: Vanilla JavaScript with MathLive for LaTeX rendering

### Adding New Features
1. Add mathematical function to `calc3.py`
2. Update the operation handling in `app.py` 
3. Add frontend controls in `popup.html/popup.js`
4. Test functionality manually in both web and extension interfaces

## 🧪 Testing

### Manual Testing
1. **Start the server**: 
   ```bash
   start_flask.bat
   ```
   
2. **Open browser**: Navigate to `http://localhost:5000`

3. **Test mathematical operations**:
   - Try basic expressions: `2t`, `x^2`
   - Test trigonometric functions: `\sin\left(t\right)`, `\cos\left(x\right)`
   - Verify edge cases: `t^{}`, empty inputs
   - Test complex expressions: `\frac{x^2}{2} + \sqrt{y}`

### Browser Extension Testing
1. Load the extension in Chrome/Firefox
2. Click the calculator icon in the toolbar
3. Test all mathematical operations in the popup
4. Verify LaTeX rendering works correctly

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make changes and test**
   ```bash
   # Start server and test manually
   start_flask.bat
   # Then open http://localhost:5000
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
- Write clear, documented code
- Follow existing code style and patterns
- Update documentation when adding features
- Test LaTeX parsing thoroughly with edge cases
- Ensure both web interface and browser extension work correctly

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
