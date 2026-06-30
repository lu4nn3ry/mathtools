# Relatório de Exploração — MathTools Offline

## 1. Estrutura do Projeto

```
mathtools/
├── backend/                    # API Python (FastAPI)
│   ├── core/                   # Motores de computação
│   │   ├── sympy_engine.py     # SymPy (álgebra, derivadas, integrais, etc.)
│   │   ├── lean_bridge.py      # Lean 4 (verificação formal)
│   │   ├── llm_engine.py       # Explicador multinível (regras + LLM local)
│   │   └── typst_bridge.py     # Exportação PDF via Typst
│   ├── models/
│   │   └── database.py         # SQLite + SQLAlchemy
│   ├── routers/                # Endpoints REST
│   │   ├── solve.py            # POST /solve, /evaluate, /simplify, /differentiate, /integrate, /exec, etc.
│   │   ├── explain.py          # POST /explain
│   │   ├── verify.py           # POST /verify, /sympy-to-lean, /extract-goal
│   │   ├── export.py           # POST /export (PDF/PNG/SVG)
│   │   └── templates.py        # GET /templates/editor, /sympy/session, /lean/theorem, /explainer/content
│   ├── main.py                 # App FastAPI + CORS
│   ├── requirements.txt
│   └── build_sidecar.py        # Script de build PyInstaller
├── frontend/                   # Interface React + Tauri
│   ├── src/
│   │   ├── components/
│   │   │   ├── Editor.jsx      # Editor LaTeX com preview
│   │   │   ├── SympyConsole.jsx # Console SymPy interativo
│   │   │   ├── LeanProver.jsx   # Prover Lean 4
│   │   │   ├── Explainer.jsx    # Explicador multinível
│   │   │   ├── Sidebar.jsx      # Sidebar de navegação
│   │   │   ├── Toolbar.jsx
│   │   │   └── Preview.jsx
│   │   ├── styles/
│   │   │   └── globals.css      # Design tokens + todos os estilos
│   │   ├── lib/
│   │   │   └── api.js           # Cliente HTTP para o backend
│   │   ├── hooks/
│   │   │   └── useApi.js        # Hook React (alternativa)
│   │   ├── App.jsx              # Roteamento dos 4 painéis
│   │   └── main.jsx
│   ├── src-tauri/               # Configuração Tauri v2
│   │   ├── src/lib.rs           # Sidecar spawn
│   │   ├── tauri.conf.json      # externalBin + bundle
│   │   └── capabilities/default.json
│   └── package.json
├── scripts/
│   ├── dev-sidecar.ps1
│   └── dev-sidecar.sh
└── TODO.md
```

## 2. Arquivos de Teste Existentes

**Nenhum.** O projeto não possui:
- Testes unitários (pytest, vitest, jest)
- Testes de integração
- Testes de componente
- Configuração de CI (GitHub Actions, GitLab CI, etc.)
- Docker/container

## 3. Dependências Atuais

### Backend (requirements.txt)
```
fastapi, uvicorn, sympy, sqlalchemy, pydantic, python-multipart
```
Sem dependências de teste.

### Frontend (package.json devDependencies)
```
@vitejs/plugin-react, vite
```
Sem framework de teste.

## 4. Motores Core (4)

| Motor       | Classe          | Métodos Principais |
|-------------|-----------------|-------------------|
| SymPy       | SympyEngine     | evaluate, solve, simplify, differentiate, integrate, expand, factor, limit, to_lean, to_lean_theorem, execute, reset_session, get_symbols |
| Lean 4      | LeanBridge      | verify, get_templates, sympy_to_lean, generate_proof, extract_goal |
| LLM         | LLMEngine       | explain (3 níveis: medio, graduacao, posgraduacao), fallback rule-based |
| Typst       | TypstBridge     | export (pdf, png, svg) |

## 5. Endpoints REST (5 routers, ~20 endpoints)

| Router      | Prefixo          | Endpoints |
|-------------|------------------|-----------|
| solve       | /api/v1          | 12 POST + 1 GET |
| explain     | /api/v1          | 1 POST |
| verify      | /api/v1          | 2 POST + 1 GET |
| export      | /api/v1          | 1 POST |
| templates   | /api/v1/templates | 5 GET + 1 POST |

## 6. Frontend (4 componentes principais)

| Componente   | API Calls                           | Estado       |
|-------------|--------------------------------------|-------------|
| Editor.jsx  | fetchEditorTemplate, exportDocument | useState/useEffect |
| SympyConsole.jsx | fetchSympySession, execSympyCode, fetchSympySymbols | useState/useEffect |
| LeanProver.jsx  | fetchLeanTheorem, verifyTheorem, extractGoal | useState/useEffect |
| Explainer.jsx   | fetchExplainerContent, checkQuizAnswer | useState/useEffect |

## 7. Status das Features do TCC

| Feature | Status |
|---------|--------|
| Editor LaTeX com renderização | ✅ Implementado (template do backend, preview estático) |
| Resolução simbólica SymPy | ✅ Implementado (5 células de curvatura de hélice) |
| Conversão para Lean 4 | ✅ Implementado (teorema helix_curvature) |
| Verificação formal básica | ✅ Implementado (endpoint /verify) |
| Explicações multinível | ✅ Implementado (3 níveis: médio, graduação, pós) |
| Exportação PDF | ⚠️ Parcial (TypstBridge, requer typst CLI) |
| Interface desktop | ✅ Tauri v2 configurado com sidecar |
| Funcionamento offline | ✅ Processamento local, sem dependência de rede |
| Testes automatizados | ❌ Nenhum |
