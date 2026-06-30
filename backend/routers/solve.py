from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from backend.core.sympy_engine import SympyEngine

router = APIRouter(prefix="/api/v1", tags=["solve"])

engine = SympyEngine()


class SolveRequest(BaseModel):
    expression: str
    variable: str = "x"


class EvalRequest(BaseModel):
    expression: str


class DiffRequest(BaseModel):
    expression: str
    variable: str = "x"
    order: int = 1


class SeriesRequest(BaseModel):
    expression: str
    variable: str = "x"
    point: str = "0"
    order: int = 6


class LinearSystemRequest(BaseModel):
    equations: list[str]
    variables: list[str]


class IntegrateRequest(BaseModel):
    expression: str
    variable: str = "x"
    lower: Optional[int] = None
    upper: Optional[int] = None


@router.post("/solve/series")
async def series_expression(req: SeriesRequest):
    try:
        result = engine.series(req.expression, req.variable, req.point, req.order)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solve/linsolve")
async def linear_system(req: LinearSystemRequest):
    try:
        result = engine.solve_linear_system(req.equations, req.variables)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class ToLeanRequest(BaseModel):
    expression: str
    theorem_name: str = "computed"


@router.post("/solve")
async def solve_expression(req: SolveRequest):
    try:
        result = engine.solve(req.expression, req.variable)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solve/evaluate")
async def evaluate_expression(req: EvalRequest):
    try:
        result = engine.evaluate(req.expression)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solve/simplify")
async def simplify_expression(req: EvalRequest):
    try:
        result = engine.simplify(req.expression)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solve/differentiate")
async def differentiate_expression(req: DiffRequest):
    try:
        result = engine.differentiate(req.expression, req.variable, req.order)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solve/integrate")
async def integrate_expression(req: IntegrateRequest):
    try:
        definite = (req.lower, req.upper) if req.lower is not None and req.upper is not None else None
        result = engine.integrate(req.expression, req.variable, definite)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solve/expand")
async def expand_expression(req: EvalRequest):
    try:
        result = engine.expand(req.expression)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solve/factor")
async def factor_expression(req: EvalRequest):
    try:
        result = engine.factor(req.expression)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solve/limit")
async def limit_expression(
    req: EvalRequest,
    variable: str = Query("x"),
    point: str = Query("0"),
    direction: str = Query("+-"),
):
    try:
        result = engine.limit(req.expression, variable, point, direction)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solve/sympy-to-lean")
async def sympy_to_lean(req: ToLeanRequest):
    try:
        theorem = engine.to_lean_theorem(req.expression, req.theorem_name)
        return {"ok": True, "theorem": theorem}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class ExecRequest(BaseModel):
    code: str


@router.post("/solve/exec")
async def execute_code(req: ExecRequest):
    try:
        result = engine.execute(req.code)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solve/reset")
async def reset_session():
    engine.reset_session()
    return {"ok": True, "message": "Session reset"}


@router.get("/solve/symbols")
async def list_symbols():
    return {"ok": True, "symbols": engine.get_symbols()}
