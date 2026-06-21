import sympy as sp

class SympyEngine:
    def __init__(self):
        self.x, self.y, self.z = sp.symbols("x y z")

    def solve(self, expression: str, variable: str = "x") -> dict:
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        solutions = sp.solve(expr, var)
        return {
            "expression": str(expr),
            "solutions": [str(s) for s in solutions],
            "latex": sp.latex(solutions) if len(solutions) != 1 else sp.latex(solutions[0]),
        }

    def simplify(self, expression: str) -> dict:
        expr = sp.sympify(expression)
        simplified = sp.simplify(expr)
        return {
            "input": str(expr),
            "result": str(simplified),
            "latex": sp.latex(simplified),
        }

    def differentiate(self, expression: str, variable: str = "x") -> dict:
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        derivative = sp.diff(expr, var)
        return {
            "input": str(expr),
            "result": str(derivative),
            "latex": sp.latex(derivative),
        }

    def integrate(self, expression: str, variable: str = "x") -> dict:
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        integral = sp.integrate(expr, var)
        return {
            "input": str(expr),
            "result": str(integral),
            "latex": sp.latex(integral),
        }
