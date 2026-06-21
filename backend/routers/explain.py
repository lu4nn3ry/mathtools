from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.core.llm_engine import LLMEngine

router = APIRouter(prefix="/api/v1", tags=["explain"])

engine = LLMEngine()

class ExplainRequest(BaseModel):
    expression: str
    level: str = "graduacao"

@router.post("/explain")
async def explain_expression(req: ExplainRequest):
    try:
        explanation = engine.explain(req.expression, req.level)
        return {"ok": True, "explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
