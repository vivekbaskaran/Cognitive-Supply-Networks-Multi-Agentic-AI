#!/bin/bash

echo "Starting backend agent..."

# Move to project root
cd "$(dirname "$0")/.." || exit 1

# Activate backend virtual environment
source backend/.venv/bin/activate

# Move into backend directory
cd backend || exit 1

# Run backend correctly as module
uv run -m main