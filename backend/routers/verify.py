from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.core.lean_bridge import LeanBridge

router = APIRouter(prefix="/api/v1", tags=["verify"])

bridge = LeanBridge()

class VerifyRequest(BaseModel):
    theorem: str
    proof: str = ""

@router.post("/verify")
async def verify_proof(req: VerifyRequest):
    try:
        result = bridge.verify(req.theorem, req.proof)
        return {"ok": True, "verified": result["verified"], "diagnostics": result["diagnostics"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
