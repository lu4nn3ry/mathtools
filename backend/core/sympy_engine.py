import sympy as sp
import re
import sys
import io
from typing import Optional


class SympyEngine:
    def __init__(self):
        self.session = {}

    def _ensure_symbols(self, expr_str: str):
        """Automatically discover and create symbols from an expression string."""
        # Find all valid Python/SymPy identifiers that aren't known functions
        known = {"sin", "cos", "tan", "cot", "sec", "csc",
                 "asin", "acos", "atan", "atan2", "acot", "asec", "acsc",
                 "sinh", "cosh", "tanh", "asinh", "acosh", "atanh",
                 "exp", "log", "sqrt", "Abs", "sign",
                 "pi", "E", "I", "oo", "Integer", "Rational", "Float",
                 "Symbol", "symbols", "Matrix", "eye", "zeros", "ones",
                 "diff", "integrate", "solve", "simplify", "expand",
                 "factor", "collect", "apart", "together", "cancel",
                 "limit", "series", "summation", "product",
                 "oo", "zoo", "nan"}
        identifiers = set(re.findall(r'\b[a-zA-Z_]\w*\b', expr_str))
        for name in identifiers:
            if name not in known and not name.startswith("_"):
                if name not in self.session:
                    self.session[name] = sp.Symbol(name)

    def evaluate(self, expression: str) -> dict:
        """Evaluate an arbitrary SymPy expression and return multiple formats."""
        self._ensure_symbols(expression)
        namespace = self.session.copy()
        namespace.update({
            "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
            "cot": sp.cot, "sec": sp.sec, "csc": sp.csc,
            "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
            "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
            "exp": sp.exp, "log": sp.log, "sqrt": sp.sqrt,
            "pi": sp.pi, "E": sp.E, "I": sp.I,
            "diff": sp.diff, "integrate": sp.integrate,
            "solve": sp.solve, "simplify": sp.simplify,
            "expand": sp.expand, "factor": sp.factor,
            "limit": sp.limit, "summation": sp.summation,
            "oo": sp.oo, "Matrix": sp.Matrix,
            "symbols": sp.symbols, "Symbol": sp.Symbol,
        })
        result = eval(expression, {"__builtins__": {}}, namespace)
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
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        solutions = sp.solve(expr, var)
        return {
            "expression": str(expr),
            "solutions": [str(s) for s in (solutions if isinstance(solutions, list) else [solutions])],
            "latex": sp.latex(solutions),
            "type": "solve",
        }

    def simplify(self, expression: str) -> dict:
        expr = sp.sympify(expression)
        simplified = sp.simplify(expr)
        return {
            "input": str(expr),
            "result": str(simplified),
            "latex": sp.latex(simplified),
            "type": "simplify",
        }

    def differentiate(self, expression: str, variable: str = "x",
                     order: int = 1) -> dict:
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        derivative = sp.diff(expr, var, order)
        return {
            "input": str(expr),
            "result": str(derivative),
            "latex": sp.latex(derivative),
            "type": "derivative",
        }

    def integrate(self, expression: str, variable: str = "x",
                  definite: Optional[tuple] = None) -> dict:
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
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
        expr = sp.sympify(expression)
        expanded = sp.expand(expr)
        return {
            "input": str(expr),
            "result": str(expanded),
            "latex": sp.latex(expanded),
            "type": "expand",
        }

    def factor(self, expression: str) -> dict:
        expr = sp.sympify(expression)
        factored = sp.factor(expr)
        return {
            "input": str(expr),
            "result": str(factored),
            "latex": sp.latex(factored),
            "type": "factor",
        }

    def series(self, expression: str, variable: str = "x",
               point: str = "0", order: int = 6) -> dict:
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        pt = sp.sympify(point)
        result = sp.series(expr, var, pt, order)
        return {
            "input": f"series({expression}, {variable}, {point}, {order})",
            "result": str(result),
            "latex": sp.latex(result),
            "type": "series",
        }

    def solve_linear_system(self, equations: list, variables: list) -> dict:
        exprs = [sp.sympify(eq) for eq in equations]
        vars = [sp.Symbol(v) for v in variables]
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
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        pt = sp.sympify(point)
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
        expr = sp.sympify(expression)
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
        """Execute Python code in the session, return stdout + last expression."""
        import builtins

        # Session namespace: only sp module + user variables (no sp.__dict__ flat)
        namespace = {"sp": sp, **self.session}

        # Snapshot variable names before execution
        before = set(namespace.keys())

        output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = output

        try:
            compiled = compile(code.strip(), "<input>", "exec")
            exec(compiled, {"__builtins__": builtins}, namespace)

            # Store only newly defined variables
            for k in namespace:
                if k not in before and not k.startswith("_"):
                    v = namespace[k]
                    if isinstance(v, (sp.Basic, list, tuple, set, dict)):
                        self.session[k] = v
                    elif hasattr(sp, "Matrix") and isinstance(v, sp.Matrix):
                        self.session[k] = v

            stdout_output = output.getvalue().strip()

            # Evaluate the last non-trivial line for its result
            last_val = None
            body = [ln.strip() for ln in code.strip().split("\n") if ln.strip()]
            for line in reversed(body):
                if line.startswith(("#", "import ", "from ", "return ")):
                    continue
                try:
                    last_val = eval(line, {"__builtins__": builtins}, namespace)
                    break
                except Exception:
                    continue

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
            sys.stdout = old_stdout

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
