#!/usr/bin/env bash
# Single-command local start for Visit Taniti prototype
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
PORT="${PORT:-4789}"
LOG="$ROOT/logs/last-start-dev.log"
mkdir -p "$ROOT/logs"

{
  echo "=== Visit Taniti start $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
  echo "Serving $ROOT on http://127.0.0.1:$PORT"
} | tee "$LOG"

# Prefer python http.server (no install); fall back to npx serve
if command -v python3 >/dev/null 2>&1; then
  echo "Using python3 -m http.server $PORT" | tee -a "$LOG"
  echo "Open http://127.0.0.1:$PORT/"
  exec python3 -m http.server "$PORT" --bind 127.0.0.1
fi

if command -v npx >/dev/null 2>&1; then
  echo "Using npx serve" | tee -a "$LOG"
  exec npx --yes serve -l "$PORT" .
fi

echo "ERROR: Need python3 or npx to serve the prototype." | tee -a "$LOG"
exit 1
