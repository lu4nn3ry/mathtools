from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import shutil
from pathlib import Path
from backend.models.database import get_db
from backend.routers import solve, explain, verify, export, templates

app = FastAPI(
    title="MathTools Offline API",
    version="0.1.0",
    docs_url="/api/docs",
)

# CORS — allow the frontend dev server and Tauri webview
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1420",      # Vite dev server
        "http://localhost:5173",      # Vite alternate port
        "tauri://localhost",           # Tauri production webview
        "https://tauri.localhost",     # Tauri production webview (alt)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(solve.router)
app.include_router(explain.router)
app.include_router(verify.router)
app.include_router(export.router)
app.include_router(templates.router)


@app.get("/api/v1/health")
async def health_check():
    # SymPy
    try:
        import sympy
        sympy_ver = sympy.__version__
        sympy_status = "ok"
    except Exception:
        sympy_ver = ""
        sympy_status = "error"

    # Lean / lake
    lake_path = shutil.which("lake")
    lean_path = shutil.which("lean")
    elan_bin = Path.home() / ".elan" / "bin"
    if not lake_path and elan_bin.exists():
        lake_path = str(elan_bin / "lake") if (elan_bin / "lake").exists() or (elan_bin / "lake.exe").exists() else None
    lean_status = "ok" if lake_path else "not found"
    if elan_bin.exists() and not lake_path:
        lean_status = "installing (toolchain download in progress)"

    # Typst
    typst_path = shutil.which("typst")
    if not typst_path:
        wget_typst = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages" / "Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe" / "typst-x86_64-pc-windows-msvc" / "typst.exe"
        if wget_typst.exists():
            typst_path = str(wget_typst)

    # LLM model
    model_path = Path(__file__).parent.parent / "models" / "qwen" / "qwen2.5-7b-instruct-q4_k_m.gguf"

    return {
        "status": "ok",
        "version": "0.1.0",
        "engines": {
            "sympy": {"status": sympy_status, "version": sympy_ver},
            "lean": {"status": lean_status, "lake": bool(lake_path), "lean": bool(lean_path)},
            "llm": {"status": "available" if model_path.exists() else "not installed",
                     "model": "Qwen 2.5 7B Q4_K_M" if model_path.exists() else None},
            "typst": {"status": "ok" if typst_path else "not found", "path": typst_path},
        },
        "database": "sqlite",
        "fpdf_fallback": True,
    }


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
        log_level="info",
    )
