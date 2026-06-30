#!/usr/bin/env bash
# Start the FastAPI backend in development mode for Tauri sidecar.
#
# Usage:
#   ./scripts/dev-sidecar.sh
#
# This script is used by Tauri in dev mode (--dev-sidecar flag).
# It launches uvicorn directly from the Python source so you get
# hot-reload during development.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "[sidecar-dev] Starting FastAPI backend on http://localhost:8080"

# Ensure dependencies are installed
pip install -q -r "$ROOT/backend/requirements.txt"

# Add Lean/elan to PATH if available
ELAN_BIN="$HOME/.elan/bin"
if [ -d "$ELAN_BIN" ]; then
    export PATH="$ELAN_BIN:$PATH"
fi

# Launch uvicorn with reload enabled
exec python -m uvicorn backend.main:app \
    --host 127.0.0.1 \
    --port 8080 \
    --reload \
    --log-level info
