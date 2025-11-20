#!/bin/bash
# sync.sh - Sync dietpink des de Pi a Mac (unidireccional)

echo "🔄 Sincronitzant dietpink des de Pi a PC..."
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Rutes
PI_HOST="root@dietpink"
PI_PATH="/root/projects/dietpink/"
MAC_PATH="$HOME/Maker-Projects/dietpink/"

# Verificar connexió
echo -e "${BLUE}📡 Verificant connexió amb dietpink...${NC}"
if ! ping -c 1 dietpink &>/dev/null; then
  echo "❌ No es pot connectar a dietpink"
  exit 1
fi
echo -e "${GREEN}✅ Connexió OK${NC}"
echo ""

# Rsync
echo -e "${BLUE}📦 Sincronitzant fitxers...${NC}"
rsync -avz --progress \
  --exclude='weather_config.json' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='*.log' \
  --exclude='.git' \
  --exclude='.DS_Store' \
  "${PI_HOST}:${PI_PATH}" \
  "${MAC_PATH}"

if [ $? -eq 0 ]; then
  echo ""
  echo -e "${GREEN}✅ Sincronització completada!${NC}"
  echo ""
  echo "📋 Fitxers sincronitzats a:"
  echo "   ${MAC_PATH}"
  echo ""
  echo "🔍 Comprova canvis amb:"
  echo "   cd ~/Maker-Projects/dietpink"
  echo "   git status"
else
  echo ""
  echo "❌ Error durant la sincronització"
  exit 1
fi

