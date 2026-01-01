#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python interpreter not found. Set PYTHON to your Python 3 executable." >&2
  exit 1
fi

if [ ! -d ".venv" ]; then
  "$PYTHON_BIN" -m venv .venv
fi

if [ -d ".venv/Scripts" ]; then
  # Windows
  # shellcheck disable=SC1091
  source .venv/Scripts/activate
  ENV_PYTHON=".venv/Scripts/python.exe"
  ACTIVATE_HINT="source .venv/Scripts/activate"
  WINDOWS_ALTERNATES="cmd: .venv\\Scripts\\activate | PowerShell: .venv\\Scripts\\Activate.ps1"
else
  # shellcheck disable=SC1091
  source .venv/bin/activate
  ENV_PYTHON=".venv/bin/python"
  ACTIVATE_HINT="source .venv/bin/activate"
  WINDOWS_ALTERNATES=""
fi

"$ENV_PYTHON" -m pip install --upgrade pip
"$ENV_PYTHON" -m pip install -r requirements.txt

echo "Environment ready."
echo "Activate with: $ACTIVATE_HINT"
if [ -n "$WINDOWS_ALTERNATES" ]; then
  echo "Windows shell alternatives: $WINDOWS_ALTERNATES"
fi
