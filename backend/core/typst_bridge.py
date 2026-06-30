import subprocess
import shutil
import tempfile
import re
from pathlib import Path

class TypstBridge:
    def __init__(self):
        self.typst_path = self._find_typst()

    def _find_typst(self) -> str | None:
        """Search for typst in PATH and common install locations."""
        path = shutil.which("typst")
        if path:
            return path
        home = Path.home()
        candidates = [
            home / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages"
            / "Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe"
            / "typst-x86_64-pc-windows-msvc" / "typst.exe",
            Path("C:/Program Files/Typst/typst.exe"),
            Path("C:/Program Files (x86)/Typst/typst.exe"),
        ]
        for c in candidates:
            if c.exists():
                return str(c)
        return None

    def export(self, content: str, fmt: str = "pdf") -> dict:
        fmt = fmt.lower()
        if fmt == "pdf":
            return self._export_pdf(content)
        elif fmt in ("png", "svg"):
            return self._export_typst(content, fmt)
        return {"ok": False, "error": f"Unsupported format: {fmt}"}

    def _export_typst(self, content: str, fmt: str) -> dict:
        """Export using Typst CLI (for PNG/SVG)."""
        if not self.typst_path:
            return {"ok": False, "error": f"Typst CLI not found for {fmt} export."}
        with tempfile.NamedTemporaryFile(suffix=".typ", delete=False, mode="w") as f:
            f.write(content)
            input_path = f.name
        output_path = input_path.replace(".typ", f".{fmt}")
        try:
            subprocess.run(
                [self.typst_path, "compile", input_path, output_path, "--format", fmt],
                capture_output=True, text=True, check=True, timeout=30,
            )
            return {"ok": True, "file": output_path, "format": fmt}
        except subprocess.CalledProcessError as e:
            return {"ok": False, "error": e.stderr}
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "Typst compilation timed out"}
        finally:
            Path(input_path).unlink(missing_ok=True)

    def _export_pdf(self, content: str) -> dict:
        """Export PDF using Typst CLI or Python fallback (fpdf2)."""
        if self.typst_path:
            result = self._export_typst(content, "pdf")
            if result["ok"]:
                return result

        try:
            return self._export_fpdf(content)
        except ImportError:
            if self.typst_path:
                return result
            return {"ok": False, "error": "PDF export requires Typst CLI (winget install Typst.Typst) or fpdf2 (pip install fpdf2)"}

    def _export_fpdf(self, content: str) -> dict:
        """Generate a PDF using Python fpdf2 with basic LaTeX-like rendering."""
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Courier", "", 10)

        for line in content.split("\n"):
            clean = re.sub(r'\$\$(.+?)\$\$', r'\1', line)
            clean = re.sub(r'\$(.+?)\$', r'\1', clean)
            pdf.cell(0, 6, clean, new_x="LMARGIN", new_y="NEXT")

        output = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        pdf.output(output.name)
        return {"ok": True, "file": output.name, "format": "pdf", "engine": "fpdf2"}
