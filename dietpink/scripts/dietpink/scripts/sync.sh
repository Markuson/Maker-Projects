# sync.sh - Sync dietpink to Raspberry Pi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE="root@dietpink"
REMOTE_DIR="/root/projects/dietpink"

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Sync dietpink to Pi Zero W        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Local:${NC}  $PROJECT_ROOT"
echo -e "${YELLOW}Remote:${NC} $REMOTE:$REMOTE_DIR"
echo ""

# Verify SSH connection
echo -e "${BLUE}→${NC} Verifying SSH connection..."
echo -e "${YELLOW}Note:${NC} If prompted, enter your password for $REMOTE"
if ssh -o ConnectTimeout=10 "$REMOTE" exit; then
    echo -e "${GREEN}✓${NC} Connection established"
else
    echo -e "${RED}✗${NC}"
    echo -e "${RED}Error: Cannot connect to $REMOTE${NC}"
    echo "Verify that dietpink is powered on and accessible."
    exit 1
fi

# Rsync
echo -e "${BLUE}→${NC} Syncing files..."

rsync -avz --delete \
    --exclude '.git/' \
    --exclude '.gitignore' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --exclude '*.pyo' \
    --exclude '*.swp' \
    --exclude '.vscode/' \
    --exclude 'logs/*.log' \
    --exclude '*.tmp' \
    --exclude 'README.md' \
    --exclude 'README.MD' \
    --exclude 'software/eink/drivers/e-Paper/.git' \
    --progress \
    "$PROJECT_ROOT/" "$REMOTE:$REMOTE_DIR/"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Sync completed successfully!${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  ssh $REMOTE"
    echo "  cd $REMOTE_DIR/software/eink/examples"
    echo "  python3 clock.py"
else
    echo ""
    echo -e "${RED}✗ Error during sync${NC}"
    exit 1
fi