# Quantum Calculator — Development Roadmap

This document outlines the planned development phases for the Quantum
Calculator project.

---

## Phase 1 — Standard Phase ✅ (Current)

**Target audience:** Elementary to middle school

**Goal:** A robust, PEMDAS-correct calculator that can evaluate any
arithmetic expression and show the step-by-step solution.

### Features Implemented
- Full PEMDAS / order-of-operations evaluation
- Step-by-step solution output
- Basic arithmetic: `+`, `-`, `*`, `/`, `%`
- Exponents/powers: `^` (e.g., `2^8`)
- Square root: `sqrt(x)`
- Grouping: explicit `(…)` and implicit multiplication `2(3+1)`
- Advanced functions: `abs`, `floor`, `ceil`, `factorial`
- Logarithms: `ln`, `log10`, `log2`
- Trigonometry: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
- Built-in constants: `pi`, `e`
- Three usage modes: importable Python module, CLI REPL, piped/scripted

---

## Phase 2 — Geometry Phase 🔲 (Planned)

**Target audience:** Middle school geometry

**Goal:** Add shape-related calculations and basic graphing support.

### Planned Features
- **Shapes module** (`quantum_calculator/geometry.py`)
  - Area, perimeter, and volume for common shapes:
    - Circle, triangle, rectangle, square, trapezoid
    - Sphere, cube, cylinder, cone, pyramid
  - Named formula output alongside the numeric result
- **Coordinate geometry**
  - Distance between two points
  - Midpoint of a line segment
  - Slope and equation of a line (`y = mx + b`)
- **Angle conversions** — degrees ↔ radians
- **Graphing** (`quantum_calculator/grapher.py`)
  - Plot expressions on a 2-D grid (using `matplotlib` or ASCII art fallback)
  - Plot geometric shapes

---

## Phase 3 — Complex Number Phase 🔲 (Planned)

**Target audience:** Pre-calculus / early college

**Goal:** Extend the parser and evaluator to handle imaginary and
complex numbers.

### Planned Features
- **Complex number literals** — parse `2+3i` or `2+3j` syntax
- **Complex arithmetic** — `+`, `-`, `*`, `/`, `^` for complex numbers
- **Complex functions**
  - `sqrt(-1)` → `i` (currently raises an error)
  - `abs(z)` → modulus; `arg(z)` → argument/phase angle
  - `conj(z)` → complex conjugate
  - `Re(z)`, `Im(z)` — real and imaginary parts
- **Polar form** — display results in `r·e^(iθ)` or `r∠θ` notation
- **Step display** updated to show real and imaginary parts separately

---

## Phase 4 — Algebra Phase 🔲 (Planned)

**Target audience:** Middle school through high school algebra

**Goal:** Introduce symbolic variables and algebraic equation solving.

### Planned Features
- **Variable support** — expressions like `2x + 3` or `a^2 + b^2`
- **Expression simplification** — collect like terms, expand products
- **Equation solver** — solve `f(x) = 0` style equations:
  - Linear: `2x + 3 = 7`
  - Quadratic: `x^2 - 5x + 6 = 0` (via quadratic formula and factoring)
  - Higher degree: numeric root finding (Newton's method / bisection)
- **Systems of equations** — solve two or more simultaneous linear
  equations
- **Inequalities** — solve and display solution sets on a number line
- **Symbolic differentiation** (stretch goal) — find `f'(x)` for
  polynomial expressions

---

## Long-term Vision

| Phase       | Status  | Key Addition                         |
|-------------|---------|--------------------------------------|
| Standard    | ✅ Done | Arithmetic, PEMDAS, step-by-step     |
| Geometry    | 🔲 Next | Shapes, coordinates, graphing        |
| Complex     | 🔲      | Imaginary numbers, polar form        |
| Algebra     | 🔲      | Variables, quadratics, systems       |
| Calculus    | 🔲      | Limits, derivatives, integrals       |
| Statistics  | 🔲      | Mean, median, standard deviation     |
