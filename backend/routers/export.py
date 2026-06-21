from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.core.typst_bridge import TypstBridge

router = APIRouter(prefix="/api/v1", tags=["export"])

bridge = TypstBridge()

class ExportRequest(BaseModel):
    content: str
    format: str = "pdf"

@router.post("/export")
async def export_document(req: ExportRequest):
    try:
        output = bridge.export(req.content, req.format)
        return {"ok": True, "file": output}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
