import sympy as sp
import re
import io
from typing import Optional

from backend.core.safe_math import SafeMathEvaluator


class SympyEngine:
    def __init__(self):
        self.session = {}

    def _parse(self, expression: str):
        """Converte entrada do usuário em expressão SymPy sem eval/exec."""
        return SafeMathEvaluator(session=self.session).parse_expression(expression)

    def _symbol(self, name: str):
        """Cria um símbolo a partir de um nome de variável validado."""
        if not re.fullmatch(r"[A-Za-z_]\w*", name or ""):
            raise ValueError(f"Nome de variável inválido: {name!r}")
        return sp.Symbol(name)

    def evaluate(self, expression: str) -> dict:
        """Evaluate a math expression and return multiple formats."""
        result = self._parse(expression)
        if isinstance(result, sp.Basic):
            return {
                "input": expression,
                "result": str(result),
                "latex": sp.latex(result),
                "type": type(result).__name__,
            }
        return {
            "input": expression,
            "result": repr(result),
            "latex": None,
            "type": type(result).__name__,
        }

    def solve(self, expression: str, variable: str = "x") -> dict:
        expr = self._parse(expression)
        var = self._symbol(variable)
        solutions = sp.solve(expr, var)
        return {
            "expression": str(expr),
            "solutions": [str(s) for s in (solutions if isinstance(solutions, list) else [solutions])],
            "latex": sp.latex(solutions),
            "type": "solve",
        }

    def simplify(self, expression: str) -> dict:
        expr = self._parse(expression)
        simplified = sp.simplify(expr)
        return {
            "input": str(expr),
            "result": str(simplified),
            "latex": sp.latex(simplified),
            "type": "simplify",
        }

    def differentiate(self, expression: str, variable: str = "x",
                     order: int = 1) -> dict:
        expr = self._parse(expression)
        var = self._symbol(variable)
        derivative = sp.diff(expr, var, order)
        return {
            "input": str(expr),
            "result": str(derivative),
            "latex": sp.latex(derivative),
            "type": "derivative",
        }

    def integrate(self, expression: str, variable: str = "x",
                  definite: Optional[tuple] = None) -> dict:
        expr = self._parse(expression)
        var = self._symbol(variable)
        if definite:
            integral = sp.integrate(expr, (var, definite[0], definite[1]))
        else:
            integral = sp.integrate(expr, var)
        return {
            "input": str(expr),
            "result": str(integral),
            "latex": sp.latex(integral),
            "type": "integral",
        }

    def expand(self, expression: str) -> dict:
        expr = self._parse(expression)
        expanded = sp.expand(expr)
        return {
            "input": str(expr),
            "result": str(expanded),
            "latex": sp.latex(expanded),
            "type": "expand",
        }

    def factor(self, expression: str) -> dict:
        expr = self._parse(expression)
        factored = sp.factor(expr)
        return {
            "input": str(expr),
            "result": str(factored),
            "latex": sp.latex(factored),
            "type": "factor",
        }

    def series(self, expression: str, variable: str = "x",
               point: str = "0", order: int = 6) -> dict:
        expr = self._parse(expression)
        var = self._symbol(variable)
        pt = self._parse(point)
        result = sp.series(expr, var, pt, order)
        return {
            "input": f"series({expression}, {variable}, {point}, {order})",
            "result": str(result),
            "latex": sp.latex(result),
            "type": "series",
        }

    def solve_linear_system(self, equations: list, variables: list) -> dict:
        exprs = [self._parse(eq) for eq in equations]
        vars = [self._symbol(v) for v in variables]
        result = sp.linsolve(exprs, vars)
        solutions = []
        for sol in result.args if hasattr(result, 'args') else [result]:
            solutions.append({str(v): str(s) for v, s in zip(vars, sol)})
        return {
            "equations": equations,
            "variables": variables,
            "solutions": solutions,
            "latex": sp.latex(result),
            "type": "linear_system",
        }

    def limit(self, expression: str, variable: str = "x",
              point: str = "0", direction: str = "+-") -> dict:
        expr = self._parse(expression)
        var = self._symbol(variable)
        pt = self._parse(point)
        if direction == "+":
            result = sp.limit(expr, var, pt, dir="+")
        elif direction == "-":
            result = sp.limit(expr, var, pt, dir="-")
        else:
            result = sp.limit(expr, var, pt)
        return {
            "input": f"limit({expression}, {variable} -> {point})",
            "result": str(result),
            "latex": sp.latex(result),
            "type": "limit",
        }

    def to_lean(self, expression: str) -> str:
        """Convert a SymPy expression to a Lean theorem statement."""
        expr = self._parse(expression)
        lean_str = repr(expr)

        replacements = [
            ("**", " ^ "),
            ("*", " * "),
            ("/", " / "),
            ("+", " + "),
            ("-", " - "),
        ]
        for old, new in replacements:
            lean_str = lean_str.replace(old, new)

        # Map common functions
        lean_str = lean_str.replace("sin(", "Real.sin ")
        lean_str = lean_str.replace("cos(", "Real.cos ")
        lean_str = lean_str.replace("tan(", "Real.tan ")
        lean_str = lean_str.replace("exp(", "Real.exp ")
        lean_str = lean_str.replace("log(", "Real.log ")
        lean_str = lean_str.replace("sqrt(", "Real.sqrt ")
        lean_str = lean_str.replace("pi", "Real.pi")
        lean_str = lean_str.replace("E", "Real.exp 1")

        # Clean up spacing
        lean_str = re.sub(r'\s+', ' ', lean_str).strip()

        return lean_str

    def to_lean_theorem(self, expression: str, name: str = "computed") -> str:
        """Generate a complete Lean theorem from a SymPy expression."""
        lean_expr = self.to_lean(expression)
        return (
            f"theorem {name} : {lean_expr} := by\n"
            f"  native_decide\n"
        )

    def execute(self, code: str) -> dict:
        """Executa uma célula na DSL matemática restrita (sem eval/exec)."""
        output = io.StringIO()
        evaluator = SafeMathEvaluator(session=self.session, stdout=output)
        try:
            last_val = evaluator.execute_cell(code)
            stdout_output = output.getvalue().strip()
            result = {
                "input": code,
                "stdout": stdout_output,
                "type": "exec",
                "session_vars": {k: str(v) for k, v in self.session.items()},
            }
            if last_val is not None:
                try:
                    result["result"] = str(last_val)
                    ltx = sp.latex(last_val) if isinstance(last_val, (sp.Basic, list, tuple)) else None
                    if ltx:
                        result["latex"] = ltx
                except Exception:
                    result["result"] = repr(last_val)
            return result
        except Exception as e:
            return {"input": code, "error": str(e), "type": "error", "session_vars": {}}
        finally:
            output.close()

    def reset_session(self):
        self.session.clear()

    def get_symbols(self) -> list:
        """Return all symbols currently in the session for the inspector."""
        return [
            {
                "name": name,
                "type": "Symbol",
                "description": str(sym),
            }
            for name, sym in self.session.items()
        ]
