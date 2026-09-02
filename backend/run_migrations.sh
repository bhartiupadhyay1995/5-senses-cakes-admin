#!/bin/bash
# Run Alembic migrations

set -e

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to backend directory
cd "$SCRIPT_DIR"

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run migrations
echo "Running Alembic migrations..."
alembic upgrade head
echo "✓ Migrations completed successfully!"
