import subprocess
import shutil
import tempfile
from pathlib import Path

class TypstBridge:
    def __init__(self):
        self.typst_path = shutil.which("typst")

    def export(self, content: str, fmt: str = "pdf") -> dict:
        if not self.typst_path:
            return {
                "ok": False,
                "error": "Typst CLI not found. Install: winget install Typst.Typst",
            }

        fmt = fmt.lower()
        if fmt not in ("pdf", "png", "svg"):
            return {"ok": False, "error": f"Unsupported format: {fmt}"}

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
