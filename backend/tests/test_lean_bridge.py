"""Unit tests for LeanBridge — formal verification bridge."""


class TestLeanBridge:
    """Feature: Verificação Formal (Lean 4)"""

    def test_verify_without_lake(self, lean_bridge):
        """Sem lake no PATH, deve retornar verified=False com diagnóstico."""
        # Force lake_path to None
        lean_bridge.lake_path = None
        result = lean_bridge.verify("theorem t : 1 = 1 :=")
        assert result["verified"] is False
        assert any("lake" in d.lower() for d in result["diagnostics"])

    def test_get_templates(self, lean_bridge):
        """Deve retornar lista de templates de teoremas."""
        templates = lean_bridge.get_templates()
        assert len(templates) >= 4
        names = [t["name"] for t in templates]
        assert "quadratic_formula" in names
        assert "pythagorean_theorem" in names
        assert "sin_squared_add_cos_squared" in names
        assert "derivative_power_rule" in names

    def test_sympy_to_lean_simple(self, lean_bridge):
        """Deve converter expressão simples para Lean."""
        lean = lean_bridge.sympy_to_lean("x**2 + 1")
        assert "^" in lean
        assert "x" in lean

    def test_sympy_to_lean_trig(self, lean_bridge):
        """Deve converter sin/cos para Real.sin/Real.cos."""
        lean = lean_bridge.sympy_to_lean("sin(x)**2 + cos(x)**2")
        assert "Real.sin" in lean
        assert "Real.cos" in lean

    def test_sympy_to_lean_invalid(self, lean_bridge):
        """Expressão inválida deve retornar fallback."""
        lean = lean_bridge.sympy_to_lean("@@@ invalid @@@")
        assert "sorry" in lean

    def test_generate_proof_equality(self, lean_bridge):
        """Geração de prova para igualdade deve usar native_decide."""
        result = lean_bridge.generate_proof("(x+1)**2 = x**2 + 2*x + 1", "test_eq")
        assert "native_decide" in result["proof_tactic"]

    def test_generate_proof_trig(self, lean_bridge):
        """Geração de prova para trig deve usar simp."""
        result = lean_bridge.generate_proof("sin(x)**2 + cos(x)**2 = 1", "test_trig")
        assert "simp" in result["proof_tactic"]

    def test_generate_proof_unknown(self, lean_bridge):
        """Geração de prova sem correspondência deve usar sorry."""
        result = lean_bridge.generate_proof("f(x) = g(x)", "test_unknown")
        assert "sorry" in result["proof_tactic"]

    def test_extract_goal_simple(self, lean_bridge):
        """Deve extrair contexto e alvo de um teorema."""
        code = "theorem my_thm (a b : ℝ) (h : a = b) : a + 1 = b + 1 :="
        result = lean_bridge.extract_goal(code)
        assert len(result["context"]) >= 2
        assert "a + 1 = b + 1" in result["target"]
        names = [c["name"] for c in result["context"]]
        assert "a" in names
        assert "b" in names

    def test_extract_goal_without_theorem(self, lean_bridge):
        """Sem 'theorem', deve retornar contexto vazio."""
        result = lean_bridge.extract_goal("def x := 1")
        assert result["context"] == []
        assert result["target"] == ""

    def test_parse_diagnostics(self, lean_bridge):
        """Deve classificar diagnósticos por severidade."""
        output = "error: syntax error\nwarning: unused variable\ninfo: loaded"
        msgs = lean_bridge._parse_diagnostics(output)
        assert len(msgs) == 3
        assert msgs[0]["level"] == "error"
        assert msgs[1]["level"] == "warning"
        assert msgs[2]["level"] == "info"
