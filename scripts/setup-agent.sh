#!/bin/bash

# Move to project root (one level above scripts)
cd "$(dirname "$0")/.." || exit 1

# Move into backend directory
cd backend || exit 1

# Sync dependencies
uv sync