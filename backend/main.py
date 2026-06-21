from fastapi import FastAPI, Depends
import uvicorn

from backend.models.database import get_db
from backend.routers import solve, explain, verify, export

app = FastAPI(title="MathTools Offline API", version="0.1.0")

app.include_router(solve.router)
app.include_router(explain.router)
app.include_router(verify.router)
app.include_router(export.router)


@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "ok",
        "engines": {"sympy": "ok", "lean": "stub", "llm": "stub"},
        "database": "sqlite",
    }


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8080, reload=True)
