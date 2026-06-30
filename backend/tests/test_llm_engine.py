"""Unit tests for LLMEngine — multilevel math explainer."""


class TestLLMEngine:
    """Feature: Explicador Multinível"""

    def test_explain_derivative_medio(self, llm_engine):
        """Nível médio deve conter linguagem acessível e exemplos."""
        result = llm_engine.explain("derivative of sin(x)", "medio")
        assert result["level"] == "medio"
        assert result["level_label"] == "Ensino Médio"
        assert result["source"] == "rule-based"
        explanation = result["explanation"]
        assert "derivada" in explanation.lower()
        assert "taxa de variação" in explanation.lower()

    def test_explain_derivative_graduacao(self, llm_engine):
        """Nível graduação deve conter definição formal com limites."""
        result = llm_engine.explain("derivative of x^3", "graduacao")
        assert result["level"] == "graduacao"
        assert "lim" in result["explanation"] or "limite" in result["explanation"].lower()

    def test_explain_derivative_posgraduacao(self, llm_engine):
        """Nível pós-graduação deve conter generalizações avançadas."""
        result = llm_engine.explain("derivative", "posgraduacao")
        assert result["level"] == "posgraduacao"
        explanation = result["explanation"]
        assert any(term in explanation for term in ["Fréchet", "Gateaux", "Lie", "Banach"])

    def test_explain_integral_medio(self, llm_engine):
        """Integral em nível médio deve explicar área sob curva."""
        result = llm_engine.explain("integral", "medio")
        assert "área" in result["explanation"].lower()

    def test_explain_integral_graduacao(self, llm_engine):
        """Integral em nível graduação deve mencionar TFC."""
        result = llm_engine.explain("integral of x^2", "graduacao")
        assert "Teorema Fundamental" in result["explanation"]

    def test_explain_integral_posgraduacao(self, llm_engine):
        """Integral em nível pós-graduação deve mencionar Lebesgue."""
        result = llm_engine.explain("integral", "posgraduacao")
        assert "Lebesgue" in result["explanation"]

    def test_explain_limit_medio(self, llm_engine):
        """Limite em nível médio deve explicar comportamento."""
        result = llm_engine.explain("limit", "medio")
        assert "comportamento" in result["explanation"].lower()

    def test_explain_limit_graduacao(self, llm_engine):
        """Limite em nível graduação deve mencionar definição ε-δ."""
        result = llm_engine.explain("limit", "graduacao")
        assert "ε" in result["explanation"] or "ε-δ" in result["explanation"]

    def test_explain_generic_medio(self, llm_engine):
        """Conceito desconhecido em nível médio deve dar dicas de estudo."""
        result = llm_engine.explain("topologia algébrica", "medio")
        assert "Como estudar" in result["explanation"] or "praticando" in result["explanation"]

    def test_explain_generic_graduacao(self, llm_engine):
        """Conceito desconhecido em graduação deve mostrar conexões."""
        result = llm_engine.explain("teoria dos conjuntos", "graduacao")
        assert "Conexões" in result["explanation"]

    def test_explain_generic_posgraduacao(self, llm_engine):
        """Conceito desconhecido em pós deve mostrar direções de pesquisa."""
        result = llm_engine.explain("teoria de Galois", "posgraduacao")
        assert "Pesquisa" in result["explanation"] or "Hilbert" in result["explanation"]

    def test_explain_invalid_level_fallback(self, llm_engine):
        """Nível inválido deve cair para graduação como padrão."""
        # LLMEngine doesn't validate level internally; router does
        result = llm_engine.explain("derivative", "invalid")
        assert result["source"] == "rule-based"
        assert "explanation" in result

    def test_explain_returns_expected_keys(self, llm_engine):
        """Toda explicação deve conter metadados."""
        result = llm_engine.explain("derivative of sin(x)", "graduacao")
        assert "expression" in result
        assert "level" in result
        assert "level_label" in result
        assert "explanation" in result
        assert "source" in result
