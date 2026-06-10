#!/usr/bin/env bash
# setup_auth.sh — install JWT dependency and run auth migration
# Run from the project root: bash setup_auth.sh

set -e  # exit on first error

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# ── 1. Resolve Python ───────────────────────────────────────────────────────
# Use whatever python3 already has fastapi (the one running the server).
PYTHON=$(python3 -c "import fastapi; import sys; print(sys.executable)" 2>/dev/null || true)

if [ -z "$PYTHON" ]; then
    echo "ERROR: Could not find a python3 with fastapi installed."
    echo "       Make sure your virtual environment is active, then re-run."
    exit 1
fi

echo "Using Python: $PYTHON ($($PYTHON --version))"

# ── 2. Install PyJWT ────────────────────────────────────────────────────────
if $PYTHON -c "import jwt" 2>/dev/null; then
    JWT_VER=$($PYTHON -c "import jwt; print(jwt.__version__)")
    echo "PyJWT already installed (v$JWT_VER) — skipping."
else
    echo "Installing PyJWT..."
    $PYTHON -m pip install "PyJWT==2.13.0"
    echo "PyJWT installed."
fi

# ── 3. Check .env ───────────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: No .env file found."
    echo "         Create one before running migrations. Example:"
    echo ""
    echo "  DATABASE_URL=postgresql://user:password@localhost:5432/dbname"
    echo "  JWT_SECRET_KEY=$(LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c 48 2>/dev/null || echo 'replace-with-a-long-random-secret')"
    echo ""
    echo "Skipping migration. Re-run this script after creating .env."
    exit 0
fi

# ── 4. Run migration ────────────────────────────────────────────────────────
echo "Running database migrations..."
$PYTHON scripts/migrate.py
echo ""
echo "Done. Auth is ready."
