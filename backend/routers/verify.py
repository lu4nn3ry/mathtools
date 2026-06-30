from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.core.lean_bridge import LeanBridge

router = APIRouter(prefix="/api/v1", tags=["verify"])

bridge = LeanBridge()


class VerifyRequest(BaseModel):
    theorem: str
    proof: str = ""


class ToLeanRequest(BaseModel):
    expression: str
    theorem_name: str = "auto"


@router.post("/verify")
async def verify_proof(req: VerifyRequest):
    try:
        result = bridge.verify(req.theorem, req.proof)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/verify/templates")
async def list_templates():
    return {"ok": True, "templates": bridge.get_templates()}


@router.post("/verify/sympy-to-lean")
async def sympy_to_lean(req: ToLeanRequest):
    try:
        result = bridge.generate_proof(req.expression, req.theorem_name)
        return {"ok": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/verify/extract-goal")
async def extract_goal(req: VerifyRequest):
    try:
        goal = bridge.extract_goal(req.theorem)
        return {"ok": True, **goal}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
