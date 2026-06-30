"""Unit tests for TypstBridge — document export engine."""


class TestTypstBridge:
    """Feature: Exportação PDF"""

    def test_export_fpdf_fallback(self):
        """Sem typst, usa fallback fpdf2."""
        from backend.core.typst_bridge import TypstBridge
        bridge = TypstBridge()
        bridge.typst_path = None
        result = bridge.export("# Hello", "pdf")
        assert result["ok"] is True, f"fpdf2 fallback failed: {result.get('error')}"
        assert result["engine"] == "fpdf2"

    def test_export_invalid_format(self):
        """Formato inválido deve retornar erro."""
        from backend.core.typst_bridge import TypstBridge
        bridge = TypstBridge()
        bridge.typst_path = "/fake/path"
        result = bridge.export("# Hello", "docx")
        assert result["ok"] is False
        assert "unsupported" in result["error"].lower()
