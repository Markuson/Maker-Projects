# ssh.sh - Connectar ràpid a dietpink

REMOTE="root@dietpink"

echo "→ Connectant a dietpink..."
ssh -t "$REMOTE" "cd /root/projects/dietpink && exec bash -l"