# MathTools Offline — Implementation Checklist

## Frontend (React + Vite)

### Editor
- [ ] **Editor.jsx**: Real Monaco editor (not static `pre`) wired to a live LaTeX state
- [ ] **Compile button**: POST to `/api/v1/export` → updates preview pane
- [ ] **Save/Undo/Redo**: File system access via Tauri IPC (`@tauri-apps/plugin-fs`)
- [ ] **Templates**: Dropdown loading `.tex` templates from `assets/templates/`
- [ ] **Symbols**: Insert math symbols at cursor position
- [ ] **Export PDF**: POST to `/api/v1/export?format=pdf` → trigger download
- [ ] **Status bar**: Real memory usage (via Tauri `os` plugin), real cursor position
- [ ] **Line numbers**: Sync with editor content length

### SymPy Console
- [ ] **Execute cell**: POST to `/api/v1/solve` → render result in output cell
- [ ] **Cell state**: Manage notebook cells (add, delete, reorder, edit)
- [ ] **Live Scope**: Real variable inspector fetched from session state
- [ ] **Kernel status**: Poll `/api/v1/health` or WebSocket for real CPU/mem
- [ ] **Common Operations**: Click a button (∫, d/dx, ∑) to insert template into current cell
- [ ] **History**: Persist session to SQLite via Tauri IPC

### Lean 4 Prover
- [ ] **Execute proof**: POST to `/api/v1/verify` → real Lean server response
- [ ] **Goal View**: Display real context + target goal from Lean
- [ ] **Messages**: Show real Lean diagnostics (errors, warnings, info)
- [ ] **File tree**: List `.lean` files from project directory
- [ ] **Tactic chips**: Click to insert tactic at cursor
- [ ] **Command palette**: Ctrl+P search theorems/tactics (query Lean mathlib)
- [ ] **Worker status**: Real process state (idle/busy/mem)

### Math Explainer
- [ ] **Explain endpoint**: POST `/api/v1/explain` with expression → get step-by-step
- [ ] **Toggle details**: Expand/collapse per-step detail panels
- [ ] **Quiz**: Validate answer, show correct/incorrect feedback
- [ ] **Related concepts**: Fetch from knowledge graph (SQLite)
- [ ] **Search**: `/api/v1/explain/search?q=` → autocomplete concepts
- [ ] **3D Visualization**: Embed three.js or mathjax for interactive plots

### Shared
- [ ] **Theme toggle**: Dark/light mode switch persisted to localStorage
- [ ] **Responsive layout**: Collapse sidebar, adapt to window resize
- [ ] **Offline indicator**: Real network status (navigator.onLine + backend ping)
- [ ] **Keyboard shortcuts**: Ctrl+S save, Ctrl+P palette, etc.
- [ ] **i18n**: Extract strings for pt-BR / en-US

## Backend (Python FastAPI)

### Solve Router (`/api/v1/solve`)
- [ ] **SymPy eval**: Execute arbitrary SymPy expressions securely
- [ ] **Session state**: Per-session symbol cache (in-memory dict keyed by session_id)
- [ ] **Serialization**: Return results as LaTeX + plain text + MathJSON

### Explain Router (`/api/v1/explain`)
- [ ] **LLM integration**: Connect to local model (llama.cpp / Ollama) for step-by-step
- [ ] **Fallback**: Rule-based explanation when LLM unavailable
- [ ] **Search**: Full-text search over local explanation database (SQLite FTS5)

### Verify Router (`/api/v1/verify`)
- [ ] **Lean runner**: Spawn `lean` process, capture stdout/stderr
- [ ] **Goal parsing**: Extract context, target goal, and messages from Lean output
- [ ] **Timeout**: Kill lean process after N seconds, return partial results

### Export Router (`/api/v1/export`)
- [ ] **Typst compilation**: Call `typst` binary to render `.typ` → PDF/SVG/PNG
- [ ] **LaTeX fallback**: Use `pdflatex` if available

### Core
- [ ] **Health endpoint**: Real engine status checks
- [ ] **Error handling**: Structured error responses (RFC 9457)
- [ ] **Rate limiting**: Prevent abuse of Lean/SymPy subprocesses
- [ ] **Database migrations**: Alembic for SQLite schema changes

## Desktop Integration (Tauri + Rust)

### Sidecar
- [ ] **PyInstaller spec**: `backend/pyinstaller.spec` — bundle FastAPI + dependencies
- [ ] **Build script**: `scripts/build-sidecar.sh` — compile Python, copy to `binaries/`
- [ ] **tauri.conf.json**: `externalBin` pointing to sidecar binary
- [ ] **lib.rs**: Spawn sidecar on app startup, kill on shutdown
- [ ] **Capabilities**: `shell:allow-execute` permission for sidecar

### Tauri Plugins
- [ ] **shell**: Sidecar management
- [ ] **fs**: Read/write user files (save `.tex`, `.lean`)
- [ ] **dialog**: Open/save file dialogs
- [ ] **os**: Memory/CPU stats for status bar
- [ ] **clipboard-manager**: Copy/paste math expressions
- [ ] **process**: Graceful sidecar shutdown

### Build & Distribute
- [ ] **Windows**: NSIS or MSI installer
- [ ] **macOS**: DMG (codesigned)
- [ ] **Linux**: AppImage / deb
- [ ] **Auto-update**: Tauri updater with GitHub Releases

## Testing

- [ ] **Frontend**: Vitest + React Testing Library for components
- [ ] **Backend**: pytest for API endpoints
- [ ] **E2E**: Tauri's WebDriver testing (tauri-driver)
- [ ] **Lean**: Test proofs compile with actual `lean4` binary

## Documentation

- [ ] **README.md**: Project overview + setup instructions (✓ done partially)
- [ ] **TODO.md**: This file
- [ ] **ARCHITECTURE.md**: How frontend, backend, Tauri, and sidecar connect
- [ ] **CONTRIBUTING.md**: How to set up dev environment
