#!/bin/bash
# ssh.sh - Quick connect to dietpink

REMOTE="root@dietpink"

echo "→ Connecting to dietpink..."
echo "Note: If prompted, enter your password for $REMOTE"
ssh -t "$REMOTE" "cd /root/projects/dietpink && exec bash -l"