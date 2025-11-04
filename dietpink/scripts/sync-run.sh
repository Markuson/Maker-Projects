#!/bin/bash
# sync-run.sh - Sync and run a script

if [ $# -eq 0 ]; then
    echo "Usage: ./sync-run.sh <script.py>"
    echo "Example: ./sync-run.sh clock.py"
    exit 1
fi

SCRIPT_NAME="$1"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE="root@dietpink"

# Sync first
"$PROJECT_ROOT/scripts/sync.sh"

if [ $? -eq 0 ]; then
    echo ""
    echo "→ Running $SCRIPT_NAME on dietpink..."
    echo ""
    ssh -t "$REMOTE" "cd /root/projects/dietpink/software/eink/examples && python3 $SCRIPT_NAME"
fi