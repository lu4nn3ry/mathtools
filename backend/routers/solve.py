from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.core.sympy_engine import SympyEngine

router = APIRouter(prefix="/api/v1", tags=["solve"])

engine = SympyEngine()

class SolveRequest(BaseModel):
    expression: str
    variable: str = "x"

@router.post("/solve")
async def solve_expression(req: SolveRequest):
    try:
        result = engine.solve(req.expression, req.variable)
        return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
