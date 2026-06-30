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
        if not output.get("ok"):
            raise HTTPException(status_code=400, detail=output.get("error", "Export failed"))
        return {"ok": True, "file": output.get("file"), "format": output.get("format")}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
