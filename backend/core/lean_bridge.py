import subprocess
import shutil
from pathlib import Path

class LeanBridge:
    def __init__(self):
        self.lake_path = shutil.which("lake")

    def verify(self, theorem: str, proof: str = "") -> dict:
        if not self.lake_path:
            return {
                "verified": False,
                "diagnostics": ["Lean 4 (lake) not found in PATH. Install elan: curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh"],
            }

        code = f"""
import Mathlib

{theorem}
"""
        if proof:
            code += f"\n{proof}"

        try:
            result = subprocess.run(
                [self.lake_path, "run"],
                input=code,
                text=True,
                capture_output=True,
                timeout=30,
                cwd=str(Path(__file__).parent.parent.parent / "lean"),
            )
            return {
                "verified": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "diagnostics": [],
            }
        except subprocess.TimeoutExpired:
            return {"verified": False, "diagnostics": ["Lean verification timed out"]}
        except Exception as e:
            return {"verified": False, "diagnostics": [str(e)]}

    def sympy_to_lean(self, expression: str) -> str:
        try:
            expr = sp.sympify(expression)
            lean_str = str(expr).replace("**", "^")
            return f"theorem generated : {lean_str} := by\n  sorry"
        except Exception:
            return "theorem error_in_conversion : sorry := by sorry"
