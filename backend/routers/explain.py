from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from backend.core.llm_engine import LLMEngine

router = APIRouter(prefix="/api/v1", tags=["explain"])

engine = LLMEngine()


class ExplainRequest(BaseModel):
    expression: str
    level: str = "graduacao"
    style: str = "didatico"


@router.post("/explain")
async def explain_expression(req: ExplainRequest):
    valid_levels = {"medio", "graduacao", "posgraduacao"}
    valid_styles = {"didatico", "conciso", "formal"}
    if req.level not in valid_levels:
        raise HTTPException(
            status_code=400,
            detail=f"Nível inválido: '{req.level}'. Opções: {', '.join(sorted(valid_levels))}",
        )
    if req.style not in valid_styles:
        raise HTTPException(
            status_code=400,
            detail=f"Estilo inválido: '{req.style}'. Opções: {', '.join(sorted(valid_styles))}",
        )
    try:
        result = engine.explain(req.expression, req.level, req.style)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
