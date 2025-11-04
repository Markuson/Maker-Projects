# sync.sh - Sincronitzar dietpink a la Raspberry Pi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuració
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE="root@dietpink.local"
REMOTE_DIR="/root/projects/dietpink"

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Sync dietpink to Pi Zero W        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Local:${NC}  $PROJECT_ROOT"
echo -e "${YELLOW}Remote:${NC} $REMOTE:$REMOTE_DIR"
echo ""

# Verificar connexió SSH
echo -ne "${BLUE}→${NC} Verificant connexió SSH... "
if ssh -o ConnectTimeout=3 -o BatchMode=yes "$REMOTE" exit 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo -e "${RED}Error: No es pot connectar a $REMOTE${NC}"
    echo "Verifica que dietpink està engegada i accessible."
    exit 1
fi

# Rsync
echo -e "${BLUE}→${NC} Sincronitzant fitxers..."

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
    echo -e "${GREEN}✓ Sync completat amb èxit!${NC}"
    echo ""
    echo -e "${YELLOW}Pròxims passos:${NC}"
    echo "  ssh $REMOTE"
    echo "  cd $REMOTE_DIR/software/eink/examples"
    echo "  python3 clock.py"
else
    echo ""
    echo -e "${RED}✗ Error durant la sincronització${NC}"
    exit 1
fi