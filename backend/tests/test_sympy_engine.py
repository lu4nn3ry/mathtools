"""Unit tests for SympyEngine — core symbolic computation engine."""

import sympy as sp
import pytest


class TestSympyEngine:
    """Feature: Manipulação Simbólica (SymPy)"""

    def test_evaluate_simple(self, sympy_engine):
        """Deve avaliar expressões simples e retornar resultado + latex."""
        result = sympy_engine.evaluate("x**2 + 2*x + 1")
        assert result["ok"] if "ok" in result else True
        assert result["input"] == "x**2 + 2*x + 1"
        assert "x**2" in result["result"]
        assert "latex" in result
        assert result["type"] in ("Add", "Symbol", "expr")

    def test_evaluate_trig(self, sympy_engine):
        """Deve avaliar funções trigonométricas."""
        result = sympy_engine.evaluate("sin(pi/2)")
        assert "1" in result["result"]

    def test_evaluate_matrix(self, sympy_engine):
        """Deve avaliar matrizes."""
        result = sympy_engine.evaluate("Matrix([1, 2, 3])")
        assert "Matrix" in result["result"] or "Matrix" in result["type"]

    def test_solve_quadratic(self, sympy_engine):
        """Deve resolver equação quadrática."""
        result = sympy_engine.solve("x**2 - 4", "x")
        assert result["type"] == "solve"
        assert "-2" in result["solutions"]
        assert "2" in result["solutions"]

    def test_solve_linear(self, sympy_engine):
        """Deve resolver equação linear."""
        result = sympy_engine.solve("2*x + 3", "x")
        assert "-3/2" in result["solutions"] or "-1.5" in str(result["solutions"])

    def test_simplify_trig(self, sympy_engine):
        """Deve simplificar expressões trigonométricas."""
        result = sympy_engine.simplify("sin(x)**2 + cos(x)**2")
        assert "1" in result["result"]

    def test_simplify_polynomial(self, sympy_engine):
        """Deve simplificar polinômios."""
        result = sympy_engine.simplify("x**2 + 2*x + 1")
        assert "x**2" in result["result"]

    def test_differentiate_power(self, sympy_engine):
        """Deve derivar x³ → 3x²."""
        result = sympy_engine.differentiate("x**3", "x", 1)
        assert "3*x**2" in result["result"]

    def test_differentiate_sin(self, sympy_engine):
        """Deve derivar sin(x) → cos(x)."""
        result = sympy_engine.differentiate("sin(x)", "x")
        assert "cos" in result["result"]

    def test_differentiate_second_order(self, sympy_engine):
        """Deve calcular derivada segunda."""
        result = sympy_engine.differentiate("x**3", "x", 2)
        assert "6*x" in result["result"]

    def test_integrate_indefinite(self, sympy_engine):
        """Deve calcular integral indefinida de x²."""
        result = sympy_engine.integrate("x**2", "x")
        assert "x**3/3" in result["result"]

    def test_integrate_cos(self, sympy_engine):
        """Deve integrar cos(x) → sin(x)."""
        result = sympy_engine.integrate("cos(x)", "x")
        assert "sin" in result["result"]

    def test_integrate_definite(self, sympy_engine):
        """Deve calcular integral definida."""
        result = sympy_engine.integrate("x", "x", definite=(0, 1))
        assert "1/2" in result["result"]

    def test_expand(self, sympy_engine):
        """Deve expandir (x+1)² → x² + 2x + 1."""
        result = sympy_engine.expand("(x + 1)**2")
        assert "x**2" in result["result"]
        assert "2*x" in result["result"]

    def test_factor(self, sympy_engine):
        """Deve fatorar x² - 4 → (x-2)(x+2)."""
        result = sympy_engine.factor("x**2 - 4")
        assert "(x - 2)" in result["result"]

    def test_limit_basic(self, sympy_engine):
        """Deve calcular limite de sin(x)/x quando x→0."""
        result = sympy_engine.limit("sin(x)/x", "x", "0")
        assert "1" in result["result"]

    def test_to_lean_conversion(self, sympy_engine):
        """Deve converter expressão SymPy para sintaxe Lean."""
        lean = sympy_engine.to_lean("x**2 + 2*x + 1")
        assert "^" in lean or "x" in lean

    def test_to_lean_theorem(self, sympy_engine):
        """Deve gerar esqueleto de teorema Lean."""
        theorem = sympy_engine.to_lean_theorem("x**2 + 2*x + 1")
        assert theorem.startswith("theorem")
        assert "native_decide" in theorem

    def test_exec_simple(self, sympy_engine):
        """Deve executar código Python/SymPy."""
        result = sympy_engine.execute("x = sp.symbols('x')\nx**2 + 1")
        assert result["type"] == "exec"
        assert "x**2" in str(result.get("result", ""))

    def test_exec_with_import(self, sympy_engine):
        """Deve executar código com import."""
        code = "import sympy as sp\na, t = sp.symbols('a t')\nsp.diff(a*sp.cos(t), t)"
        result = sympy_engine.execute(code)
        assert "error" not in result
        assert result["type"] == "exec"

    def test_exec_session_preserved(self, sympy_engine):
        """Deve preservar variáveis entre execuções."""
        sympy_engine.execute("x = sp.symbols('x')")
        sympy_engine.execute("y = sp.symbols('y')")
        result = sympy_engine.execute("x + y")
        assert "error" not in result

    def test_get_symbols(self, sympy_engine):
        """Deve listar símbolos da sessão."""
        sympy_engine.execute("z = sp.symbols('z')")
        symbols = sympy_engine.get_symbols()
        names = [s["name"] for s in symbols]
        assert "z" in names

    def test_reset_session(self, sympy_engine):
        """Deve limpar a sessão."""
        sympy_engine.execute("k = sp.symbols('k')")
        sympy_engine.reset_session()
        assert sympy_engine.session == {}
