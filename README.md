# 🧮 Calc3_assistant

A comprehensive mathematical calculator designed for college students, featuring advanced calculus operations, vector calculus, and LaTeX expression parsing with exact symbolic computation.

## 📖 Table of Contents
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🔢 Core Mathematical Operations
- **Partial Derivatives** - Calculate partial derivatives of multivariable functions
- **Arc Length** - Compute arc length of parametric curves  
- **Gradient** - Find gradient vectors of scalar fields
- **Multiple Integrals** - Evaluate double and triple integrals
- **Divergence** - Calculate divergence of vector fields
- **Curl** - Compute curl of 3D vector fields

### 🌊 Vector Calculus
- **Line Integrals** - Evaluate line integrals over curves
- **Surface Integrals** - Calculate surface integrals over parametric surfaces
- **Directional Derivatives** - Find derivatives in specified directions
- **Green's Theorem** - 2D circulation and flux calculations
- **Stokes' Theorem** - Relating surface and line integrals

### 📐 Advanced Topics
- **Lagrange Multipliers** - Constrained optimization problems with exact symbolic solutions

### 🎨 User Experience
- **LaTeX Input Support** - Parse complex mathematical expressions with robust preprocessing
- **Real-time Calculation** - Instant results with MathLive rendering
- **Exact Symbolic Results** - Preserves square roots, fractions, and exact forms
- **Expression Cleanup** - Automatically removes `log(e)` terms and simplifies expressions
- **Modern Interface** - Beautiful gradient backgrounds and smooth animations
- **Error Handling** - Graceful error messages and validation
- **Responsive Design** - Works on desktop and mobile devices
- **Browser Extension** - Quick access popup calculator

### 🔧 Technical Features
- **Single API Endpoint** - Unified `/calculate` endpoint handling all operations
- **Advanced LaTeX Parsing** - Handles malformed LaTeX like `\sqrt2` → `\sqrt{2}`
- **Symbolic Mathematics** - Built on SymPy with custom expression cleanup
- **Expression Preprocessing** - Fixes common LaTeX formatting issues automatically
- **Exact Computation** - Preserves exact forms without numeric approximation
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
- Python 3.8+ (tested with Python 3.13.3)
- Modern web browser (Chrome, Firefox, Edge)

### Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/omarramy22/Calc3_assistant.git
   cd Calc3_assistant
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   *Or manually install:*
   ```bash
   pip install flask flask-cors sympy gunicorn antlr4-python3-runtime
   ```

3. **Start the server**
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
# Basic expressions
2*t                         # Simple expressions
x^2 + y                     # Powers and variables

# Functions (auto-preprocessed)
\sqrt2 → \sqrt{2}          # Square roots
\sinx → \sin{x}            # Trigonometric functions  
\ln2 → \ln{2}              # Logarithms

# Complex expressions
\frac{x^2}{2}              # Fractions
\sqrt{x + y}               # Square roots with expressions
\int_{0}^{1} x dx          # Integrals
```


### API Endpoints
```
POST /calculate
# Single endpoint that handles all operations based on "operation" parameter:
# - partial_derivative      # ∂f/∂x calculations
# - multiple_integral       # Double/triple integrals
# - arc_length             # Parametric curve length
# - gradient               # ∇f calculations  
# - divergence             # ∇·F calculations
# - curl                   # ∇×F calculations
# - line_integral          # ∫F·dr along curves
# - surface_integral       # ∫∫F·dS over surfaces
# - directional_derivative # D_uF at points
# - greens_theorem         # 2D circulation/flux
# - stokes_theorem         # 3D circulation
# - lagrange_multipliers   # Constrained optimization
```

## 📁 Project Structure

```
AUC_calculator/
├── 🌐 Frontend
│   └── calculator_extension/     # Browser extension
│       ├── popup.html           # Main interface
│       ├── popup.js             # Frontend logic with MathLive
│       ├── styles.css           # Modern styling with gradients
│       ├── manifest.json        # Extension configuration
│       └── icons/               # Extension icons
│   
├── ⚙️ Backend  
│   ├── app.py                   # Flask server & unified API endpoint
│   ├── calc3.py                 # Mathematical computation with exact symbolic results
│   ├── parser.py                # LaTeX parsing with preprocessing
│   ├── requirements.txt         # Python dependencies
│   └── __pycache__/            # Python cache files
│
└── 📋 Documentation
    ├── firefox_package.zip      # Firefox extension package
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

### Multiple Integrals
```javascript
POST /calculate
{
    "operation": "multiple_integral",
    "function": "x*y", 
    "variables": "x,y",
    "limits": "0,1,0,2"  // x: 0→1, y: 0→2
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
   pip install -r requirements.txt
   ```

2. **Start development server**
   ```bash
   cd backend
   python app.py
   ```

3. **Access the application**
   - Web interface: `http://localhost:5000`
   - Browser extension: Load `calculator_extension` folder

### Key Components
- **LaTeX Preprocessing**: Automatic fixing of common LaTeX formatting issues
- **Symbolic Mathematics**: Built on SymPy with custom expression cleanup functions
- **Expression Cleanup**: Removes `log(e)` terms and preserves exact symbolic forms
- **Unified API**: Single `/calculate` endpoint handling all mathematical operations
- **Frontend**: Vanilla JavaScript with MathLive for LaTeX rendering

### Mathematical Engine Features
- **Exact Computation**: No forced numeric approximation
- **Automatic Simplification**: Cleans up trigonometric and logarithmic expressions
- **Robust Parsing**: Handles malformed LaTeX with preprocessing
- **Comprehensive Coverage**: All vector calculus and multivariable calculus operations

### Adding New Features
1. Add mathematical function to `calc3.py` with `clean_trig_result()` call
2. Update the operation handling in `app.py` 
3. Add frontend controls in `popup.html/popup.js`
4. Test functionality in both web and extension interfaces

##  Contributing

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make changes and test**
   ```bash
   cd backend
   python app.py
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
- Write clear, documented code following existing patterns
- use * when multiplying things like 2x, so it becomes 2*x
- Test LaTeX parsing with edge cases like `\sqrt2`, `\sinx`
- Ensure exact symbolic computation is preserved
- Update documentation when adding features
- Test both web interface and browser extension

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Omar Ramy** - [@omarramy22](https://github.com/omarramy22)

## 🙏 Acknowledgments

- Built for AUC (American University in Cairo) students
- Powered by SymPy for exact symbolic mathematical computations
- Uses MathLive for beautiful LaTeX rendering
- Custom LaTeX preprocessing for robust expression parsing

## 📞 Support

For questions, issues, or suggestions:
- 🐛 [Open an Issue](https://github.com/omarramy22/Calc3_assistant/issues)
- 📧 Contact: Omarramy@aucegypt.edu
- 💬 Discussions: [GitHub Discussions]

---

**⭐ Star this repository if it helped you with your calculus homework!**
