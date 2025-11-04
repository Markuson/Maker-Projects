# sync-run.sh - Sync i executar un script

if [ $# -eq 0 ]; then
    echo "Usage: ./sync-run.sh <script.py>"
    echo "Example: ./sync-run.sh clock.py"
    exit 1
fi

SCRIPT_NAME="$1"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE="root@dietpink.local"

# Sync primer
"$PROJECT_ROOT/scripts/sync.sh"

if [ $? -eq 0 ]; then
    echo ""
    echo "→ Executant $SCRIPT_NAME a dietpink..."
    echo ""
    ssh -t "$REMOTE" "cd /root/projects/dietpink/software/eink/examples && python3 $SCRIPT_NAME"
fi
EOF

chmod +x ~/Maker-Projects/dietpink/scripts/sync-run.sh
4.3. Script de Quick SSH
bashcat > ~/Maker-Projects/dietpink/scripts/ssh.sh << 'EOF'
#!/bin/bash
# ssh.sh - Connectar ràpid a dietpink

REMOTE="root@dietpink.local"

echo "→ Connectant a dietpink..."
ssh -t "$REMOTE" "cd /root/projects/dietpink && exec bash -l"