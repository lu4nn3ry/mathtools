from pydantic import BaseModel
from typing import Optional


class SolveRequest(BaseModel):
    expression: str
    variable: str = "x"
    operation: str = "solve"


class ExplainRequest(BaseModel):
    expression: str
    level: str = "graduacao"


class VerifyRequest(BaseModel):
    theorem: str
    proof: str = ""


class ExportRequest(BaseModel):
    content: str
    format: str = "pdf"
    title: Optional[str] = "document"
