#!/usr/bin/env bash
set -euo pipefail
# Creates a local virtual environment and installs pinned requirements
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

if [ -d ".venv" ]; then
  echo ".venv already exists. Activating and installing requirements..."
else
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. Activate with: source .venv/bin/activate"
